## Documentación Técnica del Script: **`descargar_archivos.py`**

## Descripción General

Este script está diseñado para descargar archivos GZIP (.gz) desde Google Drive utilizando `gdown`. El script realiza las siguientes tareas:
1. Definir las rutas de las carpetas.
2. Verificar la existencia de las carpetas y crearlas si no existen.
3. Descargar los archivos GZIP desde los enlaces proporcionados, solo si no existen en el directorio especificado.

## Importaciones

```python
import os
import gdown
```

- **`os`**: Módulo para interactuar con el sistema de archivos.
- **`gdown`**: Biblioteca para descargar archivos desde Google Drive utilizando sus enlaces de descarga.

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

### Definición de Enlaces y Nombres de Archivos

```python
# Definir los enlaces y nombres de los archivos
files = {
    'https://drive.google.com/uc?id=1wgjHpBK6zQlSY52TrXlqOnUW-G5pelXQ': 'users_items.json.gz',
    'https://drive.google.com/uc?id=1xE7pEEjYssfOeulGncRz6LXMbZni0x8k': 'user_reviews.json.gz',
    'https://drive.google.com/uc?id=13sS6oB9KWJuF3wS36yiuHAAVpcasztUE': 'steam_games.json.gz'
}
```

- **Propósito**: Definir los enlaces de descarga y los nombres de los archivos a descargar.
- **Operaciones**:
  - **`dict`**: Un diccionario donde las claves son los enlaces de descarga y los valores son los nombres de los archivos correspondientes.

### Descarga de Archivos

```python
# Descargar los archivos si no existen
for url, name in files.items():
    file_path = os.path.join(original_dir, name)
    if not os.path.exists(file_path):
        gdown.download(url, file_path, quiet=False)
        print(f"Archivo '{name}' descargado.")
    else:
        print(f"Archivo '{name}' ya existe y no se descargará nuevamente.")
```

- **Propósito**: Descargar los archivos GZIP desde los enlaces proporcionados si no existen en el directorio especificado.
- **Operaciones**:
  - **`os.path.exists(path)`**: Verifica si la ruta especificada existe.
  - **`gdown.download(url, output, quiet)`**: Descarga el archivo desde el enlace proporcionado y lo guarda en la ruta especificada.
  - **`print(message)`**: Imprime un mensaje para informar al usuario sobre el estado de la descarga.
  
- **Mensajes**:
  - Si el archivo no existe, se descarga y se imprime: `"Archivo '{name}' descargado."`.
  - Si el archivo ya existe, se imprime: `"Archivo '{name}' ya existe y no se descargará nuevamente."`.

---
