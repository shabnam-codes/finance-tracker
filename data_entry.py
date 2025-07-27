from datetime import datetime 
import pandas as pd
categories = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")

    try:
        valid_date = datetime.strptime(date_str, "%d-%m-%Y")
        return valid_date.strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category (Income - 'I' or Expense - 'E'): ").upper()
    if category in categories:
        return categories[category]

    print("Invalid category. Please enter 'I' or 'E'.")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")


def get_transactions(start_date, end_date):
    CSV_FILE = "finance_data.csv"
    FORMAT = "%d-%m-%Y"

    df = pd.read_csv(CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], format=FORMAT)
    start = datetime.strptime(start_date, FORMAT)
    end = datetime.strptime(end_date, FORMAT)

    mask = (df["date"] >= start) & (df["date"] <= end)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
        print("No transactions found in the given date range")
    else:
        print(f"Transactions from {start.strftime(FORMAT)} to {end.strftime(FORMAT)}")
        print(
            filtered_df.to_string(
                index=False, formatters={"date": lambda x: x.strftime(FORMAT)}
            )
        )

    total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
    total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

    print("\nSUMMARY:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Net savings: ${(total_income - total_expense):.2f}")

    return filtered_df

