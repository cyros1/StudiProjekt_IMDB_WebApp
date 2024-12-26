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
    return render(request, 'create.html')


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
