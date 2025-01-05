from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'IMBD_app'

urlpatterns = [
    # Homepage
    path("", views.home, name="home"),

    # Movie related URLs
    path("movies/", views.movie_list, name="movie_list"),
    path("movies/<int:pk>", views.movie_details, name="movie_details"),  # Movie detail page
    
    path("movies/<int:pk>/", views.movie_details, name="movie_details"), # Movie details from home.html


    # Actor related URLs
    path("actors/", views.actor_list, name="actor_list"),
    path("actors/<int:pk>/", views.actor_details, name="actor_details"),  # Actor detail page

    # Director related URLs
    path("directors/", views.director_list, name="director_list"),
    path("directors/<int:pk>/", views.director_details, name="director_details"),  # Director detail page

    # Authentication URLs
    path("signup/", views.signup, name="signup"),  # Signup page
    path("login/", views.user_login, name="user_login"),      # Login page
    path("logout/", views.user_logout, name="logout"),  # Logout path

    # Create page (for adding new movies, actors, directors)
    path("create/", views.create, name="create"),

    # Success page
    path("success/", views.success, name="success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


