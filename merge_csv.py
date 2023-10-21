import pandas as pd

def merge_csv(input_csv1, input_csv2, output_csv):
    movies = pd.read_csv(input_csv1)
    ratings = pd.read_csv(input_csv2)

    movies = movies.merge(ratings, on='movieId', how='inner')
    movies.to_csv(output_csv, index=False)

if __name__ == '__main__':
    merge_csv('small_movies.csv', 'small_ratings.csv', 'small_merged.csv')