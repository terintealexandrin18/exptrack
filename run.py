# Import necessary modules
import gspread
import calendar
import datetime
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load Google Sheets credentials from the service account file
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Expense Tracker')

# Initialize global variables
monthly_budget = 0
total_spent = 0

# ANSI escape codes for text color
BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Function to print ASCII art from a file


def print_ascii_art(file_path):
    """
    Function to change the text style
    """
    try:
        with open(file_path, 'r') as file:
            ascii_art = file.read()
            print(ascii_art)
    except FileNotFoundError:
        print("ASCII art file not found.")

# Functions to apply ANSI escape codes for text color


def blue(text):
    """
    Function to transform the text to color blue.
    """
    return f"{BLUE}{text}{RESET}"


def red(text):
    """
    Function transform the text to color red
    """
    return f"\033[91m{text}\033[0m"


def green(text):
    """
    Function to transform the text to color green.
    """
    return f"{GREEN}{text}{RESET}"

# Define Expense class


class Expense:
    def __init__(self, name, category, amount) -> None:
        """
        Create an Expense object with a name, category, and amount.
        """
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        """
        Return a string representation of the Expense object
        """
        return f"Expense: {self.name}, {self.category}, £{self.amount:.2f}"

# Function to remove commas from input string


def remove_commas(input_str):
    """
    Remove commas from the input string.
    Will return the input string with commas removed.
    """
    return input_str.replace(',', '')

# Function to check if the input string contains only letters and spaces


def is_valid_input(input_str):
    """
    Check if the input string contains only letters and spaces.
    """
    return input_str.strip() and all(
        c.isalpha() or c.isspace() for c in input_str
    )

# Function to get user input for expense details and return an Expense object


def get_user_expenses():
    """
    Get user input for expense details (name, category, amount) and
    return an Expense object.
    """
    while True:
        name_of_expense = input(blue("Enter your expense name: "))
        if is_valid_input(name_of_expense):
            break

        else:
            print(green("Invalid input. Please enter a valid expense name "
                  "(only letters and spaces allowed)."))

    while True:
        amount_of_expense = input(blue("Enter the expense amount: ") + "£")
        amount_of_expense = remove_commas(amount_of_expense)

        try:
            amount_of_expense = float(amount_of_expense)
            break

        except ValueError:
            print(green("Invalid input. Please enter a valid number "
                  "(e.g. 1200.50, 5, 7.23)."))

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
                input(f"Enter one of the category "
                      f"numbers: {range_of_value}")) - 1

            if select_index_value in range(len(category_expense)):
                chosen_category = category_expense[select_index_value]
                new_expense = Expense(name=name_of_expense,
                                      category=chosen_category,
                                      amount=amount_of_expense)
                return new_expense

            else:
                print(green("Invalid category. Please try again."))

        except ValueError:
            print(green("Invalid input. Please enter a valid number."))


# Function to save an expense to the Google Sheets document


def save_expenses_to_google_sheet(expense_store):
    """
    Save an expense to the Google Sheets document.
    """
    try:
        global total_spent
        expense_dict = {
            "name": expense_store.name,
            "category": expense_store.category,
            "amount": expense_store.amount
        }

        page1_worksheet = SHEET.worksheet("page1")
        page1_worksheet.append_row([
            expense_dict["name"],
            expense_dict["category"],
            expense_dict["amount"]])
        total_spent += expense_store.amount
        print("Saved successfully.🤗")

    except Exception as e:
        print(green(f"An error occurred while saving: {str(e)}"))

# Function to calculate and display total expenses by category


def calculate_total_expenses_by_category():
    """
    Calculate and display total expenses by category.
    """
    try:
        print("Calculating total expenses by category:")
        page1_worksheet = SHEET.worksheet("page1")
        data = page1_worksheet.get_all_values()

        if len(data) < 2:
            print("No expenses found.")

        categories_total = {}
        # Start iterating from the second row (index 1) to include row 2
        for row in data[1:]:
            if len(row) >= 3:
                category, amount = row[1], row[2]

                if category not in categories_total:
                    categories_total[category] = 0
                categories_total[category] += float(amount)

            else:
                print(green(f"Skipping row: {row} - Expected 3 values in "
                      f"each row, found {len(row)}"))

        if not categories_total:
            print(green("No valid expenses found in categories."))

        else:
            for category, total_amount in categories_total.items():
                print(f"{category}: \033[94m£{total_amount:.2f}\033[0m")

    except Exception as e:
        print(green(f"An error occurred while calculating expenses "
              f"by category: {str(e)}"))

# Function to view expenses by category


def view_expenses_by_category():
    """
    View expenses by category and allow the user to select a category
    to display expenses within that category.
    """
    print("View expenses by category:")
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()

    categories = {}
    for row in data[1:]:
        name, category, amount = row

        if category not in categories:
            categories[category] = []
        categories[category].append((name, float(amount)))

    for index, category in enumerate(categories.keys(), start=1):
        print(f"{index}: {category}")

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
                    print(blue(f"  {name}: £{amount:.2f}"))

            else:
                print(green("Invalid category number. Please try again."))

        else:
            print(green("Invalid input. Please enter a number."))


