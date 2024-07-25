import os
import gdown

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

# Definir los enlaces y nombres de los archivos
files = {
    'https://drive.google.com/uc?id=1wgjHpBK6zQlSY52TrXlqOnUW-G5pelXQ': 'users_items.json.gz',
    'https://drive.google.com/uc?id=1xE7pEEjYssfOeulGncRz6LXMbZni0x8k': 'user_reviews.json.gz',
    'https://drive.google.com/uc?id=13sS6oB9KWJuF3wS36yiuHAAVpcasztUE': 'steam_games.json.gz'
}

# Descargar los archivos si no existen
for url, name in files.items():
    file_path = os.path.join(original_dir, name)
    if not os.path.exists(file_path):
        gdown.download(url, file_path, quiet=False)
        print(f"Archivo '{name}' descargado.")
    else:
        print(f"Archivo '{name}' ya existe y no se descargará nuevamente.")
