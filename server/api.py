import asyncio
import httpx
import os


API_KEY = os.getenv("TMDB_API_KEY") or ""
headers = {"Authorization": f"Bearer {API_KEY}"}


async def get_movie(movie_id: int, client: httpx.AsyncClient):
    """
    Fetches details for a single movie from the TMDB API.

    Args:
        movie_id (int): The TMDB identifier for the movie.
        client (httpx.AsyncClient): An active HTTPX asynchronous client.

    Returns:
        dict or None: A dictionary containing movie title, poster link, and genres,
                      or None if the API request fails.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = await client.get(url, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    genres = [el["name"] for el in data["genres"]]
    return {"title": data["title"],
            "poster_link": "https://image.tmdb.org/t/p/w500" + data["poster_path"],
            "genres": genres}


async def get_movies_info(movie_ids):
    """
    Fetches details for multiple movies in parallel using TMDB API.

    Args:
        movie_ids (list[int]): A list of TMDB movie identifiers.

    Returns:
        list[dict]: A list of dictionaries containing movie details for all 
                    successfully fetched movies.
    """
    async with httpx.AsyncClient() as client:
        tasks = [get_movie(movie_id, client) for movie_id in movie_ids]
        results = await asyncio.gather(*tasks)  # the star removes the list and returns just the elements : [t1, t2] -> t1, t2
        return [info for info in results if info is not None]
