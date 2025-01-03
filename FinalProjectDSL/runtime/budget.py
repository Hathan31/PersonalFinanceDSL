import tkinter as tk
from tkinter import messagebox

def create_budget_tab(tab):
    """Función para crear la pestaña de Budget."""
    tk.Label(tab, text="Budget Section", font=("Helvetica", 16)).pack(pady=10)
    # Aquí puedes agregar el contenido específico para presupuestos
    # Ejemplo de botón y campo de entrada:
    tk.Label(tab, text="Budget Category:").pack()
    entry_budget_category = tk.Entry(tab, width=30)
    entry_budget_category.pack()

    tk.Label(tab, text="Amount:").pack()
    entry_budget_amount = tk.Entry(tab, width=30)
    entry_budget_amount.pack()

    tk.Button(tab, text="Add Budget", command=lambda: messagebox.showinfo("Info", "Budget added")).pack(pady=10)
