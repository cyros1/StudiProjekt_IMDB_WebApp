from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    biography = models.TextField()
    image = models.ImageField(upload_to='actors/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Director(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    biography = models.TextField()
    image = models.ImageField(upload_to='directors/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('comedy', 'Comedy'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('fantasy', 'Fantasy'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('sci_fi', 'Sci-Fi'),
        ('thriller', 'Thriller')
    ]

    title = models.CharField(max_length=255)
    date = models.IntegerField()  # Nur Jahr
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    # genre = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='films')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name="directed_movies")
        # related_name, um einträge easier zu finden, bsp:
        # director = Director.objects.get(id=1)
        # movies = director.directed_movies.all()  # Liste aller Filme dieses Regisseurs
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

    def __str__(self):
        return self.title

# Rating maybe erst auf Filmseite anzeigen lassen, Kommentarspalte
# Durchschnittsrating weiter oben auf film_details anzeigen lassen
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, default=1)    
        # gehört zum jeweiligen Film dazu, wenn rating gelöscht wird, bleibt Movie am leben
    rating = models.PositiveSmallIntegerField(default=1) 
        # legt nur fest, dass ganzzahlen verwendet werden, kann auch über 5 gehen
    author = models.CharField(max_length=25, default="") # Name des Nutzers
    comment = models.TextField(blank=True, null=True) # Kommentar des Nutzers, optional
    created_at = models.DateTimeField(auto_now_add=True) # Datum

    def __str__(self):
        return f"{self.author} - {self.movie.title}: {self.rating} stars"
    