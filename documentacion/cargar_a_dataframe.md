## Documentación Técnica del Script: **`cargar_a_dataframe.py`**

## Descripción General

Este script está diseñado para cargar archivos JSON con el prefijo "se" en DataFrames de pandas y luego imprimir las primeras filas de cada DataFrame en formato Markdown. El script realiza las siguientes tareas:
1. Especificar la ruta de los archivos JSON con el prefijo "se".
2. Cargar los archivos JSON en DataFrames.
3. Imprimir los DataFrames en formato Markdown.

## Importaciones

```python
import os
import pandas as pd
```

- **`os`**: Módulo para interactuar con el sistema de archivos.
- **`pandas`**: Biblioteca para la manipulación y el análisis de datos, proporcionando estructuras de datos de alto rendimiento y fáciles de usar.

## Código del Script

### Definición de Rutas de los Archivos JSON

```python
def main():
    # Especificamos la ruta de los archivos JSON con el prefijo "se"
    carpeta = "datasets/original"
    archivo1 = os.path.join(carpeta, "se_user_reviews.json")
    archivo2 = os.path.join(carpeta, "se_users_items.json")
    archivo3 = os.path.join(carpeta, "se_steam_games.json")
```

- **Propósito**: Definir las rutas de los archivos JSON con el prefijo "se".
- **Operaciones**:
  - **`os.path.join(path, *paths)`**: Une uno o más componentes de ruta de manera inteligente.

### Carga de Archivos JSON en DataFrames

```python
    # Cargamos los archivos JSON en DataFrames
    df_user_reviews = pd.read_json(archivo1, orient='records', lines=True)
    df_users_items = pd.read_json(archivo2, orient='records', lines=True)
    df_steam_games = pd.read_json(archivo3, orient='records', lines=True)
```

- **Propósito**: Cargar los archivos JSON en DataFrames de pandas.
- **Operaciones**:
  - **`pd.read_json(path_or_buf, orient, lines)`**: Lee un archivo JSON y lo convierte en un DataFrame de pandas.
    - **`path_or_buf`**: Ruta del archivo o un búfer de cadena.
    - **`orient`**: Indica el formato de los datos en el archivo JSON. `'records'` indica que los datos están en forma de lista de registros (diccionarios).
    - **`lines`**: Si es `True`, cada línea en el archivo se trata como un objeto JSON separado.

### Impresión de DataFrames en Formato Markdown

```python
    # Imprimimos los DataFrames en formato Markdown
    print("### DataFrame: user_reviews")
    print(df_user_reviews.head().to_markdown(index=False))
    print("\n### DataFrame: users_items")
    print(df_users_items.head().to_markdown(index=False))
    print("\n### DataFrame: steam_games")
    print(df_steam_games.head().to_markdown(index=False))

if __name__ == "__main__":
    main()
```

- **Propósito**: Imprimir las primeras filas de cada DataFrame en formato Markdown.
- **Operaciones**:
  - **`print(message)`**: Imprime un mensaje en la salida estándar.
  - **`df.head(n)`**: Devuelve las primeras `n` filas del DataFrame.
  - **`df.to_markdown(index)`**: Convierte el DataFrame a una tabla en formato Markdown.
    - **`index`**: Si es `False`, no incluye el índice del DataFrame en la salida.

---

Este script está diseñado para ser ejecutado directamente, y al ejecutarlo se cargarán los archivos JSON en DataFrames y se imprimirán las primeras filas en formato Markdown, proporcionando una vista rápida y legible de los datos.