from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'IMBD_app'

urlpatterns=[
    path("", views.home, name="home"),
    path("movie/", views.movie, name="movie"),
    path("actor/", views.actor, name="actor"),
    path("director/", views.director, name="director"),
    path("create/", views.create, name="create"),
    path("success/", views.success, name="success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# nach der url einfach / film, schauspieler whatever eingeben um daraufzukommen

