# Finance Tracker Application

A comprehensive personal finance management tool built in Python that helps users track income, expenses, manage budgets, and generate financial reports.

## Features

### **User Authentication**
- Secure login and registration
- Password reset functionality with security questions
- Password validation:
  - Minimum **8 characters**
  - At least **one uppercase letter**
  - At least **one lowercase letter**
  - At least **one number**
- Login attempts limited to prevent brute-force attacks
- General error message for invalid credentials to avoid exposing user existence


### **Transaction Management**
- Add, view, update, and delete transactions
- Delete multiple transactions at once
- **Prevent duplicate transactions**
- Categorize expenses automatically using NLP
- Search transactions by **date, category, or description**
- Import/export transactions from **CSV or JSON files**
- **Command-line support** for quick transaction entry


### **Budget Tracking**
- Set budgets for different spending categories
- Real-time budget alerts when exceeding limits
- View remaining budget for each category

### **Financial Analysis**
- View **financial summaries and reports**
- Track **spending by category**
- Export financial data to **CSV or JSON**
- Exported reports are saved in a **dedicated `financial_summary/` folder**

### **Command Line Interface**
- Add transactions **directly from the terminal**
- Import/export transactions via CLI
- Supports quick financial tracking **without navigating the menu**
- **Prevents duplicate transactions when adding via CLI**

---

## **Installation**

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/finance-tracker.git
   cd finance-tracker
   ```

2. Create and activate a virtual environment:
   
   **For Windows:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **For macOS/Linux:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Download **NLTK data** (needed for auto-categorization):
   ```sh
   python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')"
   ```

---

## Requirements

- Python 3.7+
- Required packages:
  - pandas
  - nltk
  - tabulate
  - bcrypt

---

## 🚀 Usage

### **1️⃣ Running the Application (Interactive Mode)**
To use the **interactive menu**, run:
```bash
python main.py
```
- **Register** or **Login**
- **Manage Transactions**
- **View Financial Reports**
- **Set and Track Budgets**
- **Import & Export Data**

---

### **2️⃣ Using CLI for Quick Operations**
Use **CLI commands** to perform actions **without opening the interactive menu**.

#### ➕ **Adding Income**
```bash
python cli_argparse.py --username Isaac --add-income 1000 --category "Salary" --description "Monthly salary"
```

#### ➖ **Adding Expense**
```bash
python cli_argparse.py --username Isaac --add-expense 50 --category "Groceries" --description "Weekly groceries"
```

#### 📤 **Exporting Transactions**
```bash
python cli_argparse.py --username Isaac --export summary.csv
```

#### 📥 **Importing Transactions**  
(Note: We use `--inport` instead of `--import` due to a naming conflict.)
```bash
python cli_argparse.py --username Isaac --inport transactions.json
```

---

## **File Structure**
```
finance-tracker/
│── main.py                    # Main application entry point
│── auth.py                     # User authentication system
│── finance.py                   # Core finance tracking functionality
│── menu_display_options.py       # Menu system for the application
│── cli_argparse.py               # Command line interface functionality
│── transactions/                 # Stores transaction data per user
│── test_file/                     # Contains test.csv for importing transactions
│── credentials.json               # Stores user credentials
│── financial_summary/             # Stores exported financial reports
```

---

## **Data Storage**
- **User credentials** are stored in `credentials.json`
- **Transaction data** is stored in `transactions/{username}_transactions.json`
- **All data is stored locally** on the user's machine
- **Financial summaries** are saved in the `financial_summary/` folder

---

## **Security Features**
- **Passwords are hashed** using `bcrypt`
- **Login attempts are limited** to prevent brute force attacks
- **General error messages** for failed login attempts to avoid exposing valid usernames
- **Security questions** provide additional **account recovery options**

### **Password Validation Requirements**
| Password         | ✅ Valid / ❌ Invalid | Reason |
|-----------------|---------------------|--------|
| `password`      | ❌ Invalid | No uppercase, no number |
| `Password`      | ❌ Invalid | No number |
| `Password1`     | ✅ Valid | Meets all criteria |
| `Pass1`         | ❌ Invalid | Less than 8 characters |

---

## **Example Usage**

1. **Register** a new user account
2. **Login** with your credentials
3. **Add income and expense transactions**
4. **Set budgets** for different categories
5. **View financial summaries and reports**
6. **Import/Export data** for external analysis

---

## **Contributing**
Contributions are welcome! Please feel free to submit a Pull Request.
