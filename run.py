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


def remove_commas(input_str):
    # Remove any commas from the input
    return input_str.replace(',', '')


def get_user_expenses():
    """
    We use this function to collect data from the user, including the expense
    name, category, and amount. If the user selects an incorrect category or
    fails to enter a valid number for the amount, we print a ValueError. We use
    the While True function to keep repeating the code until the user
    enters the correct values.
    """

    print(f" 🖍 Getting user expenses")
    name_of_expense = input("Enter your expense: ")
    while True:
        amount_of_expense = input("Enter the expense amount: ")
        amount_of_expense = remove_commas(amount_of_expense)

        try:
            amount_of_expense = float(amount_of_expense)
            # Input is successfully converted to a float, so break out of the loop
            break
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g. 1200.50, 5, 7.23).")

    category_expense = [
        "🏡  Housing",
        "🛒  Food and dining out",
        "🚃  Transportation",
        "🤑  Savings contributions",
        "🎮  Entertainment",
    ]

    while True:
        print("Select a category to add the expense: ")
        for x, category_name in enumerate(category_expense):
            print(f"  {x + 1}. {category_name}")
        range_of_value = f"[1 - {len(category_expense)}]"
        try:
            select_index_value = int(
                input(f"Enter one of the category numbers: {range_of_value}")) - 1
            if select_index_value in range(len(category_expense)):
                chosen_category = category_expense[select_index_value]
                new_expense = Expense(name=name_of_expense,
                                      category=chosen_category, amount=amount_of_expense)
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


def calculate_total_expenses_by_category():
    print("Calculating total expenses by category:")
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()

    # Create a dictionary to categorize and calculate expenses by category
    categories_total = {}
    for row in data[1:]:
        name, category, amount = row
        if category not in categories_total:
            categories_total[category] = 0
        categories_total[category] += float(amount)

    # Print total expenses by category
    for category, total_amount in categories_total.items():
        print(f"{category}: £{total_amount:.2f}")

def view_expenses_by_category():
    print("View expenses by category:")
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()

    # Create a dictionary to categorize expenses
    categories = {}
    for row in data[1:]:
        name, category, amount = row
        if category not in categories:
            categories[category] = []
        categories[category].append((name, float(amount)))

    # Display the list of categories with corresponding numbers
    for index, category in enumerate(categories.keys(), start=1):
        print(f"{index}: {category}")

    # Allow the user to choose a category to view expenses
    while True:
        category_choice = input("Enter the category number (0 to exit): ")
        if category_choice == "0":
            break
        elif category_choice.isdigit():
            category_choice = int(category_choice)
            if 1 <= category_choice <= len(categories):
                chosen_category = list(categories.keys())[category_choice - 1]
                print(f"Expenses in the category '{chosen_category}':")
                for name, amount in categories[chosen_category]:
                    print(f"  {name}: £{amount:.2f}")
            else:
                print("Invalid category number. Please try again.")
        else:
            print("Invalid input. Please enter a number.")

def expenses_tracker_main():
    print("Welcome to Expense Tracker")
    while True:
        choice = input("Choose an option (1: Enter an expense, 2: View expenses by category, 3: Calculate total expenses by category, 4: Exit): ")
        if choice == "1":
            expense = get_user_expenses()
            save_expenses_to_google_sheet(expense)
        elif choice == "2":
            view_expenses_by_category()
        elif choice == "3":
            calculate_total_expenses_by_category()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

expenses_tracker_main()