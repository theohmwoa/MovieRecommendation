import requests

data = {
    'genres': ['Comedy', 'Animation'],
    'start_date': '2015',
    'user_rated_movies': [
        {
            'movieId': 1,
            'rating': 5
        },
    ]
}

response = requests.post('http://localhost:5000/recommend_movie', json=data)

print(response.json())