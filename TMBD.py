import csv
import requests
import re

API_KEY = "13ff48a90ad91c9b9b2246a87f9f6cd4"
TMDB_API_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def clean_title(title):
    # Removes patterns like (1995) from the title
    cleaned = re.sub(r'\(\d{4}\)$', '', title).strip()
    return cleaned


def get_movie_poster_url(title):
    title = clean_title(title)
    response = requests.get(TMDB_API_URL, params={
        'api_key': API_KEY,
        'query': title
    })

    data = response.json()
    if data['results']:
        # Assuming the first result is the most relevant
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return TMDB_IMAGE_URL + poster_path
    return None


def add_images_to_csv(input_filename, output_filename):
    with open(input_filename, mode='r') as infile, open(output_filename, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['image_url']

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            print(f"Fetching image for {row['title']}...")
            row['image_url'] = get_movie_poster_url(row['title'])
            print(f"Image URL: {row['image_url']}")
            writer.writerow(row)


input_file = "data/movies.csv"
output_file = "data/output_with_images.csv"
add_images_to_csv(input_file, output_file)
