import gspread
import calendar
import datetime
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

# Initialize global variables
monthly_budget = 0
total_spent = 0


class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Expense: {self.name}, {self.category}, £{self.amount:.2f}"


def remove_commas(input_str):
    return input_str.replace(',', '')


def get_user_expenses():
    print(f" 🖍 Getting user expenses")
    name_of_expense = input("Enter your expense: ")
    while True:
        amount_of_expense = input("Enter the expense amount: ")
        amount_of_expense = remove_commas(amount_of_expense)

        try:
            amount_of_expense = float(amount_of_expense)
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
    print(f" 📌 Saving User {expense_store}")
    expense_dict = {
        "name": expense_store.name,
        "category": expense_store.category,
        "amount": expense_store.amount
    }

    page1_worksheet = SHEET.worksheet("page1")
    page1_worksheet.append_row([expense_dict["name"],
                                expense_dict["category"], expense_dict["amount"]])
    print("Saved successfully.🤗")


def calculate_total_expenses_by_category():
    print("Calculating total expenses by category:")
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()

    categories_total = {}
    for row in data[1:]:
        name, category, amount = row
        if category not in categories_total:
            categories_total[category] = 0
        categories_total[category] += float(amount)

    for category, total_amount in categories_total.items():
        print(f"{category}: £{total_amount:.2f}")


def view_expenses_by_category():
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
                    print(f"  {name}: £{amount:.2f}")
            else:
                print("Invalid category number. Please try again.")
        else:
            print("Invalid input. Please enter a number.")


def total_amount_spent():
    print("View total amount spent this month:")
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()
    global total_spent
    total_spent = 0
    for row in data[2:]:
        amount = float(row[2])
        total_spent += amount
    else:
        print(f"Total amount spent: £{total_spent:.2f}")


def set_up_monthly_budget():
    global monthly_budget, total_spent
    try:
        monthly_budget = float(input("Enter your monthly budget: £"))

        # Calculate total spent when setting up the monthly budget
        total_spent = calculate_total_spent()

        return monthly_budget
    except ValueError:
        print("Invalid input. Please enter a valid numeric value.")
        return set_up_monthly_budget()


def calculate_total_spent():
    global total_spent
    page1_worksheet = SHEET.worksheet("page1")
    data = page1_worksheet.get_all_values()
    total_spent = 0
    for row in data[2:]:
        amount = float(row[2])
        total_spent += amount
    return total_spent


def monthly_budget_left():
    if monthly_budget == 0:
        print("Please set up a monthly budget to view the budget left.")
    else:
        budget_left = monthly_budget - total_spent

        now = datetime.datetime.now()
        days_in_the_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_the_month - now.day
        daily_budget = budget_left / remaining_days
        print(f"Monthly budget left: £{budget_left:.2f}, Budget per day left: £{daily_budget:.2f}")

    
def expenses_tracker_main():
    calculate_total_spent()
    print("\nWelcome to Expense Tracker")

    while True:
        print("\nChoose an option:")
        print("  1: Enter an expense")
        print("  2: View expenses by category")
        print("  3: Calculate total expenses by category")
        print("  4: Total amount spent this month")
        print("  5: Set up monthly budget")
        print("  6: View the monthly budget left")
        print("  7: Exit")

        choice = input("\nPlease select an option: ")

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
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

expenses_tracker_main()