from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def film(request):
    return render(request, "film.html")

def schauspieler(request):
    return render(request, "schauspieler.html")

def regisseur(request):
    return render(request, "regisseur.html")


# film : Titel, Veröffentlichungsdatum, Genre, Beschreibung
# Schauspieler : Vor- & Nachname, Geburtsdatum, Biografie
# Regisseur : Vor- & Nachname, Geburtsdatum, Biografie
# Bewertung: Film (Foreignkey), Rezensent, Bewertung (1-5 Sterne)
#            Kommentar, Datum

# NÄCHSTER SCHRITT: Models!!
# from django.db import models

# class Film(models.Model):
#     titel = models.CharField(max_length=255)
#     veroeffentlichungsdatum = models.DateField()
#     genre = models.CharField(max_length=100)
#     beschreibung = models.TextField()

# class Schauspieler(models.Model):
#     vorname = models.CharField(max_length=100)
#     nachname = models.CharField(max_length=100)
#     geburtsdatum = models.DateField()
#     biografie = models.TextField()

# class Regisseur(models.Model):
#     vorname = models.CharField(max_length=100)
#     nachname = models.CharField(max_length=100)
#     geburtsdatum = models.DateField()
#     biografie = models.TextField()

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
