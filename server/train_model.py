import pandas as pd


def main():
    try:
        movies = pd.read_csv("./datasets/links.csv")
        ratings = pd.read_csv("./datasets/ratings.csv")
        print(movies.head)
    except:
        print("Error")
        exit(1)
    return

if __name__ == "__main__":
    main()