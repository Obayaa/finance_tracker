from dataclasses import dataclass
import bcrypt
import getpass
import re
from pathlib import Path
from typing import List, Dict
import json


@dataclass
class Credentials:
    username: str
    password: str

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Credentials":
        return cls(
            username=data["username"],
            password=data["password"],
        )


class UserAuthentication:
    def __init__(self):
        self.credentials: Dict[str, List[Credentials]] = {"Auth": []}
        self.credentials_file = Path("credentials.json")
        self.load_credentials()

    def load_credentials(self):
        if self.credentials_file.exists():
            with open(self.credentials_file, "r") as file:
                logins = json.load(file)
                login_credentials = logins.get("credentials", {})

                if isinstance(login_credentials, dict):
                    self.credentials = {
                        "Auth": [
                            Credentials.from_dict(l)
                            for l in login_credentials.get("Auth", [])
                        ],
                    }
                else:
                    self.credentials = {"Auth": []}
                    print("Warning: Invalid credentials format.")

    def save_credentials(self):
        data = {
            "credentials": {"Auth": [l.to_dict() for l in self.credentials["Auth"]]}
        }
        with open(self.credentials_file, "w") as file:
            json.dump(data, file, indent=4)


    def register(self):
        try:
            while True:
                username = input("Enter Username: ").lower()
                if any(cred.username == username for cred in self.credentials["Auth"]):
                    print("Username already exists. Please try a different one.")
                else:
                    break

            while True:
                password = input("Enter Password: ")
                if len(password) < 8:
                    print("Your password must be at least 8 characters long.")
                elif not re.search(r"\d", password):
                    print("Password must contain at least one number.")
                elif not re.search(r"[A-Z]", password):
                    print("Password must contain at least one uppercase letter.")
                elif not re.search(r"[a-z]", password):
                    print("Password must contain at least one lowercase letter.")
                else:
                    break

            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_credentials = Credentials(username=username, password=hashed_password)
            self.credentials["Auth"].append(new_credentials)
            self.save_credentials()
            
            print("User registered successfully!")
            self.username = username  # Store username
            return True  # Indicate success

        except Exception as e:
            print(f"Error adding credentials: {e}")
            return False  # Indicate failure


    def login(self):
        username = input("Enter Username: ").lower()
        password = getpass.getpass("Enter Password: ")

        attempts = 3
        while attempts > 0:
            for cred in self.credentials["Auth"]:
                if cred.username == username:
                    if bcrypt.checkpw(password.encode(), cred.password.encode()):
                        print("Login Successful!")
                        self.username = username  # Store logged-in username
                        return True  # Indicate success
            attempts -= 1
            if attempts > 0:
                print(f"Incorrect password. You have {attempts} attempts remaining.")
                password = getpass.getpass("Re-enter Password: ")

        print("Login failed.")
        return False  # Indicate failure



    def verify_login(self, username, password):
        attempts = 3
        while attempts > 0:
            for cred in self.credentials["Auth"]:
                if cred["username"] == username:  # Ensure dictionary access
                    if bcrypt.checkpw(password.encode(), cred["password"].encode()):
                        return True
            attempts -= 1
            if attempts > 0:
                print(f"Incorrect password. You have {attempts} attempts remaining.")
                password = getpass.getpass("Re-enter Password: ")  # Use getpass for security
        return False

    def check_user_exists(self, username):
        """Check if a username exists in the system"""
        for cred in self.credentials["Auth"]:
            if cred.username == username:
                return True
        return False

    def reset_password(self):
        username = input("Enter your username: ").lower()

        if not self.check_user_exists(username):
            print("Username not found. Please register for an account.")
            return

        user_found = next(
            (cred for cred in self.credentials["Auth"] if cred.username == username),
            None,
        )

        if not user_found:
            print("Error retrieving user data.")
            return

        attempts = 3
        while attempts > 0:
            security_answer = input("For security, what was your first pet's name? ").strip().lower()
            if security_answer == user_found.security_answer:
                new_password = input("Enter new password: ")

                if len(new_password) < 8:
                    print("Your password must be at least 8 characters long")
                    return

                if not re.search(r"\d", new_password):
                    print("Password must contain at least one number")
                    return

                if not re.search(r"[A-Z]", new_password):
                    print("Password must contain at least one uppercase letter")
                    return

                if not re.search(r"[a-z]", new_password):
                    print("Password must contain at least one lowercase letter")
                    return

                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                user_found.password = hashed_password
                self.save_credentials()
                print("Password has been reset successfully!")
                return
            else:
                attempts -= 1
                print(f"Incorrect answer. {attempts} attempts remaining.")
        
        print("Too many failed attempts. Consider contacting support for recovery.")
