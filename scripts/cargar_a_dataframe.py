import os
import pandas as pd

def main():
    # Especificamos la ruta de los archivos JSON con el prefijo "se"
    carpeta = "datasets/original"
    archivo1 = os.path.join(carpeta, "se_user_reviews.json")
    archivo2 = os.path.join(carpeta, "se_users_items.json")
    archivo3 = os.path.join(carpeta, "se_steam_games.json")

    # Cargamos los archivos JSON en DataFrames
    df_user_reviews = pd.read_json(archivo1, orient='records', lines=True)
    df_users_items = pd.read_json(archivo2, orient='records', lines=True)
    df_steam_games = pd.read_json(archivo3, orient='records', lines=True)

    # Imprimimos los DataFrames en formato Markdown
    print("### DataFrame: user_reviews")
    print(df_user_reviews.head().to_markdown(index=False))
    print("\n### DataFrame: users_items")
    print(df_users_items.head().to_markdown(index=False))
    print("\n### DataFrame: steam_games")
    print(df_steam_games.head().to_markdown(index=False))

if __name__ == "__main__":
    main()
