from finance import FinanceTracker
from auth import UserAuthentication
from menu_display_options import Menu
from cli_argparse import parse_args, handle_args


class MainMenu:
    def __init__(self, username:str):
        self.username = username
        self.tracker = FinanceTracker(username)
        self.menu = Menu(username)
        
    def run(self):
        while True:
            self.menu.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.menu.transactions_menu()
                sub_choice = input("Enter sub-option (1-5): ")
                if sub_choice == "1":
                    self.tracker.add_transaction()
                elif sub_choice == "2":
                    self.tracker.update_transaction()
                elif sub_choice == "3":
                    self.tracker.delete_transaction()
                elif sub_choice == "4":
                    self.tracker.view_transactions()
                elif sub_choice == "5":
                    file_path = input("Enter file path for import: ")
                    self.tracker.import_transactions(file_path)
                elif sub_choice == "0":
                    continue
            elif choice == "2":
                self.menu.budget_menu()
                sub_choice = input("Enter sub-option (1-2): ")
                if sub_choice == "1":
                    self.tracker.set_budget()
                elif sub_choice == "2":
                    self.tracker.view_budget()
                elif sub_choice == "0":
                    continue
            elif choice == "3":
                self.menu.data_analysis_menu()
                sub_choice = input("Enter sub-option (1-4): ")
                if sub_choice == "1":
                    self.tracker.view_financial_summary()
                elif sub_choice == "2":
                    file_path = input("Enter file path for export: ")
                    self.tracker.export_financial_summary(file_path)
                elif sub_choice == "3":
                    self.tracker.search_transactions()
                elif sub_choice == "4":
                    self.tracker.spending_reports_by_category()
                elif sub_choice == "0":
                    continue
            elif choice == "0":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    auth = UserAuthentication()
    while True:
        print("\nEnter your credentials to Login.")
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        if auth.verify_login(username, password):
            print("\nLogin successful! Welcome,", username)
            mainmenu = MainMenu(username)
            args = parse_args()
            if any(vars(args).values()):
                handle_args(args, mainmenu.tracker, username)
            else:
                mainmenu.run()
            break

        print("\nInvalid credentials.")
        choice = input("Forgot password? Type 'reset' or 'register' to create an account, or 'exit' to quit: ").strip().lower()

        if choice == "reset":
            auth.reset_password()  # Call reset password function
        elif choice == "register":
            auth.add_credentials()  # Let user register an account
        elif choice == "exit":
            print("Exiting application.")
            break
