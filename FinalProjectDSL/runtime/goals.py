import tkinter as tk
from tkinter import messagebox

def create_goals_tab(tab):
    """Función para crear la pestaña de Goals."""
    tk.Label(tab, text="Goals Section", font=("Helvetica", 16)).pack(pady=10)
    # Aquí puedes agregar el contenido específico para metas
    # Ejemplo de botón y campo de entrada:
    tk.Label(tab, text="Goal Description:").pack()
    entry_goal_description = tk.Entry(tab, width=30)
    entry_goal_description.pack()

    tk.Label(tab, text="Target Amount:").pack()
    entry_goal_amount = tk.Entry(tab, width=30)
    entry_goal_amount.pack()

    tk.Button(tab, text="Add Goal", command=lambda: messagebox.showinfo("Info", "Goal added")).pack(pady=10)
