import datetime
import argparse
from finance import Transaction, FinanceTracker


def parse_args():
    parser = argparse.ArgumentParser(description="Finance Tracker CLI")
    
    # Transaction options
    parser.add_argument("--add-income", type=float, help="Add an income transaction")
    parser.add_argument("--add-expense", type=float, help="Add an expense transaction")
    parser.add_argument("--category", type=str, help="Specify transaction category")
    parser.add_argument("--description", type=str, help="Transaction description")
    
    # File operations
    parser.add_argument("--export", type=str, help="Export financial summary (CSV/JSON)")
    # Had to update import to inport to resolve naimg conflict
    parser.add_argument("--inport", type=str, help="Import transactions from CSV/JSON")
    
    return parser.parse_args()

def handle_args(args, tracker, username=None):
    """Handles command-line arguments and prevents duplicate transactions."""
    if args.add_income or args.add_expense:
        transaction_type = "income" if args.add_income else "expense"
        amount = args.add_income if args.add_income else args.add_expense
        category = args.category if args.category else "Other"
        description = args.description if args.description else "No description"
        date = datetime.date.today() if not args.date else datetime.datetime.strptime(args.date, "%Y-%m-%d").date()

        # Create transaction object
        transaction = Transaction(date, amount, category, description, transaction_type)

        # Check if the transaction already exists before adding
        if transaction in tracker.transactions[transaction.transaction_type]:
            print("\n⚠️ Duplicate transaction detected! Entry not added.\n")
            return

        # If unique, add transaction
        tracker = FinanceTracker()
        tracker.transactions[transaction.transaction_type].append(transaction)
        tracker.save_transactions()
        print(f"\n {transaction_type.capitalize()} of {amount} added successfully!\n")

    if args.export:
        tracker.export_financial_summary(args.export)
    
    if args.inport:
        tracker.import_transactions(args.inport)