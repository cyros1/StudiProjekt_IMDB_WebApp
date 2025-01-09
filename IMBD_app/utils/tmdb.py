from datetime import timedelta
from django.utils.timezone import now
from ..models import Movie, Genre, Actor, Director, CachedData
import requests
import random, string

API_KEY = "2af4d814ca966334015aa4ea035219e7"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_tmdb_data(endpoint, params=None, page=1):
    """
    Fetch data from TMDb API with optional pagination.
    :param endpoint: API endpoint (e.g., 'movie/popular', 'search/movie').
    :param params: Dictionary of additional parameters.
    :param page: Page number to fetch (default is 1).
    :return: JSON response or None if the request fails.
    """
    if params is None:
        params = {}

    params['api_key'] = API_KEY
    params['page'] = page  # Adding page parameter for pagination
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching TMDb data: {response.status_code}")
        return None



def fetch_movie_from_tmdb(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "append_to_response": "credits"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        movie_data = response.json()

        # Handle case where Date from api = ""
        release_date = movie_data.get("release_date") or None

        # Create or update the movie
        movie, created = Movie.objects.update_or_create(
            tmdb_id=movie_data.get("id"),
            defaults={
                "title": movie_data.get("title", "No Title Available"),
                "release_date": release_date,
                "backdrop_path": movie_data.get("backdrop_path", ""),
                "overview": movie_data.get("overview", "No Overview Available"),
                "rating": movie_data.get("vote_average", 0),
                "cached_at": now()
            }
        )

        # Update genres
        movie.genres.clear()
        for genre_data in movie_data.get("genres", []):
            genre, _ = Genre.objects.get_or_create(name=genre_data.get("name", "Unknown Genre"))
            movie.genres.add(genre)

        # Update directors
        movie.directors.clear()
        credits = movie_data.get("credits", {})
        for crew in credits.get("crew", []):
            if crew["job"] == "Director":
                director, _ = Director.objects.update_or_create(
                    tmdb_id=crew.get("id"),
                    defaults={"name": crew.get("name", "No Name Available"), "profile_path": crew.get("profile_path", "")}
                )
                movie.directors.add(director)

        # Update actors and roles
        movie.actors.clear()
        actors = credits.get("cast", [])[:5]
        for actor_data in actors:
            actors, _  = Actor.objects.update_or_create(
                tmdb_id=actor_data.get("id"),
                defaults={
                    "name": actor_data.get("name", "No Name Available"),
                    "profile_path": actor_data.get("profile_path", "")
                }
            )
            movie.actors.add(actors)

        movie.save()
        return movie
    else:
        response.raise_for_status()

def retrieve_500_pages(endpoint):
    """
    Retrieve data across 500 pages from a given endpoint (e.g., 'movie/popular').
    :param endpoint: The endpoint to query (e.g., 'movie/popular', 'search/movie').
    :return: List of all movie data across all 500 pages.
    """
    all_movies = []
    page = 1

    # Loop to retrieve movies from 500 pages
    while page <= 500:
        data = fetch_tmdb_data(endpoint, page=page)

        if data and 'results' in data:
            all_movies.extend(data['results'])
            # Check if there are more pages, otherwise break
            total_pages = data.get('total_pages', 0)
            if page >= total_pages:
                break  # Exit loop if we have retrieved all pages
            page += 1
        else:
            break  # Stop if there's no data or an error occurs

    return all_movies

def generate_custom_id():
    custom_id = ''.join(random.choices(string.ascii_uppercase, k=6))  # Generate a random 6-letter ID
    while Actor.objects.filter(custom_id=custom_id).exists():  # Ensure the custom_id is unique
        custom_id = ''.join(random.choices(string.ascii_uppercase, k=6))  # Regenerate if exists
    return custom_id


