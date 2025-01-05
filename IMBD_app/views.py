from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Genre, Movie, Actor, Director
from .forms import ActorForm, DirectorForm, MovieForm
from .utils.tmdb import fetch_tmdb_data, fetch_movie_from_tmdb, fetch_director_from_tmdb, fetch_actor_from_tmdb
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User 

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

# Function to fetch movie credits (cast and crew)
def fetch_movie_credits(movie_id):
    return fetch_tmdb_data(f"movie/{movie_id}/credits", params={"language": "en-US"})

# Details of a specific movie 
# In views.py
def movie_details(request, pk):
    movie = Movie.objects.filter(tmdb_id=pk).first()

    if not movie:
        movie = fetch_movie_from_tmdb(pk)

    genres = movie.genres.all()
    directors = movie.directors.all()
    top_actors = movie.movie_actors.all()[:5]

    return render(request, "movies/movie_details.html", {
        "movie": movie,
        "genres": genres if genres else ["No Genre Information Available"],
        "directors": directors if directors else ["No Director Information Available"],
        "cast": top_actors if top_actors else ["No Actor Information Available"],
    })








# Actor Details (with database saving)
def actor_details(request, pk):
    # Check if the actor exists in the database
    actor = Actor.objects.filter(tmdb_id=pk).first()

    if not actor:
        # Fetch and store actor in the database if not found
        actor = fetch_actor_from_tmdb(pk)

    if not actor:  # If actor is still None, handle gracefully
        actor = Actor(name="Unknown Actor", biography="Biography not available")
    
    # Get the top movies the actor is known for with prefetch_related to fetch genres, directors, and actors
    top_movies = actor.known_for_movies.prefetch_related(
        'genres',  # Prefetch genres related to the movie
        'directors',  # Prefetch directors related to the movie
        'movie_actors__actor'  # Prefetch actors related to the movie
    )[:5]  # Limit to top 5 movies

    return render(request, "actors/actor_details.html", {
        "actor": actor,
        "top_movies": top_movies,
    })




# Director Details (with database saving)
def director_details(request, pk):
    # Fetch director details
    director = fetch_tmdb_data(f"person/{pk}", params={"language": "en-US"})
    
    # Fetch director's movie credits (directed works)
    movie_credits = fetch_tmdb_data(f"person/{pk}/movie_credits", params={"language": "en-US"})
    
    # Get the top 5 movies the director has directed
    top_movies = movie_credits.get('crew', [])[:5]  # Limiting to the top 5 directed movies
    
    # Remove duplicates based on movie id (TMDb ID)
    unique_movies = []
    seen_ids = set()
    for movie in top_movies:
        if movie['id'] not in seen_ids:
            unique_movies.append(movie)
            seen_ids.add(movie['id'])

    return render(request, "directors/director_details.html", {
        "director": director,
        "top_movies": unique_movies,  # Use unique movies in the template
    })





# Login Page (renamed to user_login to avoid conflict with built-in login function)
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in using Django's built-in login function
            auth_login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('IMBD_app:home')  # Redirect to home page or another view
        else:
            # Check if the username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username not found.")
            else:
                messages.error(request, "Incorrect password.")
    return render(request, 'auth/login.html')

# Signup Page
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            # Create new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('user_login')  # Redirect to login page after successful signup
    return render(request, 'auth/signup.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('IMBD_app:home')  # Redirect to the home page after logout

def search_results(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'movie')  # Default to 'movie' if no category is selected

    results = {
        'movies': [],
        'actors': [],
        'directors': [],
        'genres': [],
    }

    # Wenn ein Suchbegriff angegeben ist, filtere die entsprechenden Modelle
    if query:
        if category == 'movie':
            results['movies'] = Movie.objects.filter(title__icontains=query)
        elif category == 'actor':
            results['actors'] = Actor.objects.filter(name__icontains=query)
        elif category == 'director':
            results['directors'] = Director.objects.filter(name__icontains=query)
        elif category == 'genre':
            results['genres'] = Genre.objects.filter(name__icontains=query)
    
    return render(request, 'IMBD_app/search_results.html', {
        'query': query,
        'category': category,
        'results': results,
    })


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




# alles für search bar

def movie_list(request):
    query = request.GET.get('q', '').strip()  # Search term
    category = request.GET.get('category', 'movie')  # Default category: "movie"

    # Query local database
    movies_db = Movie.objects.none()

    # Fetch movies from TMDb
    movies_tmdb = []

    if query:
        # Filter local movies
        movies_db = Movie.objects.filter(
            Q(title__icontains=query) | Q(genres__name__icontains=query)
        ).distinct()

        # Search movies on TMDb
        tmdb_response = fetch_tmdb_data("search/movie", params={"query": query})
        movies_tmdb = tmdb_response.get("results", [])

    context = {
        "query": query,
        "category": category,
        "movies_db": movies_db,
        "movies_tmdb": movies_tmdb,
    }
    return render(request, "movies/movie_list.html", context)



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
                Q(name__icontains=query)
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


# TODO
# List of all actors (mock data)
def actor_list(request):
    query = request.GET.get('q', '').strip()  # Suchbegriff
    category = request.GET.get('category', 'actor')  # Standardkategorie "actor"

    # Datenbankabfragen
    actors_db = Actor.objects.none()

    # TMDB-Abfragen
    actors_tmdb = []

    if query:
            # Lokale Schauspieler filtern
            actors_db = Actor.objects.filter(
                Q(name__icontains=query)
            )
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