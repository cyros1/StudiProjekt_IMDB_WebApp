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



# Fetch Directors from TMDb-API
def fetch_director_from_tmdb(director_id):
    """
    Fetch director details and their movie credits from TMDb API.
    :param director_id: TMDb director ID.
    :return: Director object (from the database) or None if the request fails.
    """
    # Fetch director data
    url = f"{BASE_URL}/person/{director_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        director_data = response.json()

        # Create or update director in the database
        director, created = Director.objects.update_or_create(
            tmdb_id=director_data["id"],
            defaults={
                "name": director_data["name"],
                "profile_path": director_data["profile_path"],
                "biography": director_data["biography"]
            }
        )

        # Fetch the director's movie credits (directed movies)
        movie_credits = fetch_tmdb_data(f"person/{director_id}/movie_credits", params={"language": "en-US"})
        directed_movies = movie_credits.get('crew', [])

        # Add or update only those movies where the director is actually listed as the director
        for movie_data in directed_movies:
            if movie_data['job'] == 'Director':  # Ensure it is a directed movie
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_data["id"],
                    defaults={
                        "title": movie_data["title"],
                        "release_date": movie_data["release_date"],
                        "backdrop_path": movie_data["backdrop_path"],
                        "overview": movie_data["overview"],
                        "rating": movie_data["vote_average"]
                    }
                )
                director.movies.add(movie)  # Associate director with the movie

        # Return the director object
        return director

    else:
        print(f"Error fetching director data: {response.status_code}")
        return None


    

# Fetch Actor details from TMDb-API
def fetch_actor_from_tmdb(actor_id):
    """
    Fetch actor details and their movie credits (known for) from TMDb API.
    :param actor_id: TMDb actor ID.
    :return: Actor object (from the database) or None if the request fails.
    """
    # Fetch actor data
    url = f"{BASE_URL}/person/{actor_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        actor_data = response.json()

        # Create or update actor in the database
        actor, created = Actor.objects.update_or_create(
            tmdb_id=actor_data["id"],
            defaults={
                "name": actor_data["name"],
                "profile_path": actor_data["profile_path"],
                "biography": actor_data["biography"]
            }
        )

        # Fetch the actor's movie credits (known for movies)
        movie_credits = fetch_tmdb_data(f"person/{actor_id}/movie_credits", params={"language": "en-US"})
        known_for_movies = movie_credits.get('cast', [])

        # Add or update the movies the actor is known for
        for movie_data in known_for_movies:
            movie, _ = Movie.objects.update_or_create(
                tmdb_id=movie_data["id"],
                defaults={
                    "title": movie_data["title"],
                    "release_date": movie_data["release_date"],
                    "backdrop_path": movie_data["backdrop_path"],
                    "overview": movie_data["overview"],
                    "rating": movie_data["vote_average"]
                }
            )
            actor.known_for_movies.add(movie)  # Associate actor with the movie

        # Return the actor object
        return actor

    else:
        print(f"Error fetching actor data: {response.status_code}")
        return None

