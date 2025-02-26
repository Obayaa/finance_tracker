class Menu:
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