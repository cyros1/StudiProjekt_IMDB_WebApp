from django import forms
from .models import Actor, Director, Movie

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'surname', 'date_of_birth', 'biography','image']

form = ActorForm()

actor = Actor.objects.get(pk=1)
form = ActorForm(instance=actor)

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'surname', 'date_of_birth', 'biography','image']
        

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'date', 'genre', 'description', 'actors',]  # Director kann hinzugefügt werden, wenn aktiviert
        widgets = {
            'actors': forms.CheckboxSelectMultiple(),  # Optional für bessere Auswahl
        }