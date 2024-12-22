from django.db import models

# Create your models here.

class Film(models.Model):
    titel = models.CharField(max_length=255)
    datum = models.DateField()
    genre = models.CharField(max_length=100)
    beschreibung = models.TextField()
    # bewertung?

class Schauspieler(models.Model):
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    geburtsdatum = models.DateField()
    biografie = models.TextField()

class Regisseur(models.Model):
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    geburtsdatum = models.DateField()
    biografie = models.TextField()