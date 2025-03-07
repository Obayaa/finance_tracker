import datetime
import argparse
import getpass
from finance import Transaction, FinanceTracker
from auth import UserAuthentication  # Import authentication module
import sys



def parse_args():
    parser = argparse.ArgumentParser(description="Finance Tracker CLI")

    # Username argument (now optional in argparse but required in logic)
    parser.add_argument("--username", type=str, help="Specify username (Required for all actions)")

    # Transaction options
    parser.add_argument("--add-income", type=float, help="Add an income transaction")
    parser.add_argument("--add-expense", type=float, help="Add an expense transaction")
    parser.add_argument("--category", type=str, help="Specify transaction category")
    parser.add_argument("--description", type=str, help="Transaction description")
    parser.add_argument("--date", type=str, help="Specify transaction date (YYYY-MM-DD)")

    # File operations
    parser.add_argument("--export", type=str, help="Export financial summary (CSV/JSON)")
    parser.add_argument("--inport", type=str, help="Import transactions from CSV/JSON")

    args = parser.parse_args()

    # If username is not provided, ask for it interactively
    if not args.username:
        args.username = input("Enter your username: ").strip()
        if not args.username:
            print("❌ Error: Username is required.")
            sys.exit(1)  # Exit the script

    return args



def handle_args(args):
    """Handles command-line arguments and ensures the user exists before performing actions."""

    auth = UserAuthentication()  # Create an authentication instance

    # Validate username before proceeding
    if not auth.check_user_exists(args.username):
        print(
            f"\n❌ Error: No account found for '{args.username}'. Please register or try again.\n"
        )
        return

    # Optional: Require password for extra security
    password = getpass.getpass(f"🔒 Enter password for {args.username}: ")
    if not auth.verify_login(args.username, password):
        print("\n❌ Incorrect password. Access denied.\n")
        return

    # Initialize FinanceTracker with verified user
    tracker = FinanceTracker(args.username)

    if args.add_income or args.add_expense:
        transaction_type = "income" if args.add_income else "expense"
        amount = args.add_income if args.add_income else args.add_expense
        category = args.category if args.category else "Other"
        description = args.description if args.description else "No description"
        date = (
            datetime.date.today()
            if not args.date
            else datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        )

        # Create transaction object
        transaction = Transaction(date, amount, category, description, transaction_type)

        # Check if the transaction already exists before adding
        if transaction in tracker.transactions[transaction.transaction_type]:
            print("\n⚠️ Duplicate transaction detected! Entry not added.\n")
            return

        # If unique, add transaction
        tracker.transactions[transaction.transaction_type].append(transaction)
        tracker.save_transactions()
        print(f"\n✅ {transaction_type.capitalize()} of {amount} added successfully!\n")

    if args.export:
        tracker.export_financial_summary(args.export)
        print(f"\n✅ Financial summary exported to {args.export}!\n")

    if args.inport:
        tracker.import_transactions(args.inport)
        print(f"\n✅ Transactions imported from {args.inport}!\n")


if __name__ == "__main__":
    args = parse_args()
    handle_args(args)