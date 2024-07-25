import os

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
