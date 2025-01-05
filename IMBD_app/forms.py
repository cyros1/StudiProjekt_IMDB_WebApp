from django import forms
from .models import Movie, Actor, Director, UserComment, UserRating, Genre


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'biography', 'profile_path']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter actor name',
            }),
            'biography': forms.Textarea(attrs={
                'class': 'form-field',
                'placeholder': 'Write a short biography',
            }),
            'profile_path': forms.URLInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter profile image URL',
            }),
        }


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'biography', 'profile_path']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter director name',
            }),
            'biography': forms.Textarea(attrs={
                'class': 'form-field',
                'placeholder': 'Write a short biography',
            }),
            'profile_path': forms.URLInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter profile image URL',
            }),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['tmdb_id', 'title', 'release_date', 'backdrop_path', 'overview', 'rating', 'genres', 'directors', 'is_custom']
    
    # Custom form field for adding actors (based on MovieActor)
    actors = forms.ModelMultipleChoiceField(queryset=Actor.objects.all(), required=False)

    def save(self, commit=True):
        movie = super().save(commit=False)
        if commit:
            movie.save()

        # Add the selected actors to the MovieActor model
        actors = self.cleaned_data.get('actors', [])
        for actor in actors:
            Actor.objects.create(movie=movie, actor=actor)
        
        return movie


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Enter genre name',
            }),
        }


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-field bg-footer-purple text-text-white',
                'rows': 4,
                'placeholder': 'Write your comment here...',
            }),
        }
        labels = {
            'comment': 'Your Comment',
        }

class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-field bg-footer-purple text-text-white',
                'min': 0,
                'max': 10,
                'step': 0.1,
                'placeholder': 'Enter a rating from 0 to 10',
            }),
        }
        labels = {
            'rating': 'Your Rating (0-10)',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 0 or rating > 10):
            raise forms.ValidationError("Rating must be between 0 and 10.")
        return rating
