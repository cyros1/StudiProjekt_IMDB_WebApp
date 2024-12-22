from django.urls import path
from . import views


app_name = 'IMBD_app'

urlpatterns=[
    path("", views.home, name="home"),
    path("film/", views.film, name="film"),
    path("schauspieler/", views.schauspieler, name="schauspieler"),
    path("regisseur/", views.regisseur, name="regisseur"),
]
# nach der url einfach / film, schauspieler whatever eingeben um daraufzukommen

