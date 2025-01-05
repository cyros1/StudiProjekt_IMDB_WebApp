from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)  # TMDb Movie ID
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)  # Path to backdrop image
    overview = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)  # Average TMDb rating
    genres = models.ManyToManyField(Genre, related_name="movies")  # Many-to-Many relationship with Genre
    directors = models.ManyToManyField('Director', related_name="movies")  # Many-to-Many with Director
    cached_at = models.DateTimeField(auto_now_add=True)  # Last time the movie was fetched
    is_custom = models.BooleanField(default=False)  # Flag for custom movies (not from TMDb)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Actor(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, null=True, blank=True)  # Path to profile picture
    biography = models.TextField(null=True, blank=True)
    known_for_movies = models.ManyToManyField(Movie, related_name="featured_actors", blank=True)  # Top 5 movies
    cached_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Director(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, null=True, blank=True)  # Path to profile picture
    biography = models.TextField(null=True, blank=True)
    known_for_movies = models.ManyToManyField(Movie, related_name="featured_directors", blank=True)  # Top 5 movies
    cached_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_actors")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, null=True, blank=True)  # Optional role


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
