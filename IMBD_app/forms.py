from django import forms
from .models import Actor, Director, Movie

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'surname', 'date_of_birth', 'biography','image']

form = ActorForm()
actor = Actor.objects.filter(pk=1).first() # versucht obj abzurufen mit pk 1, wenn nicht gefunden, gibt "none" zurück

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'surname', 'date_of_birth', 'biography','image',]

form = DirectorForm()
director = Director.objects.filter(pk=1).first() # versucht obj abzurufen mit pk 1, wenn nicht gefunden, gibt "none" zurück

        

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie                                                 
        fields = ['title', 'date', 'genre', 'description', 'actors','director','image']  # TODO: rating hinzufügen, maybe zur filmseite erst
        widgets = {
            'actors': forms.CheckboxSelectMultiple(),  # Für mehrere Schauspieler
            'director': forms.Select(attrs={'size': '5', 'style': 'max-height: 200px; overflow-y: auto;'})  
            # Scrollbare Liste, größe etc kann (und sollte) man noch ändern
            # bei variable date nur das jahr 
        }
        # genre maybe auch rein, aus einer liste oder so

form = MovieForm()
movie = Movie.objects.filter(pk=1).first() # versucht obj abzurufen mit pk 1, wenn nicht gefunden, gibt "none" zurück
