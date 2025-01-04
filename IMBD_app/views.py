from django.shortcuts import render
from django.db.models import Q
from .models import Movie, Actor, Director
from .forms import ActorForm, DirectorForm, MovieForm
from .utils.tmdb import fetch_tmdb_data
import requests

# Create your views here.

from django.shortcuts import render

# Home Page
def home(request):
    # Fetch top movies
    top_movies = fetch_tmdb_data("movie/popular", params={"language": "en-US", "page": 1})

    # Round vote_average for each movie
    for movie in top_movies.get("results", []):
        movie['vote_average'] = round(movie['vote_average'], 1)  # Round to 1 decimal place

    
    # TMDB only provides endpoint for persons, the specifics (actor/director) have to be filtered out from the json
    top_people = fetch_tmdb_data("person/popular", params={"language": "en-US", "page": 1})

    top_actors = [
        person for person in top_people.get("results", [])
        if person.get("known_for_department") == "Acting"
    ]

    top_directors = [
        person for person in top_people.get("results", [])
        if person.get("known_for_department") == "Directing"
    ]

    return render(request, "home.html", {
        "top_movies": top_movies.get("results", []),
        "top_actors": top_actors,
        "top_directors" : top_directors
    })



# TODO
# List of all movies
def movie_list(request):
    query = request.GET.get('q', '').strip()  # Suchbegriff
    category = request.GET.get('category', 'movie')  # Standardkategorie "movie"

    # Datenbankabfragen
    movies_db = Movie.objects.none()

    # TMDB-Abfragen
    movies_tmdb = []

    if query:
            # Lokale Filme filtern
            movies_db = Movie.objects.filter(
                Q(title__icontains=query) | Q(genre__icontains=query)
            )
            # TMDB-Filme suchen
            tmdb_response = fetch_tmdb_data("search/movie", params={"query": query})
            movies_tmdb = tmdb_response.get("results", [])


    context = {
        "query": query,
        "category": category,
        "movies_db": movies_db,
        "movies_tmdb": movies_tmdb,
    }
    return render(request, "movies/movie_list.html", context)



# Function to fetch movie credits (cast and crew)
def fetch_movie_credits(movie_id):
    return fetch_tmdb_data(f"movie/{movie_id}/credits", params={"language": "en-US"})

# Details of a specific movie 
def movie_details(request, pk):
    movie = fetch_tmdb_data(f"movie/{pk}", params={"language": "en-US"})

    # Fetch movie credits:
    credits = fetch_movie_credits(pk)
    cast = credits.get('cast', [])
    crew = credits.get('crew', [])

    # Get director from the crew
    directors = [member['name'] for member in crew if member['job'] == 'Director']
    # Select only top 5 actors
    top_actors = cast[:5] 

    return render(request, "movies/movie_details.html", {
        "movie": movie,
        "cast": top_actors,
        "directors": directors,
    })






# TODO
# List of all actors (mock data)
def actor_list(request):
    query = request.GET.get('q', '').strip()  # Suchbegriff
    category = request.GET.get('category', 'actor')  # Standardkategorie "movie"

    # Datenbankabfragen
    actors_db = Actor.objects.none()

    # TMDB-Abfragen
    actors_tmdb = []

    if query:
            # Lokale Schauspieler filtern
            actors_db = Actor.objects.filter(
                Q(name__icontains=query) | Q(surname__icontains=query)
            ).order_by('name')  # Sortiere nach Namen (alphabetisch)
            # TMDB-Personen suchen
            tmdb_response = fetch_tmdb_data("search/person", params={"query": query})
            actors_tmdb = [
                person for person in tmdb_response.get("results", [])
                if person.get("known_for_department") == "Acting"
            ]

    context = {
        "query": query,
        "category": category,
        "actors_db": actors_db,
        "actors_tmdb": actors_tmdb,
    }
    return render(request, "actors/actor_list.html", context)


