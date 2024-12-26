from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    biography = models.TextField()
    # profile_picture = models.ImageField(upload_to='actors/', blank=True, null=True)

class Director(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    biography = models.TextField()
    # movies = models.ManyToManyField(Movie) 

class Movie(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    genre = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='films')
    # director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='films', default=1) # wenn director gelöscht wird, lösch filme, nicht andersum!!

class Rating(models.Model):
    # film (foreignkey)
    # rezensent (pseudonym)
   #  movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, default=1)    # gehört zum jeweiligen film dazu
   #  rating = models.SmallIntegerField(default=1) # 0-5 steren
    comment = models.CharField(max_length=500) # Kommentar des Nutzers
    created_at = models.DateTimeField(auto_now_add=True) # Datum

# CASCADE = bei löschung werden auch alle referenzierten obj auch gelöscht