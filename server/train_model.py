import pandas as pd
import numpy as np
import sys

def get_movies_from_cosine_similarities(all_cosine_similarities, target_user_id : int):
    ratings = pd.read_csv("./datasets/ratings.csv")
    movies = pd.read_csv("./datasets/movies.csv")
    ratings = ratings.pivot(index="userId", columns="movieId", values="rating")
    index = 0
    all_curated_movies_ratings = None
    seen = set()
    while index < all_cosine_similarities.size and index < 3:
        user_id = all_cosine_similarities.iloc[index]["id"]
        # print(f"cos : {user['Cosine Similarity']}")
        
        user_movies = ratings.loc[target_user_id]
        movies_from_closest_user = ratings.loc[user_id]
        movies_from_closest_user = movies_from_closest_user.dropna()
        movies_from_closest_user = movies_from_closest_user[movies_from_closest_user >= 4]
        # movies_from_closest_user = movies_from_closest_user.sort_values()
        movies_from_closest_user = movies_from_closest_user[user_movies.notna()]
        print(movies_from_closest_user)
        curated_movies = movies_from_closest_user[~movies_from_closest_user.index.isin(seen)]
        seen.update(curated_movies.index)
        if all_curated_movies_ratings is None:
            all_curated_movies_ratings = curated_movies
        else:
            all_curated_movies_ratings = pd.concat([all_curated_movies_ratings,  curated_movies], ignore_index=False)
        # print(curated_movies)
        index+=1
    all_curated_movies_ratings = all_curated_movies_ratings.sort_values(ascending=False).index
    print(all_curated_movies_ratings)
    all_curated_movies = movies.set_index("movieId").loc[all_curated_movies_ratings].reset_index()
    print(all_curated_movies)
    return

def main():
    argv = sys.argv
    # print(argv)
    target_user_id = int(argv[1])
    ratings = pd.read_csv("./datasets/ratings.csv")
    ratings = ratings.pivot(
        index="userId",
        columns="movieId",
        values="rating"
    )
    row_of_user = ratings.loc[target_user_id]
    seen_movies_of_user = row_of_user.dropna().index
    ratings = ratings[seen_movies_of_user]
    target_user_seen_movies = ratings.loc[target_user_id]
    all_cosine_similarities = []

    for id, row in ratings.iterrows():
        if id == target_user_id:
            continue
        common_movies_bool = (row.notna() & target_user_seen_movies.notna()).to_numpy()
        # print(common_movies_bool.sum())
        if common_movies_bool.sum() < 10:
            continue
        dot_res = np.dot(row[common_movies_bool], target_user_seen_movies[common_movies_bool])
        length_of_v_user = np.linalg.norm(row[common_movies_bool])
        length_of_v_target_user = np.linalg.norm(target_user_seen_movies[common_movies_bool])
        cosine_similarity = dot_res / (length_of_v_user * length_of_v_target_user)
        all_cosine_similarities.append((id, cosine_similarity))

    all_cosine_similarities = pd.DataFrame(all_cosine_similarities, columns=["id", "Cosine Similarity"])
    sorted = all_cosine_similarities.sort_values(by="Cosine Similarity", ascending=False).reset_index(drop=True)
    get_movies_from_cosine_similarities(sorted, target_user_id)
    
        

    
        
    # common = user_a.notna() & user_b.notna()
    # print(common)
    return

if __name__ == "__main__":
    main()