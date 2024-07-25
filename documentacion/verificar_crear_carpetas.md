## Documentación Técnica del Script: **`verificar_crear_carpetas.py`**

## Descripción General

Este script está diseñado para verificar la existencia de las carpetas necesarias para un proyecto y crearlas si no existen. Específicamente, maneja las carpetas `datasets` y `datasets/original`. El script realiza las siguientes tareas:
1. Definir las rutas de las carpetas.
2. Verificar la existencia de las carpetas.
3. Crear las carpetas si no existen.

## Importaciones

```python
import os
```

- **`os`**: Módulo para interactuar con el sistema de archivos.

## Código del Script

### Definición de Rutas

```python
# Definir las rutas
base_dir = 'datasets'
original_dir = os.path.join(base_dir, 'original')
```

- **Propósito**: Especificar las rutas de las carpetas base (`datasets`) y la carpeta original (`datasets/original`).
- **Variables**:
  - **`base_dir`**: Nombre de la carpeta base.
  - **`original_dir`**: Ruta completa de la carpeta original.

### Verificación y Creación de Carpetas

```python
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

- **Propósito**: Verificar la existencia de las carpetas especificadas y crearlas si no existen.
- **Operaciones**:
  - **`os.path.exists(path)`**: Verifica si la ruta especificada existe.
  - **`os.mkdir(path)`**: Crea una nueva carpeta en la ruta especificada.
  - **`print(message)`**: Imprime un mensaje para informar al usuario sobre el estado de las carpetas.
  
- **Mensajes**:
  - Si la carpeta `datasets` no existe, se crea y se imprime: `"Carpeta 'datasets' creada."`.
  - Si la carpeta `datasets` ya existe, se imprime: `"Carpeta 'datasets' ya existe."`.
  - Si la carpeta `datasets/original` no existe, se crea y se imprime: `"Carpeta 'original' creada."`.
  - Si la carpeta `datasets/original` ya existe, se imprime: `"Carpeta 'original' ya existe."`.

---

Este documento proporciona una visión general detallada del script, incluyendo el propósito de cada sección del código, las operaciones realizadas y los mensajes informativos para el usuario.