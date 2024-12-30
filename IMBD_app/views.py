from django.shortcuts import render, redirect
from .forms import ActorForm, DirectorForm, MovieForm

# Create your views here.

from django.shortcuts import render

# Home Page
def home(request):
    return render(request, "home.html")

# Test movie Data
def get_movies():
    return [
        {'id': 1, 'title': 'Wolves with Guns', 'date': '2024-01-01', 'genre': 'action', 'description': 'GUNS EVERYWHERE', 'actors': '', 'image': '/static/images/vinonpotail.jpeg'},
        {'id': 2, 'title': 'Evil is Coming', 'date': '2024-01-02', 'genre': 'thriller', 'description': 'THE WORLD IS BURNING', 'actors': '', 'image': '/static/images/evil.jpeg'},
        {'id': 3, 'title': 'Stickmen', 'date': '2024-01-02', 'genre': 'comedy', 'description': '???', 'actors': '', 'image': '/static/images/onyplic.jpeg'},
    ]

# List of all movies (using mock data)
def movie_list(request):
    movies = get_movies()
    return render(request, "movies/movie_list.html", {'movies': movies})


# List of movies for landing page (using mock data)
def home(request):
    movies = get_movies()
    return render(request, "home.html", {'movies': movies})

# Details of a specific movie (using mock data)
def movie_details(request, pk):
    movies = get_movies()
    movie = next((m for m in movies if m['id'] == pk), None)
    if not movie:
        return render(request, "404.html")
    return render(request, "movies/movie_details.html", {'movie': movie})

# List of all actors (mock data)
def actor_list(request):
    actors = [
        {'id': 1, 'name': 'Actor 1', 'biography': 'Biography of actor 1'},
        {'id': 2, 'name': 'Actor 2', 'biography': 'Biography of actor 2'}
    ]
    return render(request, "actors/actor_list.html", {'actors': actors})

# Details of a specific actor (mock data)
def actor_details(request, pk):
    actor = {'id': pk, 'name': f'Actor {pk}', 'biography': 'Detailed biography of actor.'}
    return render(request, "actors/actor_details.html", {'actor': actor})

# List of all directors (mock data)
def director_list(request):
    directors = [
        {'id': 1, 'name': 'Director 1', 'biography': 'Biography of director 1'},
        {'id': 2, 'name': 'Director 2', 'biography': 'Biography of director 2'}
    ]
    return render(request, "directors/director_list.html", {'directors': directors})

# Details of a specific director (mock data)
def director_details(request, pk):
    director = {'id': pk, 'name': f'Director {pk}', 'biography': 'Detailed biography of director.'}
    return render(request, "directors/director_details.html", {'director': director})

# Login Page
def login(request):
    return render(request, "auth/login.html")

# Signup Page
def signup(request):
    return render(request, "auth/signup.html")


def create(request):
    # Standardformulare initialisieren
    actor_form = ActorForm()
    director_form = DirectorForm()
    movie_form = MovieForm()

    if request.method == 'POST':
        # Formulartyp aus den POST-Daten lesen, s. create.html
        form_type = request.POST.get('form_type')

        if form_type == 'actor':
            actor_form = ActorForm(request.POST, request.FILES)
            if actor_form.is_valid():
                actor_form.save()
                return render(request, 'success.html')  # Erfolgsseite
            else:
                print("ERROR: Actor couldnt be created")
        elif form_type == 'director':
            director_form = DirectorForm(request.POST, request.FILES)
            if director_form.is_valid():
                director_form.save()
                return render(request, 'success.html')  # Erfolgsseite
            else:
                print("ERROR: Director couldnt be created")
        elif form_type == 'movie':
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                movie_form.save()
                return render(request, 'success.html')  # Erfolgsseite
            else:
                print("ERROR: Movie couldnt be created")
            
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
