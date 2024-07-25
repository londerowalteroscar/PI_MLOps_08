import os
import gzip
import shutil

# Definir las rutas
base_dir = 'datasets'
original_dir = os.path.join(base_dir, 'original')

# Definir los archivos a descomprimir
files = {
    'user_reviews': 'user_reviews.json.gz',
    'users_items': 'users_items.json.gz',
    'steam_games': 'steam_games.json.gz'
}

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

# Descomprimir archivos .gz
for file_name in files.values():
    gz_file_path = os.path.join(original_dir, file_name)
    json_file_name = file_name.replace('.gz', '')
    json_file_path = os.path.join(original_dir, json_file_name)
    
    with gzip.open(gz_file_path, 'rb') as f_in:
        with open(json_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            print(f"Archivo '{json_file_name}' descomprimido.")
