from django.shortcuts import render, redirect
from .forms import ActorForm, DirectorForm, MovieForm

# Create your views here.

def home(request):
    return render(request, "home.html")

def movie(request):
    return render(request, "movie.html")

def actor(request):
    return render(request, "actor.html")

def director(request):
    return render(request, "director.html")


def create(request):
    # Standardformulare initialisieren
    actor_form = ActorForm()
    director_form = DirectorForm()
    movie_form = MovieForm()

    if request.method == 'POST':
        # Formulartyp aus den POST-Daten lesen
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

# film : Titel, Veröffentlichungsdatum, Genre, Beschreibung
# Schauspieler : Vor- & Nachname, Geburtsdatum, Biografie
# Regisseur : Vor- & Nachname, Geburtsdatum, Biografie
# Bewertung: Film (Foreignkey), Rezensent, Bewertung (1-5 Sterne)
#            Kommentar, Datum






# daten in views übergeben
# from .models import Film

# def film_list(request):
#     filme = Film.objects.all()
#     return render(request, "film.html", {"filme": filme})


# #dann django admin oder shell nutzen um daten zu erstellen:
# python manage.py shell

# from IMBD_app.models import Film
# Film.objects.create(titel="Inception", veroeffentlichungsdatum="2010-07-16", genre="Science Fiction", beschreibung="Ein Dieb stiehlt Ideen aus Träumen.")
