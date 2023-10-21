import pandas as pd

def extract_data(title):
    found = pd.Series(title).str.extract(r'\((\d{4})\)$', expand=False)
    return found[0] if not found.isna().any() else None

if __name__ == '__main__':
    movies = pd.read_csv('data/small_movies.csv')
    movies['date'] = movies['title'].apply(extract_data)
    movies['title'] = movies['title'].str.replace(r' \(\d{4}\)$', '', regex=True)
    movies.to_csv('data/small_moviesDate.csv', index=False)