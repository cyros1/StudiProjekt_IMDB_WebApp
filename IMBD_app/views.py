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
    # Erstelle eine Instanz des ActorForm
    actor_form = ActorForm()

    if request.method == 'POST':
        # Wenn das Formular übermittelt wird
        actor_form = ActorForm(request.POST, request.FILES)
        if actor_form.is_valid():  # Überprüfen, ob das Formular gültig ist
            actor_form.save()  # Speichern der Actor-Daten
            return redirect('success.html')  # Umleitung nach dem erfolgreichen Speichern

    return render(request, 'create.html', {
        'actor_form': actor_form,
    })

# def create(request):
    # Initialisiere die Formulare standardmäßig
    actor_form = ActorForm()
    director_form = DirectorForm()
    movie_form = MovieForm()

    if request.method == 'POST':
        # Prüfe, welches Formular gesendet wurde
        if 'actorName' in request.POST:
            actor_form = ActorForm(request.POST, request.FILES)
            if actor_form.is_valid():
                actor_form.save()
                print("Actor wurde gespeichert!")
                return redirect('success.html')  # Erfolgsseite
            else:
                print("Formular ist ungültig!")
                print(actor_form.errors)
        elif 'directorName' in request.POST:
            director_form = DirectorForm(request.POST, request.FILES)
            if director_form.is_valid():
                director_form.save()
                return redirect('success.html')  # Erfolgsseite
        elif 'movieTitle' in request.POST:
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                movie_form.save()
                print("Actor wurde gespeichert!")
                return redirect('success.html')  # Erfolgsseite
            else:
                print("Formular ist ungültig!")
                print(actor_form.errors)

    # Render das Template mit allen Formularen
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




# anzeigen lassen beispiel
# {% for film in filme %}
# <div>
#     <h2>{{ film.titel }}</h2>
#     <p>Genre: {{ film.genre }}</p>
#     <p>Veröffentlicht am: {{ film.veroeffentlichungsdatum }}</p>
# </div>
# {% endfor %}

# daten in views übergeben
# from .models import Film

# def film_list(request):
#     filme = Film.objects.all()
#     return render(request, "film.html", {"filme": filme})


# #dann django admin oder shell nutzen um daten zu erstellen:
# python manage.py shell

# from IMBD_app.models import Film
# Film.objects.create(titel="Inception", veroeffentlichungsdatum="2010-07-16", genre="Science Fiction", beschreibung="Ein Dieb stiehlt Ideen aus Träumen.")
