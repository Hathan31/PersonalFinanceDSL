import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, Listbox, END
import sqlite3
from dsl_parser import (
    parse_dsl,
    save_general_setting,
    save_income_field_setting,
    save_expense_field_setting,  # Added for expenses
    save_button_setting,
    save_report_button_setting,
    save_income_display_setting,
    save_income_category_to_db,
    save_income_frequency_to_db,
    print_table_data
)

# Path to the SQLite database
db_path = 'finance_rules.db'

def display_rules():
    """Displays organized rules from SQLite in the listbox."""
    rules_listbox.delete(0, END)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Display general_settings
    cursor.execute('SELECT setting_key, setting_value FROM general_settings')
    general_settings = cursor.fetchall()
    if general_settings:
        rules_listbox.insert(END, "General Settings:")
        for setting_key, setting_value in general_settings:
            rules_listbox.insert(END, f"{setting_key.replace('_', ' ').capitalize()}: {setting_value}")

    # Display income_field_settings
    cursor.execute('SELECT field_name, visible, required FROM income_field_settings')
    income_fields = cursor.fetchall()
    if income_fields:
        rules_listbox.insert(END, "Income Field Settings:")
        for field_name, visible, required in income_fields:
            rules_listbox.insert(END, f"{field_name.replace('_', ' ').capitalize()} {{ visible: {visible}, required: {required} }}")

    # Display expense_field_settings (NEW for expenses)
    cursor.execute('SELECT field_name, visible, required FROM expense_field_settings')
    expense_fields = cursor.fetchall()
    if expense_fields:
        rules_listbox.insert(END, "Expense Field Settings:")
        for field_name, visible, required in expense_fields:
            rules_listbox.insert(END, f"{field_name.replace('_', ' ').capitalize()} {{ visible: {visible}, required: {required} }}")

    # Display button_settings
    cursor.execute('SELECT button_name, visible, text FROM button_settings')
    buttons = cursor.fetchall()
    if buttons:
        rules_listbox.insert(END, "Button Settings:")
        for button_name, visible, text in buttons:
            rules_listbox.insert(END, f"{button_name.replace('_', ' ').capitalize()} {{ visible: {visible}, text: {text} }}")

    # Display report_button_settings
    cursor.execute('SELECT button_name, visible, text, report_types FROM report_button_settings')
    report_buttons = cursor.fetchall()
    if report_buttons:
        rules_listbox.insert(END, "Report Button Settings:")
        for button_name, visible, text, report_types in report_buttons:
            rules_listbox.insert(END, f"{button_name.replace('_', ' ').capitalize()} {{ visible: {visible}, text: {text}, report_types: {report_types} }}")

    # Display income_display_settings
    cursor.execute('SELECT setting_key, visible_fields, sort_by, sort_order FROM income_display_settings')
    income_display = cursor.fetchall()
    if income_display:
        rules_listbox.insert(END, "Income Display Settings:")
        for setting_key, visible_fields, sort_by, sort_order in income_display:
            rules_listbox.insert(END, f"{setting_key.replace('_', ' ').capitalize()} {{ visible_fields: {visible_fields}, sort_by: {sort_by}, sort_order: {sort_order} }}")

    # Display income_category
    cursor.execute('SELECT name FROM income_category')
    income_categories = cursor.fetchall()
    if income_categories:
        rules_listbox.insert(END, "Income Categories:")
        for category in income_categories:
            rules_listbox.insert(END, f"{category[0]}")

    # Display income_frequency
    cursor.execute('SELECT name FROM income_frequency')
    income_frequencies = cursor.fetchall()
    if income_frequencies:
        rules_listbox.insert(END, "Frequency Categories:")
        for frequency in income_frequencies:
            rules_listbox.insert(END, f"{frequency[0]}")

    conn.close()

