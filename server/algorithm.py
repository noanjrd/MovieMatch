import pandas as pd
import numpy as np
import sys


def get_movies_seen_by_user(user_id : int):
    try:
        ratings = pd.read_csv("./datasets/ratings.csv")
        ratings = ratings[ratings["userId"] == user_id]
        if ratings.size == 0:
            return None
        ratings = ratings[ratings["rating"] >= 4]
        movies_id = ratings["movieId"]
        movies_id = movies_id.head(8)
        return return_tmdb_ids(movies_id)
    except Exception:
        return  None

def return_tmdb_ids(movies_id):
    tmdb_links = pd.read_csv("./datasets/links.csv")
    tmdb_links = tmdb_links[tmdb_links["movieId"].isin(movies_id)]
    return tmdb_links["tmdbId"]

def get_movies_from_cosine_similarities(ratings :pd.DataFrame, all_cosine_similarities, target_user_id : int):
    movies = pd.read_csv("./datasets/movies.csv")
    all_curated_movies_ratings = None
    movies_seen_by_user = ratings.loc[target_user_id].dropna().index
    seen = set(movies_seen_by_user)
    index = 0
    while index < all_cosine_similarities.size and (len(seen) - len(movies_seen_by_user)) < 50 :
        user_id = all_cosine_similarities.iloc[index]["id"]
        movies_from_closest_user = ratings.loc[user_id]
        movies_from_closest_user = movies_from_closest_user.dropna()
        movies_from_closest_user = movies_from_closest_user[movies_from_closest_user >= 4]
        curated_movies = movies_from_closest_user[~movies_from_closest_user.index.isin(seen)]
        seen.update(curated_movies.index)
        if all_curated_movies_ratings is None:
            all_curated_movies_ratings = curated_movies
        else:
            all_curated_movies_ratings = pd.concat([all_curated_movies_ratings,  curated_movies], ignore_index=False)
        index+=1

    all_curated_movies_ratings = all_curated_movies_ratings.sort_values(ascending=False).index
    all_curated_movies = movies.set_index("movieId").loc[all_curated_movies_ratings].reset_index()
    return return_tmdb_ids(all_curated_movies["movieId"][:20])

def start_algo(target_user_id: int):
    try:
        ratings = pd.read_csv("./datasets/ratings.csv")
        ratings = ratings.pivot(
            index="userId",
            columns="movieId",
            values="rating"
        )
        row_of_user = ratings.loc[target_user_id]
        seen_movies_of_user = row_of_user.dropna().index
        seen_movies_ratings = ratings[seen_movies_of_user]
        seen_movies_ratings = seen_movies_ratings.sub(seen_movies_ratings.mean(axis=1), axis=0) # Centering values
        target_user_seen_movies = seen_movies_ratings.loc[target_user_id]

        #  Getting all the cosine similarities
        all_cosine_similarities = []
        for id, row in seen_movies_ratings.iterrows():
            if id == target_user_id:
                continue
            common_movies_bool = (row.notna() & target_user_seen_movies.notna()).to_numpy()
            if common_movies_bool.sum() < 15:
                continue
            dot_res = np.dot(row[common_movies_bool], target_user_seen_movies[common_movies_bool])
            length_vector_user = np.linalg.norm(row[common_movies_bool])
            length_vector_target_user = np.linalg.norm(target_user_seen_movies[common_movies_bool])
            cosine_similarity = dot_res / (length_vector_user * length_vector_target_user)
            all_cosine_similarities.append((id, cosine_similarity))

        all_cosine_similarities = pd.DataFrame(all_cosine_similarities, columns=["id", "Cosine Similarity"])
        sorted = all_cosine_similarities.sort_values(by="Cosine Similarity", ascending=False).reset_index(drop=True)
        return get_movies_from_cosine_similarities(ratings, sorted, target_user_id)
    except Exception:
        return None

def main():
    argv = sys.argv
    target_user_id = int(argv[1])
    print(start_algo(target_user_id))
    return

if __name__ == "__main__":
    main()