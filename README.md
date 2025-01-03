# Personal Finance DSL: Una Herramienta Personalizada para la Gestión Financiera

## Resumen

**Personal Finance DSL** es un proyecto desarrollado en Python que utiliza la librería TextX para crear un Lenguaje Específico de Dominio (DSL) orientado a la gestión de finanzas personales. Este proyecto permite a expertos en el dominio configurar entornos de ejecución de forma dinámica y ofrece a los usuarios finales una interfaz personalizada para la gestión financiera. Combinando la flexibilidad de TextX con bases de datos SQLite y un entorno de ejecución en Python, el sistema ofrece una herramienta poderosa y adaptable para gestionar ingresos, gastos, presupuestos y metas.

---

## Características

### Para Expertos en el Dominio

- **DSL con TextX**:
  - Gramática definida usando TextX en `finance_dsl.tx`.
  - Sintaxis legible para humanos para definir reglas de configuración.

- **Entorno de Desarrollo Integrado (IDE)**:
  - Escribir, validar y guardar reglas DSL.
  - Validación sintáctica y semántica impulsada por TextX.
  - Almacenar configuraciones en una base de datos SQLite (`finance_rules.db`).

### Para Usuarios Finales

- **Entorno de Ejecución Dinámico**:
  - Las interfaces se generan dinámicamente según las reglas definidas en el DSL.
  - Ventanas totalmente personalizables (Ingresos, Gastos, Presupuestos, Metas).
  - Introducir datos financieros, generar informes y gestionar finanzas personales de manera sencilla.

- **Gestión de Datos**:
  - Los datos del usuario se almacenan en `user_data.db`.
  - Generar informes dinámicos basados en las entradas del usuario y las configuraciones.

---

## Cómo Funciona

### Rol de TextX

TextX se utiliza para definir y analizar la gramática del DSL:

- **Definición de la Gramática**:
  - La estructura del DSL se define en `finance_dsl.tx`, permitiendo a los expertos escribir reglas legibles para humanos.

- **Análisis y Validación**:
  - El motor de TextX analiza las configuraciones del DSL, las convierte en estructuras de datos internas y las valida para garantizar su consistencia lógica.

- **Integración**:
  - Las reglas analizadas se guardan en `finance_rules.db` para su uso en tiempo de ejecución.

### Arquitectura

- **Lenguaje Específico de Dominio**:
  - Gramática definida en `finance_dsl.tx`.
  - Sintaxis para habilitar ventanas, personalizar campos y configurar informes.

- **Análisis y Validación**:
  - TextX garantiza que las reglas del DSL estén correctamente escritas y sean lógicamente coherentes.

- **Bases de Datos**:
  - `finance_rules.db`: Almacena las configuraciones del DSL.
  - `user_data.db`: Almacena las entradas del usuario en tiempo de ejecución.

- **Ejecución Dinámica**:
  - Genera la interfaz y las funcionalidades basadas en las configuraciones almacenadas en `finance_rules.db`.

### Flujo de Trabajo

1. **Experto en el Dominio**:
   - Usa el IDE para escribir y validar reglas DSL.
   - Guarda las reglas en `finance_rules.db` mediante el análisis de TextX.

2. **Tiempo de Ejecución**:
   - Lee las configuraciones desde `finance_rules.db`.
   - Construye dinámicamente pestañas, campos, botones e informes.

3. **Usuario Final**:
   - Interactúa con la interfaz generada dinámicamente para gestionar sus finanzas.

---

## Comenzando

### Requisitos Previos

- **Python 3.x**
- **SQLite3**
- **Librería TextX**:
  - Instala TextX usando pip:
    ```bash
    pip install textx
    ```

