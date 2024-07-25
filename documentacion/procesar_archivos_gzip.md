## Documentación Técnica del Script: **`procesar_archivos_gzip.py`**

## Descripción General

Este script está diseñado para procesar archivos GZIP que contienen datos en formato de literales de Python o JSON. El script realiza las siguientes tareas:
1. Descomprimir archivos GZIP.
2. Leer los datos y convertirlos a listas de Python.
3. Convertir las listas a DataFrames de `pandas`.
4. Guardar los DataFrames como archivos JSON en una carpeta de salida.

## Importaciones

```python
import gzip
import json
import ast
import os
import pandas as pd
```

- **`gzip`**: Módulo para trabajar con archivos comprimidos en formato GZIP.
- **`json`**: Módulo para manejar datos en formato JSON.
- **`ast`**: Módulo para evaluar literales de Python en cadenas de texto.
- **`os`**: Módulo para interactuar con el sistema de archivos.
- **`pandas`**: Biblioteca para el análisis y manipulación de datos en estructuras tabulares.

## Funciones

### `abrir_python`

```python
def abrir_python(archivo):
    """
    Abre un archivo GZIP que contiene literales de Python (listas, diccionarios, etc.)
    y devuelve una lista de los datos extraídos.
    """
    datos = []
    with gzip.open(archivo, "rb") as file:
        for linea in file:
            linea_decodificada = linea.decode("utf-8").strip()
            try:
                datos.append(ast.literal_eval(linea_decodificada))
            except (SyntaxError, ValueError) as e:
                print(f"Error de evaluación en la línea: {linea_decodificada}")
                print(e) 
    return datos
```

- **Propósito**: Leer un archivo GZIP que contiene literales de Python, como listas o diccionarios, y devolver una lista de datos.
- **Parámetros**: 
  - `archivo`: Ruta al archivo GZIP que se va a leer.
- **Retorna**: Una lista de datos extraídos del archivo.
- **Errores Manejado**:
  - `SyntaxError` y `ValueError` durante la evaluación de literales.

### `abrir_json`

```python
def abrir_json(archivo):
    """
    Abre un archivo GZIP que contiene objetos JSON válidos en cada línea y devuelve
    una lista de los datos extraídos.
    """
    datos = []
    with gzip.open(archivo, "rt", encoding="utf-8") as file:
        for linea in file:
            try:
                datos.append(json.loads(linea.strip()))
            except json.JSONDecodeError as e:
                print(f"Error de decodificación JSON en la línea: {linea.strip()}")
                print(e)
    return datos
```

- **Propósito**: Leer un archivo GZIP que contiene objetos JSON en cada línea y devolver una lista de datos.
- **Parámetros**:
  - `archivo`: Ruta al archivo GZIP que se va a leer.
- **Retorna**: Una lista de datos extraídos del archivo.
- **Errores Manejado**:
  - `json.JSONDecodeError` durante la decodificación de JSON.

## Procesamiento de Archivos

### Ruta de los Archivos

```python
carpeta = "datasets/original"  # Asegúrate de que la carpeta exista
archivo1 = os.path.join(carpeta, "user_reviews.json.gz")
archivo2 = os.path.join(carpeta, "users_items.json.gz")
archivo3 = os.path.join(carpeta, "steam_games.json.gz")
```

- **Propósito**: Especificar la ruta de los archivos GZIP a procesar.
- **Variables**:
  - `carpeta`: Ruta de la carpeta que contiene los archivos originales.
  - `archivo1`, `archivo2`, `archivo3`: Rutas completas de los archivos GZIP a procesar.

### Lectura y Conversión a DataFrames

```python
data1 = abrir_python(archivo1)
data2 = abrir_python(archivo2)
data3 = abrir_json(archivo3)

df_user_reviews = pd.DataFrame(data1)
df_users_items = pd.DataFrame(data2)
df_steam_games = pd.DataFrame(data3)
```

- **Propósito**: Leer los datos de los archivos y convertirlos en DataFrames de `pandas`.
- **Operaciones**:
  - `abrir_python(archivo)`: Llama a la función para abrir archivos que contienen literales de Python.
  - `abrir_json(archivo)`: Llama a la función para abrir archivos que contienen objetos JSON.
  - `pd.DataFrame(data)`: Convierte las listas de datos en DataFrames.

### Guardado de DataFrames como JSON

```python
salida_carpeta = "datasets/procesados"  # Nueva carpeta para los archivos procesados
os.makedirs(salida_carpeta, exist_ok=True)  # Crear la carpeta si no existe

df_user_reviews.to_json(os.path.join(salida_carpeta, "user_reviews.json"), orient='records', lines=True)
df_users_items.to_json(os.path.join(salida_carpeta, "users_items.json"), orient='records', lines=True)
df_steam_games.to_json(os.path.join(salida_carpeta, "steam_games.json"), orient='records', lines=True)

print("Archivos JSON guardados en la carpeta 'datasets/procesados'.")
```

- **Propósito**: Guardar los DataFrames como archivos JSON en una carpeta de salida.
- **Parámetros**:
  - `salida_carpeta`: Ruta de la carpeta donde se guardarán los archivos procesados.
- **Operaciones**:
  - `os.makedirs(path, exist_ok=True)`: Crea la carpeta de salida si no existe.
  - `to_json(path, orient, lines)`: Guarda cada DataFrame como un archivo JSON.
  - `print(message)`: Imprime un mensaje para confirmar que los archivos han sido guardados.

---

Este documento proporciona una visión general detallada del script, incluyendo el propósito, los parámetros, y los errores manejados por cada función, así como la operación general del script.