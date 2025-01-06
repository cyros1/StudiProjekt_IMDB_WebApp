from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  # Anzeigen des Namens in der Dropdown-Liste


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # Allow null for custom entries
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    custom_id = models.CharField(max_length=6, unique=True, null=True, blank=True)  # Unique 6-character ID for custom actors
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)  # Path to backdrop image (TMDb)
    custom_backdrop_image = models.ImageField(  # Neues Feld für benutzerdefinierte Backdrops
        upload_to='movies/backdrops/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    overview = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)  # Average TMDb rating
    genres = models.ManyToManyField(Genre, related_name="movies")  # Many-to-Many relationship with Genre
    actors = models.ManyToManyField('Actor', related_name="movies")
    directors = models.ManyToManyField('Director', related_name="movies")  # Many-to-Many with Director
    is_custom = models.BooleanField(default=False)  # Flag for custom movies (not from TMDb)
    cached_at = models.DateTimeField(auto_now_add=True)  # Last time the movie was fetched
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_backdrop_image(self):
        """
        Returns the URL for the backdrop image. Prioritizes custom images over TMDb paths.
        """
        if self.custom_backdrop_image:
            return self.custom_backdrop_image.url  # Local uploaded image
        elif self.backdrop_path:
            return f'https://image.tmdb.org/t/p/w500{self.backdrop_path}'  # TMDb image
        return '/static/images/default-backdrop.png'  # Default fallback
    
    def __str__(self):
        return self.title  # Anzeigen des Namens in der Dropdown-Liste


class Actor(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # Allow null for custom entries
    custom_id = models.CharField(max_length=6, unique=True, null=True, blank=True)  # Unique 6-character ID for custom actors
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, null=True, blank=True)  # For TMDb API paths
    custom_profile_image = models.ImageField(
        upload_to='actors/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    biography = models.TextField(null=True, blank=True)
    known_for_movies = models.ManyToManyField(Movie, related_name="featured_actors", blank=True)
    cached_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_profile_picture(self):
        if self.custom_profile_image:
            return self.custom_profile_image.url  # Local uploaded image
        elif self.profile_path:
            return f'https://image.tmdb.org/t/p/w500{self.profile_path}'  # TMDb image
        return '/static/images/default-profile.png'  # Default fallback
    
    def __str__(self):
        return self.name  # Anzeigen des Namens in der Dropdown-Liste



class Director(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # Allow null for custom entries
    name = models.CharField(max_length=255)
    custom_id = models.CharField(max_length=6, unique=True, null=True, blank=True)  # Unique 6-character ID for custom actors
    profile_path = models.CharField(max_length=255, null=True, blank=True)  # TMDb profile path
    custom_profile_image = models.ImageField(  # Neues Feld für benutzerdefinierte Profilbilder
        upload_to='directors/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    biography = models.TextField(null=True, blank=True)
    known_for_movies = models.ManyToManyField(Movie, related_name="featured_directors", blank=True)
    cached_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_profile_picture(self):
        """
        Returns the URL for the profile picture. Prioritizes custom images over TMDb paths.
        """
        if self.custom_profile_image:
            return self.custom_profile_image.url  # Local uploaded image
        elif self.profile_path:
            return f'https://image.tmdb.org/t/p/w500{self.profile_path}'  # TMDb image
        return '/static/images/default-profile.png'  # Default fallback
    
    def __str__(self):
        return self.name  # Anzeigen des Namens in der Dropdown-Liste
    
class UserComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Nutzer-Referenz
    comment = models.TextField()
    rating = models.FloatField(default=0.0)  # Rating im Kommentar
    created_at = models.DateTimeField(auto_now_add=True)


class UserRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ratings")
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class CachedData(models.Model):
    """
    A generic model to track when specific data has been fetched.
    Used to manage TMDb's 6-month caching requirement.
    """
    model_type = models.CharField(max_length=50)  # e.g., 'movie', 'actor', 'director'
    tmdb_id = models.IntegerField(unique=True)
    cached_at = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')  # Verhindert doppelte Einträge

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"