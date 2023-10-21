import csv

def extract_genres(filename):
    genres_set = set()

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            genres = row['genres'].split('|')
            genres_set.update(genres)

    return genres_set

if __name__ == '__main__':
    filename = '../data/small_movies.csv'
    genres = extract_genres(filename)
    print("All unique genres:", genres)

