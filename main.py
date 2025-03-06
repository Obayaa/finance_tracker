from finance import FinanceTracker
from menu_display_options import Auth_Menu, Menu
from cli_argparse import parse_args, handle_args
from auth import UserAuthentication


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
                    self.tracker.search_transactions()
                elif sub_choice == "6":
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
                    self.tracker.export_financial_summary()
                elif sub_choice == "3":
                    self.tracker.spending_reports_by_category()
                elif sub_choice == "0":
                    continue
            elif choice == "0":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu = Auth_Menu()
    auth = UserAuthentication()

    while True:
        menu.auth_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":  # Register
            if auth.register():  
                username = auth.username  
                mainmenu = MainMenu(username)
                mainmenu.run()
        
        elif choice == "2":  # Login
            if auth.login(): 
                username = auth.username 
                mainmenu = MainMenu(username)  
                mainmenu.run()
        
        elif choice == "0":  # Exit
            print("Exiting application.")
            break
        else:
            print("Incorrect choice. Please pick a choice from the options in the menu")