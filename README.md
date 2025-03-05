# Finance Tracker Application

A comprehensive personal finance management tool built in Python that helps users track income, expenses, manage budgets, and generate financial reports.

## Features

- **User Authentication**
  - Secure login and registration
  - Password reset functionality with security questions
  - Password validation (minimum 8 characters, numbers, uppercase, lowercase)

- **Transaction Management**
  - Add, view, update, and delete transactions
  - Categorize expenses automatically using NLP
  - Import/export transactions from CSV or JSON files

- **Budget Tracking**
  - Set budgets for different spending categories
  - Real-time budget alerts when exceeding limits
  - View remaining budget for each category

- **Financial Analysis**
  - View financial summaries and reports
  - Track spending by category
  - Export financial data for external analysis
  - Search transactions by date, category, or description

- **Command Line Interface**
  - Quick operations without navigating the menu
  - Supports adding transactions or importing/exporting data directly

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/finance-tracker.git
   cd finance-tracker
   ```

2. Create and activate a virtual environment:
   
   **For Windows:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **For macOS/Linux:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download NLTK data (needed for auto-categorization):
   ```
   python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')"
   ```


## Requirements

- Python 3.7+
- Required packages:
  - pandas
  - nltk
  - tabulate
  - bcrypt

## Usage

### Running the Application

```
python main.py
```

### Command Line Arguments

```
python main.py --add-income 1000 --category "Salary" --description "Monthly salary"
python main.py --add-expense 50 --category "Groceries" --description "Weekly groceries"
python main.py --export summary.csv
python main.py --inport transactions.json
```

## File Structure

- `main.py` - Main application entry point
- `auth.py` - User authentication system
- `finance.py` - Core finance tracking functionality
- `menu_display_options.py` - Menu system for the application
- `cli_argparse.py` - Command line interface functionality
- `transactions/` - Directory for storing transaction data for each user
- `files/` - Directory for storing financial summary and test file for the import transaction
- `credentials.json` - User credentials storage

## Data Storage

- User credentials are stored in `credentials.json`
- Transaction data is stored in `transactions/{username}_transactions.json`
- All data is stored locally on the user's machine

## Security

- Passwords are hashed using bcrypt
- Login attempts are limited to prevent brute force attacks
- Security questions provide an additional layer of account recovery

## Example Usage

1. Register a new user account
2. Login with your credentials
3. Add income and expense transactions
4. Set budgets for different categories
5. View financial summaries and reports
6. Export data for external analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


