import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Expense Tracker')

"""
page1 = SHEET.worksheet('page1')
data = page1.get_all_values()
print(data)
"""


class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        """
        Convert the result to a string instead of printing the memory address
        """
        return f"Expense: {self.name}, {self.category}, £{self.amount:.2f}"




def get_user_expenses():
    """
    We use this function to collect data from the user, including the expense
    name,category, and amount. If the user selects an incorrect category or
    fails to enter a number for the amount, we print a ValueError. We use 
    the While True function to keep repeating the code until the user 
    enters the correct values.
    """

    print(f" 🖍 Getting user expenses")
    name_of_expense = input("Enter your expense: ")
    while True:
        try:
            amount_of_expense = float(input("Enter the expense amount: "))
            # Input is successfully converted to a float, so break out of the
            #  loop
            break
        except ValueError:
            print("Invalid input. Please enter a valid number(e.g. 12.34, 5, 7.23).")
    
    category_expense = [
        "🏡  Housing",
        "🛒  Food and dining out",
        "🚃  Transportation",
        "🤑  Savings contributions",
        "🎮  Entertainment",
    ]

    while True:
        print("Selct a category to add the expense: ")
        for x, category_name in enumerate(category_expense):
            print(f"  {x + 1}. {category_name}")
        range_of_value = f"[1 - {len(category_expense)}]"
        try:
            select_index_value = int(
                input(f"Enter on of the categoy number: {range_of_value}")) - 1
            if select_index_value in range(len(category_expense)):
                choosen_category = category_expense[select_index_value]
                new_expense = Expense(name=name_of_expense, 
                category=choosen_category, amount=amount_of_expense)              
                return new_expense
            else:
                print("Invalid category. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def save_expenses_to_google_sheet(expense_store):
    """
     Add the expense to a Google Sheet.
    """
    print(f" 📌 Saving user expenses {expense_store}")

    # Convert the Expense object to a dictionary
    expense_dict = {
        "name": expense_store.name,
        "category": expense_store.category,
        "amount": expense_store.amount
    }

    page1_worksheet = SHEET.worksheet("page1")

    # Append the dictionary to the Google Sheet
    page1_worksheet.append_row([expense_dict["name"],
        expense_dict["category"], expense_dict["amount"]])
    print("Saved successfully.")


def view_expenses():
    print(f" 📋 View the expenses")


def expenses_tracker_main():
    # Get user imput for the expenses.
    expense_store = get_user_expenses()
    # Import the expenses in google sheet.
    save_expenses_to_google_sheet(expense_store)
    # View the expenses.
    view_expenses()


print("Welcome to Expense Tracker")
expenses_tracker_main()