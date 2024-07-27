from fastapi import HTTPException,FastAPI
import pandas as pd
from fastapi.responses import HTMLResponse, JSONResponse
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from scipy.stats import pearsonr
import json

app = FastAPI()

# Cargamos nuestros datasets: 
df_items_items = pd.read_csv("./datasets/df_items_items.csv")
df_reviews_reviews = pd.read_csv("./datasets/df_reviews_reviews.csv")
df_games = pd.read_csv("./datasets/df_games.csv")
df_items = pd.read_csv("./datasets/df_items.csv")
df_reviews = pd.read_csv("./datasets/df_reviews.csv")
df_games["release_date"] = pd.to_datetime(df_games["release_date"], errors="coerce")
df_reviews_reviews["posted"] = pd.to_datetime(df_reviews_reviews["posted"], errors="coerce")

app = FastAPI()

# Crear punto de entreada o endpoint:
@app.get("/", tags=["Bienvenida"]) 
def mensaje():
    content = """
    <h2> Bienvenido al PI_MLOps_Engineer </h2>
    <p>Accede a la documentación:</p>
    <ul>
        <li><a href='http://127.0.0.1:50000/docs' >Local (FastAPI)</a></li>
        <li><a href='https://pi-mlops-08.onrender.com/docs' >Producción (Render)</a></li>
    </ul>
    """
    return HTMLResponse(content=content)


"""
1 - def PlayTimeGenre( genero : str ): Debe devolver anio con mas horas jugadas para dicho género.
"""
# Ejemplo: Indie
# Rrespuesta esperada: { "anio de lanzamiento con más horas jugadas para el género indie": 2006 }

@app.get("/PlayTimeGenre/{genero}", tags=["Funciones"])
def PlayTimeGenre(genero: str):
    # Combinar los dataframes df_games y df_items_items utilizando la columna de identificación
    merged_df = df_games.merge(df_items_items, left_on="id", right_on="item_id")
    # Convertir genero y genres a minúsculas para hacer coincidencias insensibles a mayúsculas y minúsculas
    genero = genero.lower()
    # Convertir la columna "genres" a tipo cadena y luego a minúsculas
    merged_df["genres"] = merged_df["genres"].astype(str).str.lower()
    # Inicializar un diccionario para realizar un seguimiento del tiempo de juego por anio
    playtime_by_year = {}

    # Iterar a través de cada fila del dataframe combinado
    for index, row in merged_df.iterrows():
        # Verificar si el género proporcionado está en la lista de géneros de la fila actual
        if genero in row["genres"]:
            # Obtener el anio de la fecha de lanzamiento
            release_year = row["release_date"].year
            # Agregar las horas jugadas al contador correspondiente al anio de lanzamiento
            if release_year in playtime_by_year:
                playtime_by_year[release_year] += row["playtime_forever"]
            else:
                playtime_by_year[release_year] = row["playtime_forever"]

    # Encontrar el anio con más horas jugadas
    max_year = max(playtime_by_year, key=playtime_by_year.get)

    # Devolver el resultado como una respuesta JSON
    return JSONResponse(content={"anio de lanzamiento con más horas jugadas para el género " + genero: max_year})

"""
2 - def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por anio.
"""
# Ejemplo: Indie
# Rrespuesta esperada:  {
#                         "Usuario con más horas jugadas para Género indie": 765611983889673,
#                         "Horas jugadas": [
#                           {
#                               "anio": 2006,
#                               "Horas": 421652
#                           }
#                          ]
#                       }

@app.get("/UserForGenre/{genero}", tags=["Funciones"])
def UserForGenre(genero: str):
    # Combinar los dataframes df_games y df_items_items utilizando la columna de identificación
    merged_df = df_games.merge(df_items_items, left_on="id", right_on="item_id")

    # Convertir genero y genres a minúsculas para hacer coincidencias insensibles a mayúsculas y minúsculas
    genero = genero.lower()
    # Convertir la columna "genres" a tipo cadena y luego a minúsculas
    merged_df["genres"] = merged_df["genres"].astype(str).str.lower()
    
    # Inicializar un diccionario para realizar un seguimiento de las horas jugadas por anio para el usuario específico
    playtime_by_year = {}

    # Inicializar una variable para realizar un seguimiento del usuario con más horas jugadas
    max_playtime_user = None
    max_playtime = 0

    # Iterar a través de cada fila del dataframe combinado
    for index, row in merged_df.iterrows():
        # Verificar si el género proporcionado está en la lista de géneros de la fila actual
        if genero in row["genres"]:
            # Obtener el usuario y las horas jugadas para la fila actual
            user_id = row["user_id"]
            playtime = row["playtime_forever"]
            # Verificar si el usuario actual tiene más horas jugadas que el máximo actual
            if user_id not in playtime_by_year:
                playtime_by_year[user_id] = []
            playtime_by_year[user_id].append({"anio": row["release_date"].year, "Horas": playtime})
            if playtime > max_playtime:
                max_playtime = playtime
                max_playtime_user = user_id

    # Devolver el resultado
    return JSONResponse(content={"Usuario con más horas jugadas para Género " + genero: max_playtime_user, "Horas jugadas": playtime_by_year[max_playtime_user]})

