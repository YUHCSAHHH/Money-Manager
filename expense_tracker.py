import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

FILE = "expenses.json"


# ---------------------------
# Utility Functions
# ---------------------------

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def line():
    print("\n" + "="*40)


# ---------------------------
# Add Expense
# ---------------------------

def add_expense():

    line()
    print("ADD EXPENSE")

    date = input("Date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        print("Invalid date format")
        return

    categories = ["Food", "Travel", "Shopping", "Bills", "Others"]

    print("\nSelect Category")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    try:
        choice = int(input("Choice: "))
        category = categories[choice-1]
    except:
        print("Invalid category")
        return

    try:
        amount = float(input("Amount (₹): "))
    except:
        print("Invalid amount")
        return

    data = load_data()

    data.append({
        "Date": date,
        "Category": category,
        "Amount": amount
    })

    save_data(data)

    print("Expense saved successfully!")


# ---------------------------
# View Expenses
# ---------------------------

def view_expenses():

    line()
    print("EXPENSE HISTORY")

    data = load_data()

    if not data:
        print("No expenses recorded yet")
        return

    df = pd.DataFrame(data)

    df["Amount"] = df["Amount"].map(lambda x: f"₹{x}")

    print()
    print(df.to_string(index=False))


# ---------------------------
# Category Pie Chart
# ---------------------------

def category_chart():

    data = load_data()

    if not data:
        print("No data available")
        return

    df = pd.DataFrame(data)

    category_sum = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(7,7))

    colors = ["#FF9999", "#66B3FF", "#99FF99", "#FFD580", "#C2C2F0"]

    category_sum.plot(
        kind="pie",
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        pctdistance=0.75,
        labeldistance=1.15
    )

    plt.title("Expense Distribution by Category")
    plt.ylabel("")
    plt.tight_layout()

    plt.show()


# ---------------------------
# Monthly Chart
# ---------------------------

def monthly_chart():

    data = load_data()

    if not data:
        print("No data available")
        return

    df = pd.DataFrame(data)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    monthly_sum = df.groupby("Month")["Amount"].sum().sort_index()

    display_values = monthly_sum / 10

    plt.figure(figsize=(8,5))

    bars = plt.bar(display_values.index, display_values.values)

    plt.title("Monthly Expenses (Scaled for Visibility)")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹ / 10)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    for bar, value in zip(bars, monthly_sum.values):
        plt.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height(),
            f"₹{value}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.show()


# ---------------------------
# Total Expense
# ---------------------------

def total_expense():

    data = load_data()

    if not data:
        print("No expenses recorded")
        return

    df = pd.DataFrame(data)

    total = df["Amount"].sum()

    line()
    print(f"TOTAL EXPENSES: ₹{total}")


# ---------------------------
# Menu
# ---------------------------

def menu():

    while True:

        line()
        print("PERSONAL EXPENSE TRACKER")
        line()

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category Chart")
        print("4. Monthly Chart")
        print("5. Total Expense")
        print("6. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            category_chart()

        elif choice == "4":
            monthly_chart()

        elif choice == "5":
            total_expense()

        elif choice == "6":
            print("Exiting program...")
            break

        else:
            print("Invalid choice")


menu()
