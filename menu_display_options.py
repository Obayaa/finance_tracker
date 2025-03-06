class Auth_Menu:
    def auth_menu(self):
        menu = """
        Select an option to login to the App
        ====================
        
        1. Register
        2. Login
        
        0. Exit
        ====================
        
        """
        print(menu)
        
class Menu:
    def __init__(self, username:str):
        self.username = username
        
    def display_menu(self):
        
        print(f"Finance Tracker - User: {self.username}")
            
        menu = """
        
        Welcome to your Finance Tracker Application.
        Please select an option below:
        ========================
        
        1. Manage Transactions
        2. Track Budget
        3. Financial Analysis & Reports
        
        0. Logout
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
        5. Search Transactions
        6. Import Transactions
        
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
        3. Spending Reports by Category
        
        0. Back
        ========================
        """
        print(menu)