from fastapi import FastAPI,  Request
from fastapi.middleware.cors import CORSMiddleware
from algorithm import start_algo, get_movies_seen_by_user
import requests
import os
from dotenv import load_dotenv


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173", # Ajoutez cette ligne
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, #  signifie que le navigateur est autorisé à envoyer des informations d'authentification avec les requêtes vers ton API.
    allow_methods=['*'],
    allow_headers=['*']

)

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

@app.get("/")
def root():
    return {"message" : "test"}

@app.get("/users/{id}")
def get(id : int):
    print(id)
    movies_liked_by_user = get_movies_seen_by_user(id)
    if movies_liked_by_user is None:
        return {"success" : False, "message" : "User not found, try with a smaller id"}
    movies_recommended = list(start_algo(id))
    movies_info = [[],[]]
    # print("here :", movies_recommended)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    all_movies = [movies_recommended, movies_liked_by_user]
    for index, movies in enumerate(all_movies):
        for id in movies:
            url = f"https://api.themoviedb.org/3/movie/{id}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # print(data)
                genres = [el["name"] for el in data["genres"]]
                movies_info[index].append({
                    "title": data["title"],
                    "poster_link" : "https://image.tmdb.org/t/p/w500" +  data["poster_path"],
                    "genres" : genres
                })
            else:
                print(f"Erreur TMDB pour ID : {response.status_code}")

    print(movies_info)
    return {"success" : True, "movies_recommended" : movies_info[0], "movies_liked_by_user" : movies_info[1]}