# Details of a specific actor
def actor_details(request, pk):
    # Fetch actor details
    actor = fetch_tmdb_data(f"person/{pk}", params={"language": "en-US"})
    
    # Fetch actor's movie credits (known for roles)
    movie_credits = fetch_tmdb_data(f"person/{pk}/movie_credits", params={"language": "en-US"})
    
    # Get the top 5 movies the actor is known for
    top_movies = movie_credits.get('cast', [])[:5]  # Limiting to the top 5 movies

    return render(request, "actors/actor_details.html", {
        "actor": actor,
        "top_movies": top_movies,
    })




# TODO
# List of all directors (mock data)
def director_list(request):
    query = request.GET.get('q', '').strip()  # Suchbegriff
    category = request.GET.get('category', 'director')  # Standardkategorie "movie"

    # Datenbankabfragen
    directors_db = Director.objects.none()

    # TMDB-Abfragen
    directors_tmdb = []

    if query:
            # Lokale Regisseure filtern
            directors_db = Director.objects.filter(
                Q(name__icontains=query) | Q(surname__icontains=query)
            )
            # TMDB-Personen suchen
            tmdb_response = fetch_tmdb_data("search/person", params={"query": query})
            directors_tmdb = [
                person for person in tmdb_response.get("results", [])
                if person.get("known_for_department") == "Directing"
            ]

    context = {
        "query": query,
        "category": category,
        "directors_db": directors_db,
        "directors_tmdb": directors_tmdb,
    }
    return render(request, "directors/director_list.html", context)


# Details of a specific director 
def director_details(request, pk):
    # Fetch director details
    director = fetch_tmdb_data(f"person/{pk}", params={"language": "en-US"})
    
    # Fetch director's movie credits (directed works)
    movie_credits = fetch_tmdb_data(f"person/{pk}/movie_credits", params={"language": "en-US"})
    
    # Get the top 5 movies the director has directed
    top_movies = movie_credits.get('crew', [])[:5]  # Limiting to the top 5 directed movies

    return render(request, "directors/director_details.html", {
        "director": director,
        "top_movies": top_movies,
    })






# Login Page
def login(request):
    return render(request, "auth/login.html")

# Signup Page
def signup(request):
    return render(request, "auth/signup.html")



def create(request):
    actor_form = ActorForm()
    director_form = DirectorForm()
    movie_form = MovieForm()

    if request.method == 'POST':
        # Formulartyp aus den POST-Daten lesen
        form_type = request.POST.get('form_type')
        print(f"Form type received: {form_type}")  # Debugging-Ausgabe

        if form_type == 'actor':
            actor_form = ActorForm(request.POST, request.FILES)
            if actor_form.is_valid():
                actor_form.save()
                print("Actor created successfully!")  # Debugging-Ausgabe
                return render(request, 'success.html')  # Erfolgsseite
            else:
                print("ERROR: Actor couldn't be created")
        elif form_type == 'director':
            director_form = DirectorForm(request.POST, request.FILES)
            if director_form.is_valid():
                director_form.save()
                print("Director created successfully!")  # Debugging-Ausgabe
                return render(request, 'success.html')  # Erfolgsseite
            else:
                print("ERROR: Director couldn't be created")
        elif form_type == 'movie':
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                movie_form.save()
                print("Movie created successfully!")  # Debugging-Ausgabe
                return render(request, 'success.html')  # Erfolgsseite
            else:
                print("ERROR: Movie couldn't be created")
            
    return render(request, 'create.html', {
        'actor_form': actor_form,
        'director_form': director_form,
        'movie_form': movie_form,
    })

def success(request):
    return render(request, "success.html")


# daten in views übergeben
# from .models import Film

# def film_list(request):
#     filme = Film.objects.all()
#     return render(request, "film.html", {"filme": filme})


# #dann django admin oder shell nutzen um daten zu erstellen:
# python manage.py shell

# from IMBD_app.models import Film
# Film.objects.create(titel="Inception", veroeffentlichungsdatum="2010-07-16", genre="Science Fiction", beschreibung="Ein Dieb stiehlt Ideen aus Träumen.")
