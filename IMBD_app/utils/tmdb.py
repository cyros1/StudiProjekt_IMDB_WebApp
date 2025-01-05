from datetime import timedelta
from django.utils.timezone import now
from ..models import Movie, Genre, Actor, Director, CachedData, MovieActor
import requests

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "2af4d814ca966334015aa4ea035219e7"

def fetch_tmdb_data(endpoint, params=None):
    """
    Fetch data from TMDb API.
    :param endpoint: API endpoint (e.g., 'movie/popular', 'search/movie').
    :param params: Dictionary of additional parameters.
    :return: JSON response or None if the request fails.
    """
    if params is None:
        params = {}

    params['api_key'] = API_KEY
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

        # Create or update the movie
        movie, created = Movie.objects.update_or_create(
            tmdb_id=movie_data["id"],
            defaults={
                "title": movie_data["title"],
                "release_date": movie_data["release_date"],
                "backdrop_path": movie_data["backdrop_path"],
                "overview": movie_data["overview"],
                "rating": movie_data["vote_average"],
                "cached_at": now()
            }
        )

        # Update genres
        for genre_data in movie_data.get("genres", []):
            genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
            movie.genres.add(genre)

        # Update directors
        credits = movie_data.get("credits", {})
        for crew in credits.get("crew", []):
            if crew["job"] == "Director":
                director, _ = Director.objects.update_or_create(
                    tmdb_id=crew["id"],
                    defaults={"name": crew["name"], "profile_path": crew["profile_path"]}
                )
                movie.directors.add(director)

        # Update actors and associate them with the movie
        # Update actors
        top_actors = credits.get("cast", [])[:5]
        for actor_data in top_actors:
            actor, _ = Actor.objects.update_or_create(
                tmdb_id=actor_data["id"],
                defaults={
                    "name": actor_data["name"],
                    "profile_path": actor_data["profile_path"]
                }
            )
            # Create the MovieActor association
            MovieActor.objects.update_or_create(movie=movie, actor=actor)


        movie.save()  # Save the movie after updating everything
        return movie
    else:
        response.raise_for_status()