# Function to calculate and display the total amount spent this month


def total_amount_spent():
    """
    Calculate and display the total amount spent this month.
    """
    print("\nView total amount spent this month:")
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()
    global total_spent
    total_spent = 0

    # Start iterating from the second row (index 1) to include row 2
    for row in data[1:]:
        amount = float(row[2])
        total_spent += amount

    else:
        print(f"Total amount spent: \033[94m£{total_spent:.2f}\033[0m")


# Function to set up the user's monthly budget


def set_up_monthly_budget():
    """
    Set up the user's monthly budget.
    """
    global monthly_budget
    try:
        monthly_budget = float(input(blue("Enter monthly budget: ") + "£"))

        if monthly_budget < 0:
            print(green("Monthly budget cannot be negative. "
                  "Please enter a valid budget."))
            return set_up_monthly_budget()
        return monthly_budget

    except ValueError:
        print(green("Invalid input. Please enter a valid numeric value."))
        return set_up_monthly_budget()


# Function to calculate and return the total amount spent this month


def calculate_total_spent():
    """
    Calculate and return the total amount spent this month.
    """
    global total_spent
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()
    total_spent = 0
    for row in data[2:]:
        amount = float(row[2])
        total_spent += amount


# Function to calculate and display the monthly budget left and daily budget


def monthly_budget_left():
    """
    Calculate and display the monthly budget left and daily budget.
    """
    if monthly_budget == 0:
        print(green("Please set up a monthly budget to view the budget left."))

    else:
        budget_left = monthly_budget - total_spent

        # Time and days
        now = datetime.datetime.now()
        days_in_the_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_the_month - now.day
        daily_budget = budget_left / remaining_days

        if budget_left < 0:
            savings_covered = total_spent - monthly_budget
            print(red(f"⚠ Warning ⚠\nYour budget of ") +
                  f"\033[94m£{monthly_budget:.2f}\033[0m" +
                  red(f" is smaller than your total spent of") +
                  f"\033[94m£{total_spent:.2f}\033[0m" + red("."))
            print(red("You've taken ") + f"\033[94m£{savings_covered:.2f}"
                  f"\033[0m" + red(" from your savings to cover the deficit."))

        else:
            print(f"Monthly Budget is: \033[94m£{monthly_budget:.2f}\033[0m")
            print(f"Monthly budget left: \033[94m£{budget_left:.2f}\033[0m")
            print(f"Budget per day left: \033[94m£{daily_budget:.2f}\033[0m")


# Function to clear all expenses data in the Google Sheet, excluding
# the first row


def clear_expenses_data():
    """
    Clear all expenses data in the Google Sheet, excluding the first row.
    """
    try:
        page1_worksheet = SHEET.worksheet("page1")
        num_rows = len(page1_worksheet.get_all_values())

        if num_rows > 1:
            for _ in range(num_rows - 1):
                page1_worksheet.delete_rows(2)

    except Exception as e:
        print(green(f"An error occurred while clearing "
                    f"expenses data: {str(e)}"))


# Main function to run the Expense Tracker application


def expenses_tracker_main():
    """
    Main function to run the Expense Tracker application.
    """
    try:
        clear_expenses_data()
        calculate_total_spent()
        ascii_art_file_path = 'ascii-text-art.txt'
        print_ascii_art(ascii_art_file_path)
        print(red(f"With Expense Tracker, you can easily manage and monitor "
                  f"your spending."))
        print(red(f"You can add your daily expenses, view expenses by "
                  f"category, calculate totals,"))
        print(red("set up a monthly budget, and track your budget status."))
        print(red("Let's start tracking your expenses!\n"))

        while True:
            print("\nChoose an option:")
            print("  1: Add an Expense")
            print("  2: View Expenses by Category")
            print("  3: Calculate Total Expenses by Category")
            print("  4: View Total Amount Spent This Month")
            print("  5: Set Up Monthly Budget")
            print("  6: View Monthly Budget Status")
            print("  7: Exit")

            choice = input(blue("\nPlease select an option: "))

            if choice == "1":
                expense = get_user_expenses()
                save_expenses_to_google_sheet(expense)
            elif choice == "2":
                view_expenses_by_category()
            elif choice == "3":
                calculate_total_expenses_by_category()
            elif choice == "4":
                total_amount_spent()
            elif choice == "5":
                set_up_monthly_budget()
            elif choice == "6":
                monthly_budget_left()
            elif choice == "7":
                print(blue("\nGoodbye!"))
                break
            else:
                print(green("\nInvalid choice. Please try again."))
    except Exception as e:
        print(green(f"An error occurred: {str(e)}"))


# Run the main function to start the Expense Tracker application


expenses_tracker_main()
