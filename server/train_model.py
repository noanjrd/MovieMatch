import pandas as pd
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
    # print(row_of_user)
    seen_movies = row_of_user.dropna().index
    user_movies = user_movies[seen_movies]
    print(user_movies)
    print(user_movies.iloc[user_id])
    return

if __name__ == "__main__":
    main()