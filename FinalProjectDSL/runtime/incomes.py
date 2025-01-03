import tkinter as tk
from tkinter import ttk, messagebox, Listbox, END, simpledialog
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ruta a la base de datos de reglas
db_path = '../src/finance_rules.db'

# Ruta a la base de datos del usuario
db_user_path = 'user_data.db'

# Función para obtener las reglas relacionadas con Income
def get_income_rules():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener configuraciones de campos de ingresos
    cursor.execute("SELECT field_name, visible, required FROM income_field_settings")
    field_settings = {row[0]: {'visible': row[1] == 'yes', 'required': row[2] == 'yes'} for row in cursor.fetchall()}

    # Obtener configuraciones de botones
    cursor.execute("SELECT button_name, visible, text FROM button_settings")
    button_settings = {row[0]: {'visible': row[1] == 'yes', 'text': row[2]} for row in cursor.fetchall()}

    # Obtener configuraciones de visualización
    cursor.execute("SELECT visible_fields, sort_by, sort_order FROM income_display_settings")
    display_settings = cursor.fetchone()
    visible_fields = display_settings[0].split(', ') if display_settings else []
    sort_by = display_settings[1] if display_settings else 'start_date'
    sort_order = display_settings[2] if display_settings else 'asc'

    conn.close()

    return {
        'field_settings': field_settings,
        'button_settings': button_settings,
        'visible_fields': visible_fields,
        'sort_by': sort_by,
        'sort_order': sort_order
    }

# Función para obtener categorías y frecuencias
def get_categories_and_frequencies():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM income_category")
    categories = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM income_frequency")
    frequencies = [row[0] for row in cursor.fetchall()]

    conn.close()
    return categories, frequencies

