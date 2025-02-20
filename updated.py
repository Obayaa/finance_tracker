import datetime
import json
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
from tabulate import tabulate
import csv
import datetime
import pandas as pd


class Category:
    CATEGORIES = [
        "Groceries", "Rent", "Utilities", "Entertainment",
        "Transportation", "Shopping", "Health", "Other"
    ]

    @classmethod
    def list_categories(cls):
        return cls.CATEGORIES


@dataclass
class Transaction:
    date: datetime.date
    amount: float
    category: str
    description: str
    transaction_type: str

    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_type": self.transaction_type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        return cls(
            date=datetime.date.fromisoformat(data["date"]),
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
            transaction_type=data["transaction_type"],
        )


class FinanceTracker:
    def __init__(self):
        self.transactions: Dict[str, List[Transaction]] = {"income": [], "expense": []}
        self.budgets: Dict[str, float] = {}
        self.transactions_file = Path("transactions.json")
        self.load_transactions()

    def load_transactions(self):
        if self.transactions_file.exists():
            with open(self.transactions_file, "r") as file:
                data = json.load(file)
                transactions_data = data.get("transactions", {})
                
                if isinstance(transactions_data, dict):
                    self.transactions = {
                        "income": [Transaction.from_dict(t) for t in transactions_data.get("income", [])],
                        "expense": [Transaction.from_dict(t) for t in transactions_data.get("expense", [])]
                    }
                else:
                    self.transactions = {"income": [], "expense": []}
                    print("Warning: Invalid transactions format. Resetting to default.")
                
                self.budgets = data.get("budgets", {})
                if not isinstance(self.budgets, dict):
                    self.budgets = {}
                    print("Warning: Invalid budgets format. Resetting to default.")

    def save_transactions(self):
        data = {
            "transactions": {
                "income": [t.to_dict() for t in self.transactions["income"]],
                "expense": [t.to_dict() for t in self.transactions["expense"]]
            },
            "budgets": self.budgets,
        }
        with open(self.transactions_file, "w") as file:
            json.dump(data, file, indent=4)

    def add_transaction(self):
        try:
            print("\nAdding a new transaction...")
            transaction_type = input("Enter type (income/expense): ").lower()
            if transaction_type not in ["income", "expense"]:
                raise ValueError("Invalid transaction type. Choose 'income' or 'expense'.")
            
            date_str = input("Enter the date (YYYY-MM-DD): ")
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(input("Enter amount: "))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            
            if transaction_type == "income":
                category = "Salary"
            else:
                print("\nAvailable Categories:")
                for i, cat in enumerate(Category.list_categories(), 1):
                    print(f"{i}. {cat}")
                cat_choice = int(input("Select category number: "))
                category = Category.list_categories()[cat_choice - 1]
            
            description = input("Enter description: ")
            transaction = Transaction(date, amount, category, description, transaction_type)
            self.transactions[transaction_type].append(transaction)
            self.save_transactions()
            print("\nTransaction added successfully!\n")
        except ValueError as e:
            print(f"\nInput Error: {e}\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
    
    def delete_transaction(self):
        print("\nDelete a Transaction\n")
        all_transactions = self.transactions["income"] + self.transactions["expense"]
        if not all_transactions:
            print("No transactions recorded.\n")
            return
        
        headers = ["Index", "Date", "Amount", "Category", "Description", "Type"]
        rows = [[i, t.date, t.amount, t.category, t.description, t.transaction_type] for i, t in enumerate(all_transactions)]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        
        try:
            index = int(input("Enter transaction index to delete: "))
            if 0 <= index < len(all_transactions):
                transaction = all_transactions.pop(index)
                self.transactions[transaction.transaction_type].remove(transaction)
                self.save_transactions()
                print("Transaction deleted successfully!\n")
            else:
                print("Invalid index.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")

    def update_transaction(self):
        print("\nUpdate a Transaction\n")
        all_transactions = self.transactions["income"] + self.transactions["expense"]
        if not all_transactions:
            print("No transactions recorded.\n")
            return
        
        headers = ["Index", "Date", "Amount", "Category", "Description", "Type"]
        rows = [[i, t.date, t.amount, t.category, t.description, t.transaction_type] for i, t in enumerate(all_transactions)]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        
        try:
            index = int(input("Enter transaction index to update: "))
            if 0 <= index < len(all_transactions):
                transaction = all_transactions[index]
                
                new_date = input(f"Enter new date (YYYY-MM-DD) [{transaction.date}]: ") or transaction.date
                new_amount = input(f"Enter new amount [{transaction.amount}]: ")
                new_category = input(f"Enter new category [{transaction.category}]: ") or transaction.category
                new_description = input(f"Enter new description [{transaction.description}]: ") or transaction.description
                new_type = input(f"Enter new type (income/expense) [{transaction.transaction_type}]: ") or transaction.transaction_type
                
                transaction.date = datetime.date.fromisoformat(new_date) if new_date else transaction.date
                transaction.amount = float(new_amount) if new_amount else transaction.amount
                transaction.category = new_category
                transaction.description = new_description
                transaction.transaction_type = new_type
                
                self.save_transactions()
                print("Transaction updated successfully!\n")
            else:
                print("Invalid index.\n")
        except ValueError:
            print("Invalid input. Please enter the correct values.\n")
            

    def view_transactions(self):
        all_transactions = self.transactions["income"] + self.transactions["expense"]
        if not all_transactions:
            print("\nNo transactions recorded.\n")
            return
        print("\nAll Transactions\n")
        headers = ["Date", "Amount", "Category", "Description", "Type"]
        rows = [[t.date, t.amount, t.category, t.description, t.transaction_type] for t in all_transactions]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        print()
        
    def import_transactions(self, file_path):
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".json"):
                df = pd.read_json(file_path)
            else:
                print("Invalid file format. Please provide a CSV or JSON file.")
                return
            
            df["date"] = pd.to_datetime(df["date"], dayfirst=True).dt.strftime("%Y-%m-%d")
            
            for _, row in df.iterrows():
                transaction = Transaction(
                    date=datetime.date.fromisoformat(row["date"]),
                    amount=float(row["amount"],),
                    category=row["category"],
                    description=row["description"],
                    transaction_type=row["transaction_type"]
                )
                self.transactions[transaction.transaction_type].append(transaction)
            self.save_transactions()
            print("\nTransactions imported successfully!\n")
            
        except Exception as e:
            print(f"\nError importing transactions: {e}\n")
            
    
    def view_financial_summary(self):
        print("\nFinancial Summary\n")
        
        # Display all income transactions
        print("Income Breakdown:")
        income_headers = ["Date", "Amount", "Description"]
        income_rows = [[t.date, t.amount, t.description] for t in self.transactions["income"]]
        print(tabulate(income_rows, headers=income_headers, tablefmt="fancy_grid"))
        
        total_income = sum(t.amount for t in self.transactions["income"])
        print(f"Total Income: {total_income}\n")
        
        # Display all expense transactions
        print("Expense Breakdown:")
        expense_headers = ["Date", "Amount", "Category", "Description"]
        expense_rows = [[t.date, t.amount, t.category, t.description] for t in self.transactions["expense"]]
        print(tabulate(expense_rows, headers=expense_headers, tablefmt="fancy_grid"))
        
        total_expense = sum(t.amount for t in self.transactions["expense"])
        net_savings = total_income - total_expense
        print(f"Total Expenses: {total_expense}")
        print(f"Actual Savings (after expenses): {net_savings}\n")
        
        # Display budget breakdown
        print("Budget Breakdown:")
        budget_headers = ["Category", "Budgeted Amount", "Spent", "Remaining"]
        budget_rows = []
        total_budget = sum(self.budgets.values())
        for category, budget in self.budgets.items():
            spent = sum(t.amount for t in self.transactions["expense"] if t.category == category)
            remaining = budget - spent
            budget_rows.append([category, budget, spent, remaining])
        print(tabulate(budget_rows, headers=budget_headers, tablefmt="fancy_grid"))
        
        planned_savings = total_income - total_budget
        print(f"Total Budget Allocation: {total_budget}")
        print(f"Planned Savings (after budgeting): {planned_savings}\n")
        
    def search_transactions(self):
        print("\nSearch Transactions\n")
        keyword = input("Enter keyword (date, category, or description): ").lower()
        filtered = [t for t in self.transactions["income"] + self.transactions["expense"]
                    if keyword in t.date.strftime("%Y-%m-%d")
                    or keyword in t.category.lower()
                    or keyword in t.description.lower()]
        if not filtered:
            print("\nNo matching transactions found.\n")
            return
        headers = ["Date", "Amount", "Category", "Description", "Type"]
        rows = [[t.date, t.amount, t.category, t.description, t.transaction_type] for t in filtered]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        print()

    def export_financial_summary(self, file_path):
        try:
            income_data = [[t.date, t.amount, t.description] for t in self.transactions["income"]]
            income_sum = sum(t.amount for t in self.transactions["income"])
            
            expense_data = [[t.date, t.amount, t.category, t.description] for t in self.transactions["expense"]]
            total_expense = sum(t.amount for t in self.transactions["expense"])
            net_savings = income_sum - total_expense
            
            budget_data = []
            for category, budget in self.budgets.items():
                spent = sum(t.amount for t in self.transactions["expense"] if t.category == category)
                remaining = budget - spent
                budget_data.append([category, budget, spent, remaining])
                
            total_budget = sum(self.budgets.values())
            planned_savings = income_sum - total_budget
            
            if file_path.endswith(".csv"):
                with open(file_path, "w", newline="") as file:
                    file.write("Income Breakdown\n")
                    df_income = pd.DataFrame(income_data, columns=["Date", "Amount", "Description"])
                    if not df_income.empty:
                        df_income.to_csv(file, index=False)
                    
                    file.write("\nTotal Income:," + str(income_sum) + "\n")
                        
                    file.write("\nExpense Breakdown\n")
                    df_expense = pd.DataFrame(expense_data, columns=["Date", "Amount", "Category", "Description"])
                    if not df_expense.empty:
                        df_expense.to_csv(file, index=False)
                        
                    file.write(f"\nTotal Expenses: {total_expense} \n")
                    file.write(f"Actual Savings (after expenses):  {net_savings} \n\n")
                    
                        
                    file.write("Budgets Breakdown\n")
                    df_budget = pd.DataFrame(budget_data, columns=["Category", "Budgetted Amount", "Spent", "Remaining"])
                    if not df_budget.empty:
                        df_budget.to_csv(file, index=False)
                    
                    file.write(f"\nTotal Budget Allocation: {total_budget} \n")
                    file.write(f"Planned Savings (after budgeting): {planned_savings} \n")
                        
            elif file_path.endswith(".json"):
                data = {
                    "income": {"transactions": income_data, "total_income": income_sum },
                    "expense": {"transactions": expense_data, "total_expense": total_expense, "net_savings": net_savings},
                    "budgets": {"transactions": budget_data, "total_budget": total_budget, "planned_savings": planned_savings}
                }
                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)
                    
            print(f"\nFinancial summary successfully exported to {file_path}\n")
        
        except Exception as e:
            print(f"\nError exporting data: {e}\n")
    
    def set_budget(self):
        print("\nSet Budget for a Category\n")
        print("Available Categories:")
        for i, cat in enumerate(Category.list_categories(), 1):
            print(f"{i}. {cat}")
        try:
            cat_choice = int(input("Select category number: "))
            category = Category.list_categories()[cat_choice - 1]
            amount = float(input("Enter budget amount: "))
            if amount <= 0:
                raise ValueError("Budget amount must be greater than zero.")
            
            total_income = sum(t.amount for t in self.transactions["income"])
            total_budget = sum(self.budgets.values()) + amount
            
            if total_budget > total_income:
                print(f"\nError: Total budget allocation ({total_budget}) exceeds total income ({total_income}). Please adjust the budget.\n")
                return
            
            self.budgets[category] = amount
            self.save_transactions()
            print(f"\nBudget set for {category}: {amount}\n")
        except ValueError as e:
            print(f"\nInput Error: {e}\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
    
    def view_budget(self):
        print("\nBudget Overview\n")
        if not self.budgets:
            print("No budgets set.\n")
            return
        headers = ["Category", "Budget", "Spent", "Remaining"]
        rows = []
        for category, budget in self.budgets.items():
            spent = sum(t.amount for t in self.transactions["expense"] if t.category == category)
            remaining = budget - spent
            rows.append([category, budget, spent, remaining])
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        print()
        
    def spending_reports_by_category(self):
        print("\nSpending Reports by Category\n")
        if not self.transactions["expense"]:
            print("No expense transactions recorded.\n")
            return
        
        category_totals = {}
        for transaction in self.transactions["expense"]:
            category_totals[transaction.category] = category_totals.get(transaction.category, 0) + transaction.amount
        
        headers = ["Category", "Total Spent"]
        rows = [[category, amount] for category, amount in category_totals.items()]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        
        # Identify Top 3 Spending Categories
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        print("\nTop 3 Spending Categories:")
        for i, (category, amount) in enumerate(sorted_categories[:3], 1):
            print(f"{i}. {category}: {amount}")
        
        # Identify Biggest Expense
        biggest_expense = max(self.transactions["expense"], key=lambda t: t.amount, default=None)
        if biggest_expense:
            print("\nBiggest Expense:")
            print(f"{biggest_expense.category} - {biggest_expense.amount} on {biggest_expense.date} ({biggest_expense.description})")
        print()

    
    def display_menu(self):
        menu = """
        
        Welcome to our Finance Tracker Application.
        Please select an option below:
        ========================
        
        1. Manage Transactions
        2. Track Budget
        3. Data Analysis & Reports
        
        0. Exit
        ========================
        """
        print(menu)
    
    def transactions_menu(self):
        menu = """
        Manage Transactions
        ========================
        
        1. Add Transaction
        2. Update Transaction
        3. Delete Transaction
        4. View Transactions
        5. Import Transactions
        
        0. Back
        ========================
        """
        print(menu)
    
    def budget_menu(self):
        menu = """
        Track Budget
        ========================
        
        1. Set Budget
        2. View Budget
        
        0. Back
        ========================
        """
        print(menu)

    def data_analysis_menu(self):
        menu = """
        Data Analysis & Reports
        ========================
        
        1. View Financial Summary
        2. Export Financial Summary
        3. Search Transactions
        4. Spending Reports by Category
        
        0. Back
        ========================
        """
        print(menu)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.transactions_menu()
                sub_choice = input("Enter sub-option (1-5): ")
                if sub_choice == "1":
                    self.add_transaction()
                elif sub_choice == "2":
                    self.update_transaction()
                elif sub_choice == "3":
                    self.delete_transaction()
                elif sub_choice == "4":
                    self.view_transactions()
                elif sub_choice == "5":
                    file_path=input("Enter file path for import: ")
                    self.import_transactions(file_path)
                elif sub_choice == "0":
                    continue
            elif choice == "2":
                self.budget_menu()
                sub_choice = input("Enter sub-option (1-2): ")
                if sub_choice == "1":
                    self.set_budget()
                elif sub_choice == "2":
                    self.view_budget()
                elif sub_choice == "0":
                    continue
            elif choice == "3":
                self.data_analysis_menu()
                sub_choice = input("Enter sub-option (1-4): ")
                if sub_choice == "1":
                    self.view_financial_summary()
                elif sub_choice == "2":
                    file_path=input("Enter file path for export: ")
                    self.export_financial_summary(file_path)
                elif sub_choice == "3":
                    self.search_transactions()
                elif sub_choice == "4":
                    self.spending_reports_by_category()
                elif sub_choice == "0":
                    continue
            elif choice == "0":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.run()