from fastapi import FastAPI,  Request
from fastapi.middleware.cors import CORSMiddleware
from train_model import start_algo
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
print(API_KEY)

@app.get("/")
def root():
    return {"message" : "test"}

@app.get("/users/{id}")
def get(id : int):
    print(id)
    movies = list(start_algo(id))
    movies_info = []
    headers = {"Authorization": f"Bearer {API_KEY}"}
    for id in movies:
        url = f"https://api.themoviedb.org/3/movie/{id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(data)
            genres = [el["name"] for el in data["genres"]]
            movies_info.append({
                "title": data["title"],
                "poster_link" : "https://image.tmdb.org/t/p/w500" +  data["poster_path"],
                "genres" : genres
            })
    else:
                print(f"Erreur TMDB pour ID : {response.status_code}")

        

    print(movies_info)
    return {"movies" : movies_info}

