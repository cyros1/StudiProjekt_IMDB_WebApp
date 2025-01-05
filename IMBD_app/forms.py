from django import forms
from .models import Movie, Actor, Director, UserComment, UserRating, Genre
from .utils.tmdb import generate_custom_id

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'biography', 'profile_path', 'custom_profile_image', 'custom_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Enter actor name'}),
            'biography': forms.Textarea(attrs={'class': 'form-field', 'placeholder': 'Write a short biography'}),
            'profile_path': forms.URLInput(attrs={'class': 'form-field', 'placeholder': 'Enter profile image URL'}),
            'custom_profile_image': forms.ClearableFileInput(attrs={'class': 'form-field'}),  # File input widget
        }

    def save(self, commit=True):
        actor = super().save(commit=False)
        
        # If there's a custom profile image, use it and clear the profile_path
        if self.cleaned_data.get('custom_profile_image'):
            actor.profile_path = None
            actor.custom_profile_image = self.cleaned_data['custom_profile_image']
        
        if commit:
            actor.save()
        return actor





class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'biography', 'profile_path', 'custom_profile_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Enter director name'}),
            'biography': forms.Textarea(attrs={'class': 'form-field', 'placeholder': 'Write a short biography'}),
            'profile_path': forms.URLInput(attrs={'class': 'form-field', 'placeholder': 'Enter profile image URL'}),
            'custom_profile_image': forms.ClearableFileInput(attrs={'class': 'form-field'}),  # File input widget
        }

    def save(self, commit=True):
        director = super().save(commit=False)
        if self.cleaned_data.get('custom_profile_image'):
            director.profile_path = None
            director.custom_profile_image = self.cleaned_data['custom_profile_image']
        if commit:
            director.save()
        return director



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'custom_backdrop_image', 'overview', 'rating', 'genres', 'actors', 'directors',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Enter movie title'}),
            'release_date': forms.DateInput(attrs={'class': 'form-field', 'placeholder': 'Enter release date'}),
            'custom_backdrop_image': forms.ClearableFileInput(attrs={'class': 'form-field'}),  # File input widget
            'overview': forms.Textarea(attrs={'class': 'form-field', 'placeholder': 'Write a short overview'}),
            'rating': forms.NumberInput(attrs={'class': 'form-field', 'placeholder': 'Enter rating'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-field'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-field'}),
            'directors': forms.SelectMultiple(attrs={'class': 'form-field'}),
        }

    def save(self, commit=True):
        actor = super().save(commit=False)
        
        # If there's a custom profile image, use it and clear the profile_path
        if self.cleaned_data.get('custom_profile_image'):
            actor.profile_path = None
            actor.custom_profile_image = self.cleaned_data['custom_profile_image']

        # Generate and assign a custom ID
        if not actor.custom_id:
            actor.custom_id = generate_custom_id()

        if commit:
            actor.save()
        return actor


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
                'class': 'form-field',
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