"""
3 - def UsersRecommend( anio : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el anio dado. (reviews.recommend = True y comentarios positivos/neutrales)
"""
# Ejemplo: 2015
# Respuesta esperada: {
#                       "Puesto 1": "counter-strike: global offensive",
#                       "Puesto 2": "garry's mod",
#                       "Puesto 3": "unturned"
#                     }

@app.get("/UsersRecommend/{anio}", tags=["Funciones"])
def UsersRecommend(anio: int):
    # Combinar los dataframes df_reviews_reviews y df_items_items utilizando la columna de identificación
    merged_df = df_reviews_reviews.merge(df_items_items, left_on="item_id", right_on="item_id")

    # Filtrar los juegos recomendados para el anio dado con análisis de sentimientos positivos y neutrales
    recommended_games = merged_df[(merged_df["recommend"] == True) & 
        (merged_df["posted"].dt.year == anio) & 
        ((merged_df["sentiment_analysis"] == 2) | (merged_df["sentiment_analysis"] == 1))]

    # Obtener los top 3 juegos más recomendados
    top_3_recommendations = recommended_games["item_name"].str.lower().value_counts().head(3).index.tolist()

    # Convertir la lista de juegos en un diccionario
    recommendations_dict = {
        "Puesto 1": top_3_recommendations[0],
        "Puesto 2": top_3_recommendations[1],
        "Puesto 3": top_3_recommendations[2]
    }

    # Devolver el resultado
    return JSONResponse(content=recommendations_dict)
"""
4 - def UsersNotRecommend( anio : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el anio dado. (reviews.recommend = False y comentarios negativos)
"""
# Ejemplo: 2015
# Respuesta esperada: 
#[
#  {
#    "Puesto 1": "counter-strike: global offensive"
#  },
#  {
#    "Puesto 2": "payday 2"
#  },
#  {
#    "Puesto 3": "unturned"
#  }
#]
def get_top_not_recommendations(df_reviews_reviews, df_items_items, anio):
    # Combinar los dataframes df_reviews_reviews y df_items_items utilizando la columna de identificación
    merged_df = df_reviews_reviews.merge(df_items_items, left_on="item_id", right_on="item_id")

    # Filtrar los juegos no recomendados para el anio dado con análisis de sentimientos negativos
    not_recommended_games = merged_df[(merged_df["recommend"] == False) & 
                                      (merged_df["posted"].dt.year == anio) & 
                                      (merged_df["sentiment_analysis"] == 0)]

    # Obtener los top 3 juegos menos recomendados
    top_3_not_recommendations = not_recommended_games["item_name"].str.lower().value_counts().head(3).index.tolist()

    return top_3_not_recommendations

@app.get("/UsersNotRecommend/{anio}", tags=["Funciones"])
async def get_users_not_recommend(anio: int):
    top_3_not_recommendations = get_top_not_recommendations(df_reviews_reviews, df_items_items, anio)
    return JSONResponse(content=[{"Puesto 1": top_3_not_recommendations[0]}, 
                                 {"Puesto 2": top_3_not_recommendations[1]}, 
                                 {"Puesto 3": top_3_not_recommendations[2]}])

"""
5 - def sentiment_analysis( anio : int ): Según el anio de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
"""
# Ejemplo: 2015
# Respuesta esperada:
#{
#  "Negative": 1100,
#  "Neutral": 891,
#  "Positive": 2470
#}

# Definimos la función para el análisis de sentimientos
def sentiment_analysis(year: int, df_games: pd.DataFrame, df_reviews_reviews: pd.DataFrame):
    try:
        # Filtrar las reseñas de juegos lanzados en el anio especificado
        filtered_games = df_games[df_games["release_date"].dt.year == year]
        
        # Obtener los IDs de juegos lanzados en ese anio
        game_ids = filtered_games["id"].tolist()
        
        # Filtrar las reseñas de usuarios que corresponden a esos juegos
        filtered_reviews = df_reviews_reviews[df_reviews_reviews["item_id"].isin(game_ids)]
        
        # Realizar el conteo de las categorías de análisis de sentimiento
        sentiment_counts = filtered_reviews["sentiment_analysis"].value_counts().to_dict()
        
        # Agregar descripciones a las categorías
        sentiment_counts_with_description = {
            "Negative": sentiment_counts.get(0, 0),
            "Neutral": sentiment_counts.get(1, 0),
            "Positive": sentiment_counts.get(2, 0)
        }
        
        return sentiment_counts_with_description
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Definir la ruta y el método para la función de análisis de sentimientos
@app.get("/sentiment_analysis/{year}", tags=["Funciones"])
def analyze_sentiments(year: int):
    # Llamar a la función de análisis de sentimientos y obtener los resultados
    sentiment_counts = sentiment_analysis(year, df_games, df_reviews_reviews)
    
    # Devolver una respuesta JSON con el contenido generado
    return JSONResponse(content=sentiment_counts)

