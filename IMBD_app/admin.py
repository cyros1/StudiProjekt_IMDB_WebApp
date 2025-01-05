from django.contrib import admin
from .models import Actor, Director, Movie, UserRating, Genre, MovieActor, UserComment, UserRating, CachedData

# Registering the Genre model
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display genre name in the list view
    search_fields = ('name',)  # Enable search by genre name

# Registering the Movie model
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'cached_at', 'is_custom')  # Fields to display
    search_fields = ('title', 'tmdb_id')  # Enable search by title or TMDb ID
    list_filter = ('release_date', 'is_custom', 'genres')  # Add filters to the list view

# Registering the Actor model
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tmdb_id', 'cached_at')  # Fields to display
    search_fields = ('name', 'tmdb_id')  # Enable search by name or TMDb ID

# Registering the Director model
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tmdb_id', 'cached_at')  # Fields to display
    search_fields = ('name', 'tmdb_id')  # Enable search by name or TMDb ID

# Registering the MovieActor model
@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    list_display = ('movie', 'actor', 'role')  # Fields to display
    search_fields = ('movie__title', 'actor__name')  # Enable search by movie title or actor name
    list_filter = ('movie', 'actor')  # Filter by movie and actor

# Registering the UserComment model
@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'created_at')  # Fields to display
    search_fields = ('movie__title', 'user')  # Enable search by movie title or user
    list_filter = ('created_at',)  # Filter by the date comment was created

# Registering the UserRating model
@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')  # Fields to display
    search_fields = ('movie__title', 'user')  # Enable search by movie title or user
    list_filter = ('created_at',)  # Filter by the date rating was created

# Registering the CachedData model
@admin.register(CachedData)
class CachedDataAdmin(admin.ModelAdmin):
    list_display = ('model_type', 'tmdb_id', 'cached_at')  # Fields to display
    search_fields = ('model_type', 'tmdb_id')  # Enable search by model type or TMDb ID
    list_filter = ('model_type',)  # Filter by model type

