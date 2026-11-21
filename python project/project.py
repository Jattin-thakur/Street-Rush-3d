import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date


# =========================
# DATABASE
# =========================

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    category TEXT,
    amount REAL
)
""")

conn.commit()


# =========================
# FUNCTIONS
# =========================

def add_expense():
    expense_date = date_entry.get()
    description = description_entry.get()
    category = category_box.get()
    amount = amount_entry.get()

    if description == "" or category == "" or amount == "":
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    cursor.execute("""
    INSERT INTO expenses (date, description, category, amount)
    VALUES (?, ?, ?, ?)
    """, (expense_date, description, category, amount))

    conn.commit()

    clear_entries()
    show_expenses()
    calculate_total()

    messagebox.showinfo("Success", "Expense added successfully!")


def show_expenses():
    # Remove old rows
    for item in expense_table.get_children():
        expense_table.delete(item)

    cursor.execute("""
    SELECT id, date, description, category, amount
    FROM expenses
    ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    for expense in expenses:
        expense_table.insert("", tk.END, values=expense)


def delete_expense():
    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense to delete."
        )
        return

    item = expense_table.item(selected[0])
    expense_id = item["values"][0]

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    show_expenses()
    calculate_total()

    messagebox.showinfo("Deleted", "Expense deleted successfully!")


def calculate_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")

    result = cursor.fetchone()[0]

    if result is None:
        result = 0

    total_label.config(text=f"Total Spending: ₹{result:.2f}")


def clear_entries():
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    category_box.set("Food")

    date_entry.delete(0, tk.END)
    date_entry.insert(0, date.today().strftime("%Y-%m-%d"))


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Expense Tracker")
root.geometry("800x600")
root.resizable(False, False)


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="💰 Expense Tracker",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=15)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(root)

input_frame.pack(pady=10)


# Date

tk.Label(
    input_frame,
    text="Date:"
).grid(row=0, column=0, padx=10, pady=8)

date_entry = tk.Entry(input_frame, width=20)

date_entry.grid(row=0, column=1, padx=10)

date_entry.insert(
    0,
    date.today().strftime("%Y-%m-%d")
)


# Description

tk.Label(
    input_frame,
    text="Description:"
).grid(row=1, column=0, padx=10, pady=8)

description_entry = tk.Entry(
    input_frame,
    width=20
)

description_entry.grid(
    row=1,
    column=1,
    padx=10
)


# Category

tk.Label(
    input_frame,
    text="Category:"
).grid(row=2, column=0, padx=10, pady=8)

categories = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Entertainment",
    "Health",
    "Technology",
    "Other"
]

category_box = ttk.Combobox(
    input_frame,
    values=categories,
    width=17,
    state="readonly"
)

category_box.grid(
    row=2,
    column=1,
    padx=10
)

category_box.set("Food")


# Amount

tk.Label(
    input_frame,
    text="Amount:"
).grid(row=3, column=0, padx=10, pady=8)

amount_entry = tk.Entry(
    input_frame,
    width=20
)

amount_entry.grid(
    row=3,
    column=1,
    padx=10
)


# Add button

add_button = tk.Button(
    input_frame,
    text="➕ Add Expense",
    command=add_expense,
    width=20
)

add_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=15
)


# =========================
# EXPENSE TABLE
# =========================

table_frame = tk.Frame(root)

table_frame.pack(pady=10)


columns = (
    "ID",
    "Date",
    "Description",
    "Category",
    "Amount"
)

expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:
    expense_table.heading(
        column,
        text=column
    )


expense_table.column(
    "ID",
    width=50
)

expense_table.column(
    "Date",
    width=110
)

expense_table.column(
    "Description",
    width=180
)

expense_table.column(
    "Category",
    width=130
)

expense_table.column(
    "Amount",
    width=100
)


expense_table.pack()


# =========================
# DELETE BUTTON
# =========================

delete_button = tk.Button(
    root,
    text="🗑 Delete Selected",
    command=delete_expense,
    width=20
)

delete_button.pack(pady=10)


# =========================
# TOTAL
# =========================

total_label = tk.Label(
    root,
    text="Total Spending: ₹0.00",
    font=("Arial", 18, "bold")
)

total_label.pack(pady=10)


# =========================
# LOAD DATA
# =========================

show_expenses()
calculate_total()


# =========================
# RUN APPLICATION
# =========================

root.mainloop()


# Close database when program ends
conn.close()