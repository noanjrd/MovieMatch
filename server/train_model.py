import pandas as pd
import numpy as np
import sys

def main():
    argv = sys.argv
    print(argv)
    user_id = int(argv[1])
    movies = pd.read_csv("./datasets/links.csv")
    ratings = pd.read_csv("./datasets/ratings.csv")
    # print(movies.head)
    user_movies = ratings.pivot(
        index="userId",
        columns="movieId",
        values="rating"
    )
    row_of_user = user_movies.loc[user_id]
    seen_movies = row_of_user.dropna().index
    print(seen_movies)
    user_movies = user_movies[seen_movies]
    print(user_movies)
    user_a = user_movies.loc[user_id]
    user_b = user_movies
    for id, row in user_movies.iterrows():
        # print(id)
        # print(row.notna())
        if id == user_id:
            continue
        common  = row.notna() & user_a.notna()
        com_t = common[common == True]
        
        # print(com_t)
        # print(common[common["movieId"] == True])
        # print(com_t)
        if com_t.size < 10:
            continue
        dot_res = np.dot(row[common], user_a[common])
        l = np.linalg.norm(row[common])
        l2 = np.linalg.norm(user_a[common])
        cos = dot_res / (l * l2)
        print(id, cos)
        
        # print(common)
        
    # common = user_a.notna() & user_b.notna()
    # print(common)
    return

if __name__ == "__main__":
    main()