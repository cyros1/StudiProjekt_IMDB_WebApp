from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Genre, Movie, Actor, Director
from .forms import ActorForm, DirectorForm, MovieForm, UserCommentForm, UserRatingForm
from .utils.tmdb import fetch_tmdb_data, fetch_movie_from_tmdb, fetch_actor_from_tmdb, fetch_director_from_tmdb
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User 
from django.db.models import Avg
from .forms import UserCommentForm, UserRatingForm
from .models import Movie, Watchlist
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
# Details of a specific movie 
def movie_details(request, pk):  
    # Hole den Film aus der Datenbank oder von TMDB
    movie = Movie.objects.filter(tmdb_id=pk).first()

    if not movie:
        movie = fetch_movie_from_tmdb(pk)

    # Hole die API-Bewertung
    genres = movie.genres.all()
    directors = movie.directors.all()
    top_actors = movie.movie_actors.all()[:5]

    # Hole Kommentare und User-Bewertung
    comments = movie.comments.select_related('user').order_by('-created_at')
    ratings = movie.ratings.all()
    user_average_rating = ratings.aggregate(average=Avg('rating'))['average']

    # Benutzer-Watchlist abrufen (Liste der tmdb_id-Werte)
    user_watchlist = list(
        Watchlist.objects.filter(user=request.user).values_list('movie__tmdb_id', flat=True)
    ) if request.user.is_authenticated else []

    # POST-Anfrage bearbeiten
    if request.method == 'POST' and request.user.is_authenticated:
        # Wenn der Button für Watchlist verwendet wird
        if 'add_to_watchlist' in request.POST or 'remove_from_watchlist' in request.POST:
            # Film zur Watchlist hinzufügen oder entfernen
            if movie.tmdb_id in user_watchlist:
                Watchlist.objects.filter(user=request.user, movie=movie).delete()
                messages.success(request, f"'{movie.title}' wurde aus Ihrer Watchlist entfernt.")
            else:
                Watchlist.objects.create(user=request.user, movie=movie)
                messages.success(request, f"'{movie.title}' wurde Ihrer Watchlist hinzugefügt.")

            # Nach der Änderung der Watchlist zurück zur Detailseite
            return redirect('IMBD_app:movie_details', pk=pk)

        # Kommentare und Bewertungen speichern
        comment_form = UserCommentForm(request.POST)
        rating_form = UserRatingForm(request.POST)

        if comment_form.is_valid() and rating_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.user = request.user
            new_comment.rating = rating_form.cleaned_data['rating']
            new_comment.save()

            new_rating = rating_form.save(commit=False)
            new_rating.movie = movie
            new_rating.user = request.user
            new_rating.save()

            messages.success(request, "Your comment and rating have been posted.")
            return redirect('IMBD_app:movie_details', pk=pk)

    else:
        # Initialisiere Formulare
        comment_form = UserCommentForm()
        rating_form = UserRatingForm()

    # Daten an das Template übergeben
    return render(request, "movies/movie_details.html", {
        "movie": movie,
        "genres": genres,
        "directors": directors,
        "cast": top_actors,
        "user_average_rating": user_average_rating,
        "comments": comments,
        "user_watchlist": user_watchlist,  # Aktuelle Watchlist des Nutzers als Liste
        "comment_form": comment_form,
        "rating_form": rating_form,
    })




def all_movies(request):
    page_number = 1  # Default to page 1
    # You can get the page number from the request (e.g., URL query parameters)
    # For example: /movies/all_movies/?page=2
    if 'page' in request.GET:
        page_number = int(request.GET['page'])

    # Fetch top trending movies for the current page
    top_movies = fetch_tmdb_data("trending/movie/week", params={"language": "en-US"}, page=page_number)

    # Round vote_average for each movie
    for movie in top_movies.get("results", []):
        movie['vote_average'] = round(movie['vote_average'], 1)  # Round to 1 decimal place

    # Return the list of movies and the current page in the context
    return render(request, "movies/all_movies.html", {
        "movies": top_movies.get("results", []),
        "page_number": page_number,
    })


