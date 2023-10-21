import pandas as pd


def extract_year(title):
    year = title.strip()[-5:-1]
    if year.isdigit():
        return int(year)
    return None


def calculate_movie_variance(input_csv, chosenGenres, year_threshold, output_csv):
    ratings = pd.read_csv(input_csv)

    movies = pd.read_csv('data/movies.csv')

    movies['year'] = movies['title'].apply(extract_year)

    movies = movies[movies['year'] > year_threshold]

    merged_df = pd.merge(ratings, movies, on='movieId', how='inner')

    filtered_movies = merged_df[merged_df['genres'].str.contains('|'.join(chosenGenres))]

    variance_data = filtered_movies.groupby(['movieId', 'title']).agg({
        'rating': ['var', 'count']
    }).reset_index()
    variance_data.columns = ['movieId', 'title', 'rating_variance', 'rating_count']

    variance_data = variance_data.sort_values(by=['rating_variance', 'rating_count'], ascending=[False, False])

    variance_data.to_csv(output_csv, index=False)


if __name__ == '__main__':
    calculate_movie_variance('small_ratings.csv', ['Comedy', 'Sci-Fi', 'Animation'], 2015, 'movie_variance.csv')
