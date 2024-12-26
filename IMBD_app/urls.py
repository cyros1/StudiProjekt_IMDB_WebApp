from django.urls import path
from . import views


app_name = 'IMBD_app'

urlpatterns=[
    path("", views.home, name="home"),
    path("movie/", views.movie, name="movie"),
    path("actor/", views.actor, name="actor"),
    path("director/", views.director, name="director"),
    path("create/", views.create, name="create"),
]
# nach der url einfach / film, schauspieler whatever eingeben um daraufzukommen

