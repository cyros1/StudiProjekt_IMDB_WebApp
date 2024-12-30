from django import forms
from .models import Actor, Director, Movie

# Forms für /create.html, um Objekte zu erstellen als eingeloggter User
# TODO: Login Page hierfür erstellen

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'surname', 'date_of_birth', 'biography','image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter actor name',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter actor surname',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-field',
                'type': 'date',
            }),
            'biography': forms.Textarea(attrs={
                'class': 'form-field',
                'placeholder': 'Write a short biography',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-field',
            }),
        }

form = ActorForm()
actor = Actor.objects.filter(pk=1).first() 
# versucht obj abzurufen mit pk 1, wenn nicht gefunden, gibt "none" zurück

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'surname', 'date_of_birth', 'biography','image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter director name',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter director surname',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-field',
                'type': 'date',
            }),
            'biography': forms.Textarea(attrs={
                'class': 'form-field',
                'placeholder': 'Write a short biography',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-field',
            }),
        }

form = DirectorForm()
director = Director.objects.filter(pk=1).first() 
# versucht obj abzurufen mit pk 1, wenn nicht gefunden, gibt "none" zurück

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'date', 'genre', 'description', 'actors', 'director', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter movie title',
            }),
            'date': forms.NumberInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter release year',
            }),
            'genre': forms.Select(attrs={
                'class': 'form-field',
                'placeholder': 'Select genre',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-field',
                'placeholder': 'Write a short description of the movie',
            }),
            'actors': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-field',
            }),
            'director': forms.Select(attrs={
                'class': 'form-field',
                'size': '5',
                'style': 'max-height: 200px; overflow-y: auto;',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-field',
            }),
        }

# Example usage of the form and movie instance
form = MovieForm()
movie = Movie.objects.filter(pk=1).first()