def recent_movies(request):
    page_number = 1  # Default to page 1
    if 'page' in request.GET:
        page_number = int(request.GET['page'])

    # Fetch movies sorted by release date (most recent first)
    recent_movies = fetch_tmdb_data(
        "discover/movie",  # TMDb-API-Ressource für das Filtern/Suchen
        params={
            "language": "en-US",
            "sort_by": "release_date.desc",  # Sortiere nach Release-Datum (neueste zuerst)
            "include_adult": False,         # Keine Erwachsenenfilme
            "include_video": False,         # Keine Video-only Einträge
            "page": page_number,            # Aktuelle Seite
            "release_date.lte": "2025-01-05"  # Nur Filme bis heute
        }
    )

    # Round vote_average for each movie
    for movie in recent_movies.get("results", []):
        movie['vote_average'] = round(movie['vote_average'], 1)  # Runde auf 1 Nachkommastelle

    # Render the "all_movies" template
    return render(request, "movies/recent_movies.html", {
        "movies": recent_movies.get("results", []),
        "page_number": page_number,
    })


# Actor Details (with database saving)
def actor_details(request, pk):
    # Fetch actor details from the database or via API
    actor = Actor.objects.filter(tmdb_id=pk).first()

    if not actor:
        actor = fetch_actor_from_tmdb(pk)

    # Get the top 5 movies the actor is known for
    top_movies = actor.known_for_movies.all()[:5]

    return render(request, "actors/actor_details.html", {
        "actor": actor,
        "top_movies": top_movies,  # Use the actor's known for movies
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
        form_type = request.POST.get('form_type')
        print(f"Form type received: {form_type}")  # Debugging-Ausgabe

        if form_type == 'actor':
            actor_form = ActorForm(request.POST, request.FILES)
            if actor_form.is_valid():
                actor_form.save()
                print("Actor created successfully!")  # Debugging-Ausgabe
                messages.success(request, "Actor created successfully!")
                return redirect('IMBD_app:create')  # Redirect to actor list or another page
            else:
                # Debugging: Print out form errors
                print("ERROR: Actor couldn't be created")
                print(actor_form.errors)
                messages.error(request, "Error creating actor. Please check the form.")
        
        elif form_type == 'director':
            director_form = DirectorForm(request.POST, request.FILES)
            if director_form.is_valid():
                director_form.save()
                print("Director created successfully!")  # Debugging-Ausgabe
                messages.success(request, "Director created successfully!")
                return redirect('IMBD_app:create')  # Redirect to director list or another page
            else:
                print("ERROR: Director couldn't be created")
                print(director_form.errors)
                messages.error(request, "Error creating director. Please check the form.")
        
        elif form_type == 'movie':
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                movie_form.save()
                print("Movie created successfully!")  # Debugging-Ausgabe
                messages.success(request, "Movie created successfully!")
                return redirect('IMBD_app:create')  # Redirect to movie list or another page
            else:
                print("ERROR: Movie couldn't be created")
                print(movie_form.errors)
                messages.error(request, "Error creating movie. Please check the form.")

    return render(request, 'create.html', {
        'actor_form': actor_form,
        'director_form': director_form,
        'movie_form': movie_form,
    })


def success(request):
    return render(request, "success.html")




# alles für search bar

def movie_list(request):
    query = request.GET.get('q', '').strip()  # Search term
    category = request.GET.get('category', 'movie')  # Default category "movie"

    # Initialize context data
    movies_db = Movie.objects.none()
    genres_db = Genre.objects.none()
    movies_tmdb = []

    if query:
        if category == "movie":
            # Filter local movies by title
            movies_db = Movie.objects.filter(Q(title__icontains=query)).distinct()

            # Fetch TMDB movies if not found in DB
            tmdb_response = fetch_tmdb_data("search/movie", params={"query": query, "language": "en-US", "page": 1})
            tmdb_movies = tmdb_response.get("results", [])

            for tmdb_movie in tmdb_movies:
                # Check if the movie exists in the local database by TMDB ID
                movie_exists = Movie.objects.filter(tmdb_id=tmdb_movie["id"]).exists()
                if not movie_exists:
                    # Save the movie from TMDB to the database if not already present
                    movie = fetch_movie_from_tmdb(tmdb_movie["id"])  # This saves the movie in DB
                    movies_tmdb.append(movie)

        elif category == "genre":
            # Filter genres by name and fetch related movies
            genres_db = Genre.objects.filter(name__icontains=query)
            movies_db = Movie.objects.filter(genres__in=genres_db).distinct()

            # Fetch TMDB movies based on the query (genre)
            tmdb_response = fetch_tmdb_data("search/movie", params={"query": query, "language": "en-US", "page": 1})
            tmdb_movies = tmdb_response.get("results", [])
            for tmdb_movie in tmdb_movies:
                # Check if the movie exists in the local database by TMDB ID
                movie_exists = Movie.objects.filter(tmdb_id=tmdb_movie["id"]).exists()
                if not movie_exists:
                    # Save the movie from TMDB to the database if not already present
                    movie = fetch_movie_from_tmdb(tmdb_movie["id"])  # This saves the movie in DB
                    movies_tmdb.append(movie)

    context = {
        "query": query,
        "category": category,
        "movies_db": movies_db,  # Local database movies
        "genres_db": genres_db,  # Genres in database
        "movies_tmdb": movies_tmdb,  # TMDB movies
    }
    return render(request, "movies/movie_list.html", context)



# List of all directors (mock data)
def director_list(request):
    query = request.GET.get('q', '').strip()  # Search term
    category = request.GET.get('category', 'director')  # Default category "director"

    # Initialize context data
    directors_db = Director.objects.none()
    directors_tmdb = []

    if query:
        if category == "director":
            # Filter local directors by name
            directors_db = Director.objects.filter(Q(name__icontains=query))

            # Fetch TMDB directors if not found in DB
            tmdb_response = fetch_tmdb_data("search/person", params={"query": query})
            tmdb_directors = tmdb_response.get("results", [])

            for tmdb_director in tmdb_directors:
                # Check if the director exists in the local database by TMDB ID
                director_exists = Director.objects.filter(tmdb_id=tmdb_director["id"]).exists()
                if not director_exists:
                    # Save the director from TMDB to the database if not already present
                    director = fetch_director_from_tmdb(tmdb_director["id"])  # This saves the director in DB
                    directors_tmdb.append(director)

    context = {
        "query": query,
        "category": category,
        "directors_db": directors_db,  # Local database directors
        "directors_tmdb": directors_tmdb,  # TMDB directors
    }
    return render(request, "directors/director_list.html", context)




# List of all actors (mock data)
def actor_list(request):
    query = request.GET.get('q', '').strip()  # Search term
    category = request.GET.get('category', 'actor')  # Default category "actor"

    # Initialize context data
    actors_db = Actor.objects.none()
    actors_tmdb = []

    if query:
        if category == "actor":
            # Filter local actors by name
            actors_db = Actor.objects.filter(Q(name__icontains=query))

            # Fetch TMDB actors if not found in DB
            tmdb_response = fetch_tmdb_data("search/person", params={"query": query})
            tmdb_actors = tmdb_response.get("results", [])

            for tmdb_actor in tmdb_actors:
                # Check if the actor exists in the local database by TMDB ID
                actor_exists = Actor.objects.filter(tmdb_id=tmdb_actor["id"]).exists()
                if not actor_exists:
                    # Save the actor from TMDB to the database if not already present
                    actor = fetch_actor_from_tmdb(tmdb_actor["id"])  # This saves the actor in DB
                    actors_tmdb.append(actor)

    context = {
        "query": query,
        "category": category,
        "actors_db": actors_db,  # Local database actors
        "actors_tmdb": actors_tmdb,  # TMDB actors
    }
    return render(request, "actors/actor_list.html", context)

def toggle_watchlist(request, pk):
    if request.method == "POST" and request.user.is_authenticated:
        # Prüfen, ob der Film in der Datenbank existiert
        movie = Movie.objects.filter(tmdb_id=pk).first()
        
        # Wenn der Film nicht existiert, aus der TMDB-API laden
        if not movie:
            movie = fetch_movie_from_tmdb(pk)

        # Prüfen, ob der Film in der Watchlist des Benutzers ist
        watchlist_item = Watchlist.objects.filter(user=request.user, movie=movie).first()

        if watchlist_item:
            # Film aus der Watchlist entfernen
            watchlist_item.delete()
            messages.success(request, f"'{movie.title}' has been removed from your watchlist.")
        else:
            # Film zur Watchlist hinzufügen (nur Titel verwenden)
            Watchlist.objects.create(user=request.user, movie=movie)
            messages.success(request, f"'{movie.title}' has been added to your watchlist.")

        return redirect('IMBD_app:movie_details', pk=pk)
    else:
        messages.error(request, "You need to be logged in to modify your watchlist.")
        return redirect('IMBD_app:user_login')



def watchlist_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your watchlist.")
        return redirect('IMBD_app:user_login')

    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, "watchlist.html", {
        "movie_titles": watchlist_items
    })
