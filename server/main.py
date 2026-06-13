from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from algorithm import start_algo, get_movies_seen_by_user
from api import get_movies_info
import asyncio
import os
from dotenv import load_dotenv



app = FastAPI()

load_dotenv()
ORIGIN = os.getenv("FRONT_URL") or ""


origins = [
    ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']

)


@app.get("/users/{id}")
async def get(id: int):
    try:
        print(id)
        assert id is not None, "Missing id"
        movies_liked_by_user = get_movies_seen_by_user(id)
        assert movies_liked_by_user is not None, "User not found, try with a smaller id"
        movies_recommended = start_algo(id)
        assert movies_recommended is not None, "Error"
        movies_recommended = movies_recommended.to_list()
        movies_recommended_info, movies_liked_by_user_info = await asyncio.gather(get_movies_info(movies_recommended), get_movies_info(movies_liked_by_user))
        print("success")
        return {"success": True, "movies_recommended": movies_recommended_info, "movies_liked_by_user": movies_liked_by_user_info}
    except AssertionError as e:
        print("fail")
        return {"success": False, "message": str(e)}
    except Exception as e:
        print("fail:", e)
        return {"success": False}
        
