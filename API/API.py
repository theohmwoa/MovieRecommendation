from flask import Flask, request, jsonify
from surprise import Dataset, Reader
from flask_cors import CORS
import pickle
import pandas as pd
import requests
import time
from flask_cors import cross_origin

def load_model(model_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model


API_KEY = "UR_API_KEY"
TMDB_API_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def get_movie_poster_url(title):
    response = requests.get(TMDB_API_URL, params={
        'api_key': API_KEY,
        'query': title
    })

    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return TMDB_IMAGE_URL + poster_path
    return None

def update_model_with_new_ratings(model, new_ratings):
    new_user_id = model.trainset.n_users

    new_ratings_df = pd.DataFrame({
        'userId': new_user_id,
        'movieId': [x['movieId'] for x in new_ratings],
        'rating': [x['rating'] for x in new_ratings],
        'timestamp': int(time.time())
    })

    reader = Reader(rating_scale=(0.5, 5))
    new_data = Dataset.load_from_df(new_ratings_df[['userId', 'movieId', 'rating']], reader)
    new_trainset = new_data.build_full_trainset()

    model.fit(new_trainset)
    return model


app = Flask(__name__)
CORS(app)

model = load_model('../models/best_svd_model-20231019-152417.pkl')

movies = pd.read_csv('../data/small_moviesDate.csv')
movies['date'].fillna(2000, inplace=True)

ratings = pd.read_csv('../data/small_ratings.csv')


@app.route('/next_movie_to_rate', methods=['POST'])
@cross_origin(origin="http://localhost:3000")
def next_movie_to_rate():
    preferred_genres = request.json.get('genres', [])
    start_date = int(request.json.get('start_date', '1900'))
    user_rated_movies = request.json.get('user_rated_movies', [])

    rated_movies_by_user = [rating['movieId'] for rating in user_rated_movies]

    filtered_movies = movies[
        ((movies['date'].astype(int)) >= start_date) &
        (~movies['movieId'].isin(rated_movies_by_user))
        ]
    if preferred_genres:
        filtered_movies = filtered_movies[filtered_movies['genres'].isin(preferred_genres)]

    movie_stats = ratings[ratings['movieId'].isin(filtered_movies['movieId'])].groupby('movieId').rating.agg(
        ['var', 'count'])

    movie_stats['var'] = (movie_stats['var'] - movie_stats['var'].min()) / (
                movie_stats['var'].max() - movie_stats['var'].min())
    movie_stats['count'] = (movie_stats['count'] - movie_stats['count'].min()) / (
                movie_stats['count'].max() - movie_stats['count'].min())

    movie_stats['score'] = 0.6 * movie_stats['var'] + 0.4 * movie_stats['count']

    top_movie_id = movie_stats['score'].idxmax()
    top_movie = movies[movies['movieId'] == top_movie_id].iloc[0]

    movie_poster = get_movie_poster_url(top_movie['title'])

    return jsonify({
        'movieId': int(top_movie['movieId']),
        'title': top_movie['title'],
        'genres': top_movie['genres'],
        'date': top_movie['date'],
        'poster': movie_poster
    })


@app.route('/recommend_movie', methods=['POST'])
@cross_origin(origin="http://localhost:3000")
def recommend_movie():
    global model
    user_rated_movies = request.json.get('user_rated_movies', [])
    preferred_genres = request.json.get('genres', [])
    start_date = int(request.json.get('start_date', '1900'))

    user_rated_movies = [movie for movie in user_rated_movies if movie['rating'] != -1]

    user_ratings_df = pd.DataFrame(user_rated_movies)

    rated_movie_ids = user_ratings_df['movieId'].tolist()

    model = update_model_with_new_ratings(model, user_rated_movies)

    candidate_movies = movies[
        (~movies['movieId'].isin(rated_movie_ids)) &
        (movies['date'] >= start_date)
        ]
    if preferred_genres:
        pattern = '|'.join(preferred_genres)
        candidate_movies = candidate_movies[candidate_movies['genres'].str.contains(pattern)]

    predictions = []
    for _, movie in candidate_movies.iterrows():
        prediction = model.predict(uid=0, iid=movie['movieId'])
        predictions.append((movie['movieId'], prediction.est))

    top_movie_id = max(predictions, key=lambda x: x[1])[0]
    top_movie = movies[movies['movieId'] == top_movie_id].iloc[0]

    movie_poster = get_movie_poster_url(top_movie['title'])

    return jsonify({
        'movieId': int(top_movie['movieId']),
        'title': top_movie['title'],
        'genres': top_movie['genres'],
        'date': int(top_movie['date']),
        'poster': movie_poster
    })


if __name__ == '__main__':
    app.run(debug=True)

