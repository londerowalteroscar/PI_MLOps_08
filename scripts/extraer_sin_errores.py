import gzip
import json
import ast
import os
import pandas as pd

# --- Funciones para abrir archivos ---

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

# --- Ruta de los archivos ---

carpeta = "datasets/original"  # Asegúrate de que la carpeta exista
archivo1 = os.path.join(carpeta, "user_reviews.json.gz")
archivo2 = os.path.join(carpeta, "users_items.json.gz")
archivo3 = os.path.join(carpeta, "steam_games.json.gz")

# --- Lectura y conversión a DataFrames ---

data1 = abrir_python(archivo1)
data2 = abrir_python(archivo2)
data3 = abrir_json(archivo3)

df_user_reviews = pd.DataFrame(data1)
df_users_items = pd.DataFrame(data2)
df_steam_games = pd.DataFrame(data3)

# --- Guardado de DataFrames como JSON ---

salida_carpeta = "datasets/procesados"  # Nueva carpeta para los archivos procesados
os.makedirs(salida_carpeta, exist_ok=True)  # Crear la carpeta si no existe

df_user_reviews.to_json(os.path.join(salida_carpeta, "user_reviews.json"), orient='records', lines=True)
df_users_items.to_json(os.path.join(salida_carpeta, "users_items.json"), orient='records', lines=True)
df_steam_games.to_json(os.path.join(salida_carpeta, "steam_games.json"), orient='records', lines=True)

print("Archivos JSON guardados en la carpeta 'datasets/procesados'.")
