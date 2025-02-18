import datetime
from dataclasses import dataclass
import json
from typing import List, Dict
from pathlib import Path as path
from tabulate import tabulate
from enum import Enum   


class Category(Enum):
    INCOME = "Income"
    GROCERIES = "Groceries"
    RENT = "Rent"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    TRANSPORTATION = "Transportation"
    SHOPPING = "Shopping"
    HEALTH = "Health"
    OTHER = "Other"

    @classmethod
    def list_categories(cls):
        return [cat.value for cat in cls]


@dataclass
class Transaction:
    date: datetime.date
    amount: float
    category: Category
    description: str
    transaction_type: str

    # Method to convert the transaction object to a dictionary. Without this there would be a TypeError
    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "amount": self.amount,
            "category": self.category.value,
            "description": self.description,
            "transaction_type": self.transaction_type,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        return cls(
            date=datetime.date.fromisoformat(data["date"]),
            amount=float(data["amount"],),
            category=Category(data["category"]),
            description=data["description"],
            transaction_type=data["transaction_type"],
        )


class Budget:
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount


class FinanceTracker:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.budgets: Dict[Category, Budget] = {}
        self.transactions_file = path("transactions.json")
        self.load_transactions()
        print("\nWelcome to the Finance Tracker App.")
        print(
            "We offer opportunities for users to track their expenses, income and budget."
        )
        print("\nLet's get started.")

    # Let's create a function to load the transactions from the file. This is because, without loading, the file would keep updating itself with existing.
    def load_transactions(self):
        if not self.transactions_file.exists():
            return
        
        with open(self.transactions_file, "r") as file:
            data = json.load(file)
            
            self.transactions = [Transaction.from_dict(transaction) for transaction in data["transactions"]]
            if data.get("budgets") and isinstance(data["budgets"], list) and data["budgets"]:
                self.budgets = {
                    category: Budget(budget["category"], budget["amount"])
                    for category, budget in data["budgets"][0].items()
                }
                
            else:
                self.budgets = {}
            

    # Let's create a function to handle saving transactions to a file
    def save_transactions(self):
        transactions_dict = {
            "transactions": [
                transaction.to_dict() for transaction in self.transactions
            ],
            "budgets": [
                {
                    category: {"category": budget.category, "amount": budget.amount}
                    for category, budget in self.budgets.items()
                },
            ],
        }

        with open(self.transactions_file, "w") as file:
            json.dump(transactions_dict, file, indent=4)

    def add_transaction(self):
        try:
            date = input("Enter the date of the transaction (YYYY-MM-DD): ")
            datetime.datetime.strptime(date, "%Y-%m-%d")

            amount = float(input("Enter the amount of the transaction: "))
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")

            print("\n Available Categories:")
            categories = Category.list_categories()

            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")

            cat_choice = int(input("Select category number: "))
            if 1 <= cat_choice <= len(Category):
                category = list(Category)[cat_choice - 1]
            else:
                raise ValueError(
                    "Invalid category choice. Please select a valid category."
                )

            description = input("Enter the description of the transaction: ")

            transaction_type = input(
                "Enter the type of the transaction (income or expense): "
            )
            if transaction_type not in ["income", "expense"]:
                print("Invalid transaction type. Please enter 'income' or 'expense'.")
                return

            transaction = Transaction(
                date, amount, category, description, transaction_type
            )
            self.transactions.append(transaction)
            self.save_transactions()

            print("\nTransaction added successfully.")
        except ValueError:
            print(f"Error: Invalid input")

    def view_transactions(self):
        if not self.transactions:
            print("No transactions available.")
            return
        else:
            print("\nTransactions:")
            headers = ["Date", "Amount", "Category", "Description", "Type"]
            self.transactions.sort(reverse=True, key=lambda x: x.date)
            table = tabulate(self.transactions, headers=headers, tablefmt="fancy_grid")
            print(table)

    def set_budget(self):
        print("\nTo Set Budget, Please provide the following details:")
        print("Available Categories: \n")
        categories = Category.list_categories()
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")

        cat_choice = int(input("Select category number: "))
        if 1 <= cat_choice <= len(Category):
            category = list(Category)[cat_choice - 1]
        else:
            raise ValueError("Invalid category choice. Please select a valid category.")

        amount = float(input("Enter the budget amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        self.category = category
        self.amount = amount
        self.budgets[category] = Budget(category, amount)
        self.save_transactions()
        print(f"Budget set for {category} category: {amount}")

    def view_budgets(self):
        if not self.budgets:
            print("No budgets available.")
            return
        else:
            print("\nBudgets:")
            headers = ["Category", "Amount"]
            rows = [
                [budget.category.value, budget.amount] for budget in self.budgets.values()
            ]
            print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

    def display_menu(self):
        """Display the main menu of the application."""
        menu = """
        Personal Finance Tracker
        ===============================

            1. Add Transaction
            2. View Transactions
            3. Set Budget
            4. View Budgets
            5. View Financial Summary
            6. Exit

        ===============================
        """
        print(menu)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.set_budget()
            elif choice == "4":
                self.view_budgets()
            elif choice == "5":
                print("View Financial Summary")
            elif choice == "6":
                print(
                    "Exiting the application. Thank you for using the Finance Tracker App."
                )
                break
            else:
                print("Invalid choice. Please enter a valid choice.")


if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.run()
