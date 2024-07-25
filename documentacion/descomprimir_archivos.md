## Documentación Técnica del Script: **`descomprimir_archivos.py`**

## Descripción General

Este script está diseñado para descomprimir archivos GZIP (.gz) que contienen datos en formato JSON. El script realiza las siguientes tareas:
1. Definir las rutas de las carpetas.
2. Verificar la existencia de las carpetas y crearlas si no existen.
3. Descomprimir los archivos GZIP y guardar los archivos JSON resultantes en la misma carpeta.

## Importaciones

```python
import os
import gzip
import shutil
```

- **`os`**: Módulo para interactuar con el sistema de archivos.
- **`gzip`**: Módulo para trabajar con archivos comprimidos en formato GZIP.
- **`shutil`**: Módulo para realizar operaciones de alto nivel en archivos y colecciones de archivos.

## Código del Script

### Definición de Rutas y Verificación de Carpetas

```python
# Definir las rutas
base_dir = 'datasets'
original_dir = os.path.join(base_dir, 'original')

# Verificar y crear las carpetas si no existen
if not os.path.exists(base_dir):
    os.mkdir(base_dir)
    print(f"Carpeta '{base_dir}' creada.")
else:
    print(f"Carpeta '{base_dir}' ya existe.")

if not os.path.exists(original_dir):
    os.mkdir(original_dir)
    print(f"Carpeta '{original_dir}' creada.")
else:
    print(f"Carpeta '{original_dir}' ya existe.")
```

- **Propósito**: Especificar las rutas de las carpetas base (`datasets`) y la carpeta original (`datasets/original`), y crear las carpetas si no existen.
- **Operaciones**:
  - **`os.path.exists(path)`**: Verifica si la ruta especificada existe.
  - **`os.mkdir(path)`**: Crea una nueva carpeta en la ruta especificada.
  - **`print(message)`**: Imprime un mensaje para informar al usuario sobre el estado de las carpetas.
  
- **Mensajes**:
  - Si la carpeta `datasets` no existe, se crea y se imprime: `"Carpeta 'datasets' creada."`.
  - Si la carpeta `datasets` ya existe, se imprime: `"Carpeta 'datasets' ya existe."`.
  - Si la carpeta `datasets/original` no existe, se crea y se imprime: `"Carpeta 'original' creada."`.
  - Si la carpeta `datasets/original` ya existe, se imprime: `"Carpeta 'original' ya existe."`.

### Descompresión de Archivos GZIP

```python
# Archivos a descomprimir
files = {
    "user_reviews": "user_reviews.json.gz",
    "users_items": "users_items.json.gz",
    "steam_games": "steam_games.json.gz"
}

# Descomprimir archivos .gz
for file_name in files.values():
    gz_file_path = os.path.join(original_dir, file_name)
    json_file_name = file_name.replace('.gz', '')
    json_file_path = os.path.join(original_dir, json_file_name)
    
    with gzip.open(gz_file_path, 'rb') as f_in:
        with open(json_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            print(f"Archivo '{json_file_name}' descomprimido.")
```

- **Propósito**: Descomprimir los archivos GZIP especificados y guardar los archivos JSON resultantes en la carpeta `datasets/original`.
- **Operaciones**:
  - **`os.path.join(path, filename)`**: Combina una ruta y un nombre de archivo en una única ruta.
  - **`gzip.open(file, mode)`**: Abre un archivo GZIP en el modo especificado.
  - **`open(file, mode)`**: Abre un archivo en el modo especificado.
  - **`shutil.copyfileobj(fsrc, fdst)`**: Copia el contenido de un archivo a otro.
  - **`print(message)`**: Imprime un mensaje para informar al usuario sobre el estado de los archivos.
  
- **Mensajes**:
  - Para cada archivo descomprimido, se imprime: `"Archivo '{json_file_name}' descomprimido."`.

---
