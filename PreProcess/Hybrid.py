from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle

movies = pd.read_csv('../data/small_movies.csv')

ratings = pd.read_csv('../data/small_ratings.csv')

vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
genres_matrix = vectorizer.fit_transform(movies['genres'])

model = pickle.load(open('../models/svd_model.pkl', 'rb'))

def get_top_n_recommendations(model, user_ratings, top_n=10):
    all_movie_ids = set(movies['movieId'].tolist())
    rated_movie_ids = {rating['movieId'] for rating in user_ratings}
    unrated_movie_ids = all_movie_ids - rated_movie_ids
    testset = [[user_ratings[0]['userId'], movieId, 0] for movieId in
               unrated_movie_ids]

    predictions = model.test(testset)

    predictions.sort(key=lambda x: x.est, reverse=True)
    top_n_movie_ids = [pred.iid for pred in predictions[:top_n]]

    return top_n_movie_ids


def recommend_movies_based_on_genres(genre_matrix, movie_ids_rated_by_user, top_n=10):
    user_profile = genre_matrix[movie_ids_rated_by_user].mean(axis=0)
    cosine_similarities = cosine_similarity(user_profile, genre_matrix)
    similar_indices = cosine_similarities.argsort().flatten()[-top_n - 1:][
                      ::-1]
    recommended_movie_ids = [movies.iloc[index]['movieId'] for index in similar_indices if
                             movies.iloc[index]['movieId'] not in movie_ids_rated_by_user]
    return recommended_movie_ids[:top_n]


def hybrid_recommendation(user_ratings, model, genre_matrix, threshold=5):
    movie_ids_rated_by_user = [rating['movieId'] for rating in user_ratings]

    if len(movie_ids_rated_by_user) < threshold:
        return recommend_movies_based_on_genres(genre_matrix, movie_ids_rated_by_user)

    recommendations = get_top_n_recommendations(model, user_ratings)
    return recommendations



