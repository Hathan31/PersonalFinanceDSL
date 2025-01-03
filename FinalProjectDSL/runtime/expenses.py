import tkinter as tk

def create_expenses_tab(tab):
    tk.Label(tab, text="Expenses Section", font=("Arial", 18)).pack(pady=10)
    tk.Label(tab, text="Source Name:").pack()
    tk.Entry(tab, width=30).pack()
    tk.Label(tab, text="Amount:").pack()
    tk.Entry(tab, width=30).pack()
    tk.Button(tab, text="Add Expense").pack(pady=10)

