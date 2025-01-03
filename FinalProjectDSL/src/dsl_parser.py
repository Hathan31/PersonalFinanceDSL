from textx import metamodel_from_file
import os
import sqlite3

# Ruta al archivo de grammar
grammar_path = os.path.join(os.path.dirname(__file__), '../grammar/finance_dsl.tx')
finance_dsl_meta = metamodel_from_file(grammar_path)

# Ruta al archivo de la base de datos SQLite
db_path = os.path.join(os.path.dirname(__file__), 'finance_rules.db')

# Función para inicializar la base de datos SQLite
def initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tablas necesarias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS general_settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enabled_windows (
        window_name TEXT PRIMARY KEY
    )
    ''')

    # Income settings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income_field_settings (
        field_name TEXT PRIMARY KEY,
        visible TEXT,
        required TEXT
    )
    ''')

    # Expense settings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense_field_settings (
        field_name TEXT PRIMARY KEY,
        visible TEXT,
        required TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense_display_settings (
        setting_key TEXT PRIMARY KEY,
        visible_fields TEXT,
        sort_by TEXT,
        sort_order TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS button_settings (
        button_name TEXT PRIMARY KEY,
        visible TEXT,
        text TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS report_button_settings (
        button_name TEXT PRIMARY KEY,
        visible TEXT,
        text TEXT,
        report_types TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income_display_settings (
        setting_key TEXT PRIMARY KEY,
        visible_fields TEXT,
        sort_by TEXT,
        sort_order TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income_category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income_frequency (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense_category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Función para mostrar el contenido de todas las tablas
def print_table_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = [
        "general_settings", "enabled_windows", "income_field_settings",
        "expense_field_settings", "button_settings", "report_button_settings",
        "income_display_settings", "expense_display_settings",
        "income_category", "expense_category", "income_frequency"
    ]

    for table in tables:
        print(f"\nContents of {table}:")
        cursor.execute(f"SELECT * FROM {table}")
        for row in cursor.fetchall():
            print(row)

    conn.close()

initialize_db()  # Inicializar la base de datos

# Función para analizar el texto DSL usando la gramática y devolver el modelo
def parse_dsl(dsl_text):
    """Función que analiza el texto DSL y devuelve el modelo."""
    try:
        model = finance_dsl_meta.model_from_str(dsl_text)
        print("Parsing successful!")
        return model
    except Exception as e:
        print(f"Parsing error: {e}")
        raise

# Funciones para guardar configuraciones
def save_general_setting(setting_key, setting_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO general_settings (setting_key, setting_value) VALUES (?, ?)",
                   (setting_key, setting_value))
    conn.commit()
    conn.close()
    print(f"Saved general setting: {setting_key} = {setting_value}")

def save_income_field_setting(field_name, visible, required):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO income_field_settings (field_name, visible, required) VALUES (?, ?, ?)",
                   (field_name, visible, required))
    conn.commit()
    conn.close()
    print(f"Saved income field setting: {field_name} (visible: {visible}, required: {required})")

def save_expense_field_setting(field_name, visible, required):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO expense_field_settings (field_name, visible, required) VALUES (?, ?, ?)",
                   (field_name, visible, required))
    conn.commit()
    conn.close()
    print(f"Saved expense field setting: {field_name} (visible: {visible}, required: {required})")

def save_button_setting(button_name, visible, text):
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO button_settings (button_name, visible, text) VALUES (?, ?, ?)",
                   (button_name, visible, text))
    conn.commit()
    conn.close()
    print(f"Saved button setting: {button_name} (visible: {visible}, text: {text})")

def save_report_button_setting(button_name, visible, text, report_types):
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO report_button_settings (button_name, visible, text, report_types) VALUES (?, ?, ?, ?)",
                   (button_name, visible, text, report_types))
    conn.commit()
    conn.close()
    print(f"Saved report button setting: {button_name} (visible: {visible}, text: {text}, report_types: {report_types})")

def save_income_display_setting(setting_key, visible_fields, sort_by, sort_order):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO income_display_settings (setting_key, visible_fields, sort_by, sort_order) VALUES (?, ?, ?, ?)",
                   (setting_key, visible_fields, sort_by, sort_order))
    conn.commit()
    conn.close()
    print(f"Saved income display setting: {setting_key} (visible_fields: {visible_fields}, sort_by: {sort_by}, sort_order: {sort_order})")

def save_expense_display_setting(setting_key, visible_fields, sort_by, sort_order):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO expense_display_settings (setting_key, visible_fields, sort_by, sort_order) VALUES (?, ?, ?, ?)",
                   (setting_key, visible_fields, sort_by, sort_order))
    conn.commit()
    conn.close()
    print(f"Saved expense display setting: {setting_key} (visible_fields: {visible_fields}, sort_by: {sort_by}, sort_order: {sort_order})")

def save_income_category_to_db(category):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO income_category (name) VALUES (?)", (category,))
    conn.commit()
    conn.close()
    print(f"Saved income category: {category}")

def save_expense_category_to_db(category):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO expense_category (name) VALUES (?)", (category,))
    conn.commit()
    conn.close()
    print(f"Saved expense category: {category}")

def save_income_frequency_to_db(frequency):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO income_frequency (name) VALUES (?)", (frequency,))
    conn.commit()
    conn.close()
    print(f"Saved income frequency: {frequency}")

def save_enabled_window(window_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO enabled_windows (window_name) VALUES (?)", (window_name,))
    conn.commit()
    conn.close()
    print(f"Saved enabled window: {window_name}")

# Funciones para eliminar reglas
def delete_rule_from_table(table_name, key_column, key_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {key_column} = ?", (key_value,))
    conn.commit()
    conn.close()
    print(f"Deleted rule from {table_name} where {key_column} = {key_value}")

def delete_rule(rule_name):
    tables = {
        "general_settings": "setting_key",
        "enabled_windows": "window_name",
        "income_field_settings": "field_name",
        "expense_field_settings": "field_name",
        "button_settings": "button_name",
        "report_button_settings": "button_name",
        "income_display_settings": "setting_key",
        "expense_display_settings": "setting_key",
        "income_category": "name",
        "expense_category": "name",
        "income_frequency": "name",
    }

    for table, key_column in tables.items():
        delete_rule_from_table(table, key_column, rule_name)