def parse_dsl_command():
    """Parses and saves the DSL command into the SQLite database."""
    dsl_command = command_text_area.get("1.0", tk.END).strip()
    if not dsl_command:
        messagebox.showwarning("Warning", "The command input is empty.")
        return

    try:
        model = parse_dsl(dsl_command)
        messagebox.showinfo("Success", "The rule has been parsed and saved successfully!")
        print(model)

        # Save each custom configuration into the database
        for element in model.elements:
            if element.__class__.__name__ == 'InitializationRule':
                save_general_setting('initialize_runtime', element.status)
            elif element.__class__.__name__ == 'WindowEnableRule':
                save_general_setting(f'enable_window_{element.window}', 'yes')

            # Income Field Customizations
            elif element.__class__.__name__ == 'IncomeSourceNameCustomization':
                save_income_field_setting('income_source_name', element.visible, element.required)
            elif element.__class__.__name__ == 'IncomeCategoryCustomization':
                save_income_field_setting('income_category', element.visible, element.required)
            elif element.__class__.__name__ == 'IncomeFrequencyCustomization':
                save_income_field_setting('income_frequency', element.visible, element.required)

            # Expense Field Customizations (NEW for expenses)
            elif element.__class__.__name__ == 'ExpenseSourceNameCustomization':
                save_expense_field_setting('expense_source_name', element.visible, element.required)
            elif element.__class__.__name__ == 'ExpenseCategoryCustomization':
                save_expense_field_setting('expense_category', element.visible, element.required)
            elif element.__class__.__name__ == 'ExpenseAmountCustomization':
                save_expense_field_setting('expense_amount', element.visible, element.required)

            # Button Customizations
            elif element.__class__.__name__ == 'AddIncomeButtonCustomization':
                save_button_setting('add_income_button', element.visible, element.text)
            elif element.__class__.__name__ == 'AddExpenseButtonCustomization':  # NEW for expenses
                save_button_setting('add_expense_button', element.visible, element.text)

        command_text_area.delete("1.0", tk.END)  # Clear the input area after saving
        display_rules()  # Refresh displayed rules
    except Exception as e:
        messagebox.showerror("Parsing Error", f"Error: {e}")

def delete_rule():
    """Deletes the rule entered in the delete field."""
    rule_to_delete = delete_entry.get().strip()
    if rule_to_delete.startswith('"') and rule_to_delete.endswith('"'):
        rule_to_delete = rule_to_delete[1:-1]  # Remove quotes if present

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Attempt to delete in all relevant tables
    cursor.execute("DELETE FROM general_settings WHERE setting_key = ?", (rule_to_delete,))
    cursor.execute("DELETE FROM enabled_windows WHERE window_name = ?", (rule_to_delete,))
    cursor.execute("DELETE FROM income_field_settings WHERE field_name = ?", (rule_to_delete,))
    cursor.execute("DELETE FROM expense_field_settings WHERE field_name = ?", (rule_to_delete,))  # NEW for expenses
    cursor.execute("DELETE FROM button_settings WHERE button_name = ?", (rule_to_delete,))
    cursor.execute("DELETE FROM report_button_settings WHERE button_name = ?", (rule_to_delete,))

    conn.commit()
    conn.close()

    print(f"Deleted rule: {rule_to_delete}")
    print_table_data()  # To verify updated database contents
    display_rules()  # Refresh displayed rules in the UI
    delete_entry.delete(0, END)  # Clear the delete entry field

# GUI setup
window = tk.Tk()
window.title("Personal Finance DSL IDE")
window.geometry("1400x900")

# Tab control setup
tab_control = ttk.Notebook(window)

# Documentation tab
tab_documentation = ttk.Frame(tab_control)
tab_control.add(tab_documentation, text="Documentation")
doc_text_area = scrolledtext.ScrolledText(tab_documentation, width=130, height=40, wrap=tk.WORD)
doc_text_area.pack(pady=10)
try:
    with open("documentation.txt", "r") as doc_file:
        doc_text_area.insert(tk.END, doc_file.read())
except FileNotFoundError:
    doc_text_area.insert(tk.END, "Documentation file not found.")
doc_text_area.config(state='disabled')

# Command entry tab
tab_commands = ttk.Frame(tab_control)
tab_control.add(tab_commands, text="Enter Command")
command_text_area = scrolledtext.ScrolledText(tab_commands, width=130, height=40, wrap=tk.WORD)
command_text_area.pack(pady=10)
save_button = tk.Button(tab_commands, text="Save Rule", command=parse_dsl_command)
save_button.pack(pady=5)

# Defined rules tab
tab_rules = ttk.Frame(tab_control)
tab_control.add(tab_rules, text="Defined Rules")
rules_listbox = Listbox(tab_rules, width=130, height=35, selectmode=tk.SINGLE)
rules_listbox.pack(pady=10)

# Delete rule entry and button
delete_entry = tk.Entry(tab_rules, width=50)
delete_entry.pack(pady=5)
delete_button = tk.Button(tab_rules, text="Delete Rule", command=delete_rule)
delete_button.pack(pady=5)

# Display rules initially
display_rules()

# Pack tabs into window
tab_control.pack(expand=1, fill="both")

# Start main GUI loop
window.mainloop()
