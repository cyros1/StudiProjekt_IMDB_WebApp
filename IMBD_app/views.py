from django.shortcuts import render, redirect
from .forms import ActorForm, DirectorForm, MovieForm

# Create your views here.

from django.shortcuts import render

# Home Page
def home(request):
    return render(request, "home.html")

# List of all movies (mock data)
def movie_list(request):
    movies = [
        {'id': 1, 'title': 'Movie 1', 'release_date': '2024-01-01', 'description': 'A great movie!'},
        {'id': 2, 'title': 'Movie 2', 'release_date': '2024-01-02', 'description': 'Another great movie!'}
    ]
    return render(request, "movies/movie_list.html", {'movies': movies})

# Details of a specific movie (mock data)
def movie_details(request, pk):
    # Simulating fetching movie by pk (id)
    movie = {'id': pk, 'title': f'Movie {pk}', 'release_date': '2024-01-01', 'description': 'Detailed description of movie.'}
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