"""
###                                 - - - # Modelos de ML para Sistema de recomendación - - - 
"""
# La funcionalidad de las funciones esta comprobada en el archivo ETL-EDA.ipynb
"""
## a - k-Nearest Neighbors (k-NN):
"""
## - El algoritmo k-NN se basa en la idea de que objetos similares tienden a estar cerca unos de otros en un espacio de características. Funciona de la siguiente manera:

# Ejemplo: 774277


# Función para obtener recomendaciones
def get_recommendations_knn(game_id):
    # Tratar los valores faltantes en las columnas "genres" y "tags" con "Desconocido"
    df_games["genres"].fillna("Desconocido", inplace=True)
    df_games["tags"].fillna("Desconocido", inplace=True)

    # Asegurarse de que las columnas "genres" y "tags" sean de tipo string
    df_games["genres"] = df_games["genres"].astype(str)
    df_games["tags"] = df_games["tags"].astype(str)

    # Realizar la eliminación de comillas simples
    df_games["genres"] = df_games["genres"].str.replace(""", "")
    df_games["tags"] = df_games["tags"].str.replace(""", "")

    # Convertir las columnas "genres" y "tags" a variables categóricas
    label_encoder = LabelEncoder()
    df_games["genres"] = label_encoder.fit_transform(df_games["genres"])
    df_games["tags"] = label_encoder.fit_transform(df_games["tags"])

    # Entrenar el modelo KNN
    knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
    knn.fit(df_games[["genres", "tags"]])
    
    # Encontrar el juego más similar utilizando el modelo KNN
    game = df_games.loc[df_games["id"] == game_id, ["genres", "tags"]].values.reshape(1, -1)
    distances, indices = knn.kneighbors(game)

    # Obtener los nombres de las aplicaciones recomendadas
    recommended_app_names = df_games.iloc[indices[0]]["app_name"].tolist()

    # Crear un JSON con los nombres de las aplicaciones recomendadas
    recommendations_json = {
        "games": recommended_app_names
    }

    return recommendations_json

@app.get("/recomendacion_juego_knn/{id_game}", tags=["Modelos de Recomendación Item-Item"])
def get_recomendacion_juego_knn(game_id:int):
    recommendations = get_recommendations_knn(game_id)
    return recommendations

"""
## b - Similitud de Cosenos
"""
## - El modelo utiliza la similitud de cosenos para encontrar juegos que son similares a un juego específico en función de sus características, como géneros y etiquetas. Este enfoque permite construir un sistema de recomendación basado en la relación ítem-ítem.

import json

def get_recommendations_sim_cos_internal(game_id):

    # Asegurarse de que las columnas "genres" y "tags" sean de tipo string
    df_games["genres"] = df_games["genres"].astype(str)
    df_games["tags"] = df_games["tags"].astype(str)

    # Realizar la eliminación de comillas simples
    df_games["genres"] = df_games["genres"].str.replace(""", "")
    df_games["tags"] = df_games["tags"].str.replace(""", "")

    # Convertir las columnas "genres" y "tags" a variables categóricas
    label_encoder = LabelEncoder()
    df_games["genres"] = label_encoder.fit_transform(df_games["genres"])
    df_games["tags"] = label_encoder.fit_transform(df_games["tags"])

    # Calcular la similitud de cosenos entre los juegos
    similarity_matrix = cosine_similarity(df_games[["genres", "tags"]])

    # Encontrar el índice del juego dado
    game_index = df_games[df_games["id"] == game_id].index[0]

    # Obtener las similitudes del juego dado con otros juegos
    game_similarities = similarity_matrix[game_index]

    # Obtener los índices de los juegos más similares
    similar_game_indices = game_similarities.argsort()[:-6:-1]

    # Obtener los nombres de las aplicaciones recomendadas
    recommended_app_names = df_games.iloc[similar_game_indices]["app_name"].tolist()

    # Crear un diccionario con los nombres de las aplicaciones recomendadas
    recommendations_dict = {"games": recommended_app_names}

    return recommendations_dict

# Ruta para la recomendación de usuario
@app.get("/recomendacion_juego_sim_cos/{id_game}", tags=["Modelos de Recomendación Item-Item"])
def get_recommendations_sim_cos(game_id:int):
    recommendations_dict = get_recommendations_sim_cos_internal(game_id)
    return recommendations_dict