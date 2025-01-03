import matplotlib
import pandas
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from incomes import create_incomes_tab
from expenses import create_expenses_tab
from budget import create_budget_tab
from goals import create_goals_tab

# Ruta a la base de datos de reglas
db_path = '../src/finance_rules.db'

def check_rules():  
    """Lee las reglas de la base de datos y verifica el estado de inicialización y las ventanas habilitadas."""
    try:
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)  # Solo lectura
        cursor = conn.cursor()

        # Verificar si el runtime fue inicializado
        cursor.execute("SELECT setting_value FROM general_settings WHERE setting_key = 'initialize_runtime'")
        initialized = cursor.fetchone()
        initialized = initialized[0] == 'yes' if initialized else False

        # Leer todas las ventanas habilitadas desde general_settings
        cursor.execute(
            "SELECT setting_key, setting_value FROM general_settings WHERE setting_key LIKE 'enable_window_%'")
        enabled_windows_data = cursor.fetchall()

        # Construir el diccionario de ventanas habilitadas
        enabled_windows = {row[0].replace("enable_window_", ""): row[1] for row in enabled_windows_data if
                           row[1] == 'yes'}

        # Debug: Imprimir el estado de inicialización y las ventanas habilitadas
        print("Runtime initialized:", initialized)
        print("Enabled windows:", enabled_windows)

        conn.close()
        return initialized, enabled_windows
    except sqlite3.OperationalError as e:
        print(f"Error accessing database: {e}")
        return False, {}


def main():
    initialized, enabled_windows = check_rules()

    if not initialized:
        messagebox.showwarning("Warning", "Runtime not initialized. Please check your settings.")
        return

    # Crear la ventana principal del runtime
    root = tk.Tk()
    root.title("Personal Finance Runtime")
    root.geometry("800x600")

    # Crear el control de pestañas
    tab_control = ttk.Notebook(root)

    # Crear las pestañas basadas en las reglas de enabled_windows
    if enabled_windows.get('incomes') == 'yes':
        incomes_tab = ttk.Frame(tab_control)
        create_incomes_tab(incomes_tab)
        tab_control.add(incomes_tab, text="Incomes")
        print("Incomes tab added.")

    if enabled_windows.get('expenses') == 'yes':
        expenses_tab = ttk.Frame(tab_control)
        create_expenses_tab(expenses_tab)
        tab_control.add(expenses_tab, text="Expenses")
        print("Expenses tab added.")

    if enabled_windows.get('budget') == 'yes':
        budget_tab = ttk.Frame(tab_control)
        create_budget_tab(budget_tab)
        tab_control.add(budget_tab, text="Budget")
        print("Budget tab added.")

    if enabled_windows.get('goals') == 'yes':
        goals_tab = ttk.Frame(tab_control)
        create_goals_tab(goals_tab)
        tab_control.add(goals_tab, text="Goals")
        print("Goals tab added.")

    # Empacar las pestañas y comenzar el loop principal de la GUI
    tab_control.pack(expand=1, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()
