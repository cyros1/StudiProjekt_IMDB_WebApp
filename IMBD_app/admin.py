from django.contrib import admin
from .models import Actor, Director, Movie

# Registrierung der jeweiligen Models
# TODO: Actor Model adden

admin.site.register(Actor)

admin.site.register(Director)

admin.site.register(Movie)
