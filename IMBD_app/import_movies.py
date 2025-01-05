
from django.core.management.base import BaseCommand
import requests
from IMBD_app.models import Movie, Actor, Director

class Command(BaseCommand):
    help = 'Importiere Film-Daten von der API'

    def handle(self, *args, **kwargs):
        # API URL (ersetze sie durch die tatsächliche URL)
        response = requests.get('https://api.themoviedb.org/3')
        data = response.json()

        for movie_data in data['results']:
            # Falls der Director existiert, ansonsten erstellen
            director, created = Director.objects.get_or_create(
                name=movie_data['director_name'], 
                surname=movie_data['director_surname']
            )

            # Erstellen des Films und der Schauspieler
            movie = Movie.objects.create(
                title=movie_data['title'],
                date=movie_data['release_year'],
                genre=movie_data['genre'],
                description=movie_data['description'],
                director=director
            )

            for actor_data in movie_data['actors']:
                actor, created = Actor.objects.get_or_create(
                    name=actor_data['name'], 
                    surname=actor_data['surname']
                )
                movie.actors.add(actor)

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {movie.title}'))