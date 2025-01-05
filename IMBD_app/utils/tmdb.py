from datetime import timedelta
from django.utils.timezone import now
from ..models import Movie, Genre, Actor, Director, CachedData, MovieActor
import requests

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
        movie.movie_actors.all().delete()
        top_actors = credits.get("cast", [])[:5]
        for actor_data in top_actors:
            actor, _ = Actor.objects.update_or_create(
                tmdb_id=actor_data.get("id"),
                defaults={
                    "name": actor_data.get("name", "No Name Available"),
                    "profile_path": actor_data.get("profile_path", "")
                }
            )
            MovieActor.objects.create(
                movie=movie,
                actor=actor,
                role=actor_data.get("character", "No Role Available")
            )

        movie.save()
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
                release_date = movie_data.get("release_date", None)
                
                # If release_date is an empty string, set it to None
                if release_date == "":
                    release_date = None

                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_data["id"],
                    defaults={
                        "title": movie_data["title"],
                        "release_date": release_date,  # Set None if empty string
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

        # Ensure there is valid actor data
        if not actor_data.get("name"):
            return None

        # Create or update actor in the database
        actor, created = Actor.objects.update_or_create(
            tmdb_id=actor_data["id"],
            defaults={
                "name": actor_data["name"],
                "profile_path": actor_data.get("profile_path", ""),
                "biography": actor_data.get("biography", "Biography not available")
            }
        )

        # Fetch the actor's movie credits (known for movies)
        movie_credits = fetch_tmdb_data(f"person/{actor_id}/movie_credits", params={"language": "en-US"})
        known_for_movies = movie_credits.get('cast', [])

        # Add or update the movies the actor is known for
        for movie_data in known_for_movies:
            # Fetch additional movie details (like genres, directors)
            movie_detail = fetch_tmdb_data(f"movie/{movie_data['id']}", params={"append_to_response": "credits,genres"})
            if movie_detail:
                release_date = movie_detail.get("release_date", None)

                # If release_date is an empty string, set it to None
                if release_date == "":
                    release_date = None

                movie, _ = Movie.objects.update_or_create(
                    tmdb_id=movie_detail["id"],
                    defaults={
                        "title": movie_detail.get("title", "No Title Available"),
                        "release_date": release_date,  # Set None if empty string
                        "backdrop_path": movie_detail.get("backdrop_path", ""),
                        "overview": movie_detail.get("overview", "No Overview Available"),
                        "rating": movie_detail.get("vote_average", 0)
                    }
                )

                # Update genres
                movie.genres.clear()
                for genre_data in movie_detail.get("genres", []):
                    genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
                    movie.genres.add(genre)

                # Update directors
                movie.directors.clear()
                for crew_member in movie_detail.get("credits", {}).get("crew", []):
                    if crew_member["job"] == "Director":
                        director, _ = Director.objects.get_or_create(
                            tmdb_id=crew_member["id"],
                            defaults={"name": crew_member["name"], "profile_path": crew_member.get("profile_path")}
                        )
                        movie.directors.add(director)

                # Now associate the actor with the movie
                actor.known_for_movies.add(movie)

        # Return the actor object
        return actor

    else:
        print(f"Error fetching actor data: {response.status_code}")
        return None



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




