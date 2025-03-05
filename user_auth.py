import mysql.connector
import bcrypt
import re

class UserAuthentication:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",  # Change if MySQL is hosted elsewhere
            user="root",  # Replace with your MySQL username
            password="blog@pp12",  # Replace with your MySQL password
            database="auth_system"
        )
        self.cursor = self.conn.cursor()

    def add_credentials(self):
        try:
            username = input("Enter Username: ").lower()

            # Check if username exists
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if self.cursor.fetchone():
                print("Username already exists.")
                return

            password = input("Enter Password: ")
            if len(password) < 8 or not re.search(r"\d", password) or \
               not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
                print("Password must meet the security requirements.")
                return

            security_answer = input("Set a security question answer: ").strip().lower()
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            self.cursor.execute(
                "INSERT INTO users (username, password_hash, security_answer) VALUES (%s, %s, %s)",
                (username, hashed_password, security_answer)
            )
            self.conn.commit()
            print("User registered successfully!")

        except Exception as e:
            print(f"Error: {e}")

    def verify_login(self, username, password):
        self.cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        user = self.cursor.fetchone()
        if user and bcrypt.checkpw(password.encode(), user[0].encode()):
            return True
        return False

    def reset_password(self):
        username = input("Enter your username: ").lower()
        self.cursor.execute("SELECT security_answer FROM users WHERE username = %s", (username,))
        user = self.cursor.fetchone()

        if not user:
            print("Username not found.")
            return

        security_answer = input("Security answer: ").strip().lower()
        if security_answer != user[0]:
            print("Incorrect answer.")
            return

        new_password = input("Enter new password: ")
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (hashed_password, username))
        self.conn.commit()
        print("Password has been reset successfully!")
