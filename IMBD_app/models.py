from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    biography = models.TextField()
    image = models.ImageField(upload_to='actors/', blank=True, null=True)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    biography = models.TextField()
    image = models.ImageField(upload_to='directors/', blank=True, null=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    genre = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='films')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, default=1)    
    # gehört zum jeweiligen film dazu, wenn rating gelöscht wird, bleibt film am leben
    # rating = models.SmallIntegerField(default=1) # 0-5 steren
    # rezensent (pseudonym)
    comment = models.CharField(max_length=500) # Kommentar des Nutzers
    created_at = models.DateTimeField(auto_now_add=True) # Datum

    def __str__(self):
        return self.movie + "-rating"  #idk ob das funktioniert, wird noch getestet

# CASCADE = bei löschung werden auch alle referenzierten obj auch gelöscht