# Función para inicializar la base de datos del usuario y crear la tabla incomes
def initialize_user_db():
    conn = sqlite3.connect(db_user_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name TEXT,
            category TEXT,
            frequency TEXT,
            amount REAL,
            start_date TEXT,
            end_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

initialize_user_db()

# Función para guardar ingresos en la base de datos del usuario
def save_income(source_name, amount, frequency, start_date, end_date, category, entry_income_source, entry_income_amount, combo_income_frequency, entry_income_start_date, entry_income_end_date, combo_income_category, listbox):
    if not source_name or not amount or not frequency or not start_date or not category:
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return

    try:
        amount = float(amount)
        datetime.strptime(start_date, "%Y-%m-%d")  # Validate date format
        if end_date:
            datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Check the date format and amount.")
        return

    conn = sqlite3.connect(db_user_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO incomes (source_name, category, frequency, amount, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source_name, category, frequency, amount, start_date, end_date))
    conn.commit()

    # Print the contents of the incomes table
    cursor.execute('SELECT * FROM incomes')
    print("Contents of incomes table:")
    for row in cursor.fetchall():
        print(row)

    conn.close()
    messagebox.showinfo("Success", "Income added successfully!")

    # Clear inputs
    entry_income_source.delete(0, END)
    entry_income_amount.delete(0, END)
    combo_income_frequency.set('')
    entry_income_start_date.delete(0, END)
    entry_income_end_date.delete(0, END)
    combo_income_category.set('')

    # Fetch dynamic display rules from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT visible_fields, sort_by, sort_order FROM income_display_settings WHERE setting_key = "income_display"')
    display_settings = cursor.fetchone()
    conn.close()

    if display_settings:
        visible_fields = display_settings[0].split(', ')  # Convert visible fields to a list
        sort_by = display_settings[1]
        sort_order = display_settings[2]
        # Refresh the incomes list dynamically
        display_incomes(listbox, visible_fields, sort_by, sort_order)
    else:
        messagebox.showerror("Error", "Display settings not found in the rules.")


# Función para mostrar ingresos en la lista
def display_incomes(listbox, visible_fields, sort_by, sort_order):
    listbox.delete(0, END)
    conn = sqlite3.connect(db_user_path)
    cursor = conn.cursor()

    # Obtener los ingresos y ordenarlos
    query = f"SELECT {', '.join(visible_fields)} FROM incomes ORDER BY {sort_by} {'DESC' if sort_order == 'desc' else 'ASC'}"
    cursor.execute(query)
    incomes = cursor.fetchall()

    for income in incomes:
        display_text = ' | '.join(f"{field.capitalize()}: {value}" for field, value in zip(visible_fields, income))
        listbox.insert(END, display_text)

    conn.close()

def delete_income(listbox):
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select an income to delete.")
        return

    # Get selected income
    selected_text = listbox.get(selected_index)
    source_name = selected_text.split(' | ')[0].split(": ")[1]  # Extract source_name from the displayed text

    # Confirm deletion
    response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this income?")
    if response:
        # Delete income from the database
        conn = sqlite3.connect(db_user_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM incomes WHERE source_name = ?', (source_name,))
        conn.commit()
        conn.close()

        # Refresh the listbox
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT visible_fields, sort_by, sort_order FROM income_display_settings WHERE setting_key = "income_display"')
        display_settings = cursor.fetchone()
        conn.close()

        if display_settings:
            visible_fields = display_settings[0].split(', ')
            sort_by = display_settings[1]
            sort_order = display_settings[2]
            display_incomes(listbox, visible_fields, sort_by, sort_order)
        else:
            listbox.delete(0, END)  # Clear the listbox if no display rules are found

        messagebox.showinfo("Success", "Income deleted successfully!")
def edit_income(listbox):
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select an income to edit.")
        return

    selected_text = listbox.get(selected_index)
    source_name = selected_text.split(' | ')[0].split(": ")[1]  # Extract the source_name

    # Fetch the income data
    conn = sqlite3.connect(db_user_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incomes WHERE source_name = ?", (source_name,))
    income = cursor.fetchone()
    conn.close()

    if not income:
        messagebox.showerror("Error", "Income not found.")
        return

    # Fetch available categories and frequencies
    categories, frequencies = get_categories_and_frequencies()

    # Create a new window for editing
    edit_window = tk.Toplevel()
    edit_window.title("Edit Income")
    edit_window.geometry("400x400")

    # Create entry fields dynamically
    fields = ['source_name', 'category', 'frequency', 'amount', 'start_date', 'end_date']
    entries = {}
    for idx, field in enumerate(fields):
        tk.Label(edit_window, text=field.replace('_', ' ').capitalize()).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        if field == 'category':
            combo_category = ttk.Combobox(edit_window, values=categories, width=27)
            combo_category.grid(row=idx, column=1, padx=10, pady=5)
            combo_category.set(income[idx + 1])  # Skip the ID column
            entries[field] = combo_category
        elif field == 'frequency':
            combo_frequency = ttk.Combobox(edit_window, values=frequencies, width=27)
            combo_frequency.grid(row=idx, column=1, padx=10, pady=5)
            combo_frequency.set(income[idx + 1])  # Skip the ID column
            entries[field] = combo_frequency
        else:
            entry = tk.Entry(edit_window, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry.insert(0, income[idx + 1])  # Skip the ID column
            entries[field] = entry

    # Save Changes Button
    def save_changes():
        updated_values = {field: entry.get() for field, entry in entries.items()}
        try:
            updated_values['amount'] = float(updated_values['amount'])
            datetime.strptime(updated_values['start_date'], "%Y-%m-%d")
            if updated_values['end_date']:
                datetime.strptime(updated_values['end_date'], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Check the date format and amount.")
            return

        # Update database
        conn = sqlite3.connect(db_user_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE incomes
            SET source_name = ?, category = ?, frequency = ?, amount = ?, start_date = ?, end_date = ?
            WHERE id = ?
        ''', (*updated_values.values(), income[0]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Income updated successfully!")
        edit_window.destroy()

        # Refresh listbox
        rules = get_income_rules()
        display_incomes(listbox, rules['visible_fields'], rules['sort_by'], rules['sort_order'])

    tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(fields), column=1, pady=10)


def generate_report():
    # Pedir al usuario que seleccione el tipo de reporte
    report_type = simpledialog.askstring("Generate Report", "Enter report type (annual, monthly, weekly, daily):")
    if report_type not in ['annual', 'monthly', 'weekly', 'daily']:
        messagebox.showerror("Error", "Invalid report type. Please enter 'annual', 'monthly', 'weekly', or 'daily'.")
        return

    # Conectar a la base de datos y obtener los datos de ingresos
    conn = sqlite3.connect(db_user_path)
    cursor = conn.cursor()
    cursor.execute('SELECT source_name, amount, start_date FROM incomes')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("Info", "No income data available for reporting.")
        return

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data, columns=['Source Name', 'Amount', 'Start Date'])
    df['Start Date'] = pd.to_datetime(df['Start Date'])

    # Generar el reporte según el tipo solicitado
    if report_type == 'annual':
        # Crear una serie de años desde 2020 hasta 2025
        years = pd.Series(range(2020, 2026))
        # Agrupar los ingresos por año
        report = df.groupby(df['Start Date'].dt.year)['Amount'].sum()
        # Reindexar para incluir todos los años y llenar los valores faltantes con cero
        report = report.reindex(years, fill_value=0)
        report_title = "Annual Income Report (2020-2025)"
    elif report_type == 'monthly':
        # Crear un rango de meses para todo el año 2024
        full_months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='MS').to_period('M')

        # Agrupar los ingresos por mes
        report = df.groupby(df['Start Date'].dt.to_period('M'))['Amount'].sum()

        # Reindexar para incluir todos los meses del rango y llenar los valores faltantes con cero
        report = report.reindex(full_months, fill_value=0)

        report_title = "Monthly Income Report"
        report.index = report.index.to_timestamp()  # Convertir a timestamps para el gráfico
    elif report_type == 'weekly':
        report = df.groupby(df['Start Date'].dt.to_period('W'))['Amount'].sum()
        report_title = "Weekly Income Report"
        report.index = report.index.to_timestamp()
        report = report[-4:]  # Mostrar solo las últimas 4 semanas
    elif report_type == 'daily':
        # Obtener los últimos 10 días
        today = pd.Timestamp.today()
        date_range = pd.date_range(end=today, periods=10)
        # Agrupar los ingresos por fecha
        report = df.groupby(df['Start Date'].dt.date)['Amount'].sum()
        # Reindexar para incluir todos los días y llenar los valores faltantes con cero
        report = report.reindex(date_range.date, fill_value=0)
        report_title = "Daily Income Report (Last 10 Days)"

    # Mostrar el reporte en una nueva ventana
    report_window = tk.Toplevel()
    report_window.title(report_title)
    report_window.geometry("800x600")  # Ajustar el tamaño de la ventana

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))  # Ajustar el tamaño del gráfico
    ax.plot(report.index, report.values, marker='o')
    ax.set_title(report_title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amount ($)')
    ax.grid(True)

    # Formatear las etiquetas del eje X según el tipo de reporte
    if report_type == 'daily' or report_type == 'weekly':
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
    elif report_type == 'monthly':
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
    elif report_type == 'annual':
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Insertar el gráfico en la ventana de reportes
    canvas = FigureCanvasTkAgg(fig, master=report_window)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')


# Función para crear la pestaña de ingresos
def create_incomes_tab(tab):
    rules = get_income_rules()
    categories, frequencies = get_categories_and_frequencies()

    field_settings = rules['field_settings']
    button_settings = rules['button_settings']

    # Create widgets dynamically based on rules
    row = 0

    if field_settings.get('income_source_name', {}).get('visible', False):
        tk.Label(tab, text="Source Name:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry_income_source = tk.Entry(tab, width=30)
        entry_income_source.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    if field_settings.get('income_category', {}).get('visible', False):
        tk.Label(tab, text="Category:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        combo_income_category = ttk.Combobox(tab, values=categories, width=27)
        combo_income_category.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    if field_settings.get('income_frequency', {}).get('visible', False):
        tk.Label(tab, text="Frequency:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        combo_income_frequency = ttk.Combobox(tab, values=frequencies, width=27)
        combo_income_frequency.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    if field_settings.get('income_start_date', {}).get('visible', False):
        tk.Label(tab, text="Start Date (YYYY-MM-DD):").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry_income_start_date = tk.Entry(tab, width=30)
        entry_income_start_date.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    if field_settings.get('income_end_date', {}).get('visible', False):
        tk.Label(tab, text="End Date (YYYY-MM-DD):").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry_income_end_date = tk.Entry(tab, width=30)
        entry_income_end_date.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    if field_settings.get('income_amount', {}).get('visible', False):
        tk.Label(tab, text="Amount:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry_income_amount = tk.Entry(tab, width=30)
        entry_income_amount.grid(row=row, column=1, padx=10, pady=5)
        row += 1

    # Add Income Button
    if button_settings.get('add_income_button', {}).get('visible', False):
        btn_text = button_settings['add_income_button']['text']
        tk.Button(tab, text=btn_text, command=lambda: save_income(
            entry_income_source.get(),
            entry_income_amount.get(),
            combo_income_frequency.get(),
            entry_income_start_date.get(),
            entry_income_end_date.get(),
            combo_income_category.get(),
            entry_income_source,
            entry_income_amount,
            combo_income_frequency,
            entry_income_start_date,
            entry_income_end_date,
            combo_income_category,
            income_listbox
        )).grid(row=row, column=1, pady=10)
        row += 1

    # Income Listbox
    income_listbox = Listbox(tab, width=80, height=10)
    income_listbox.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

    # Display incomes dynamically in the listbox
    display_incomes(income_listbox, rules['visible_fields'], rules['sort_by'], rules['sort_order'])
    row += 1

    # Add Buttons (Edit, Delete, Generate Report) dynamically
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT visible, text FROM button_settings WHERE button_name = "delete_income_button"')
    delete_button_settings = cursor.fetchone()
    cursor.execute('SELECT visible, text FROM button_settings WHERE button_name = "edit_income_button"')
    edit_button_settings = cursor.fetchone()
    cursor.execute('SELECT visible, text, report_types FROM report_button_settings WHERE button_name = "generate_report_button"')
    report_button_settings = cursor.fetchone()
    conn.close()

    button_frame = tk.Frame(tab)
    button_frame.grid(row=row, column=0, columnspan=2, pady=10)

    if edit_button_settings and edit_button_settings[0] == 'yes':
        edit_button_text = edit_button_settings[1] if edit_button_settings[1] else "Edit Income"
        tk.Button(button_frame, text=edit_button_text, command=lambda: edit_income(income_listbox)).pack(side="left", padx=5)

    if delete_button_settings and delete_button_settings[0] == 'yes':
        delete_button_text = delete_button_settings[1] if delete_button_settings[1] else "Delete Income"
        tk.Button(button_frame, text=delete_button_text, command=lambda: delete_income(income_listbox)).pack(side="left", padx=5)

    if report_button_settings and report_button_settings[0] == 'yes':
        report_button_text = report_button_settings[1] if report_button_settings[1] else "Generate Report"
        report_types = report_button_settings[2].split(', ') if report_button_settings[2] else []
        tk.Button(button_frame, text=report_button_text, command=generate_report).pack(side="left", padx=5)

