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
    path("movies/<str:pk>/", views.movie_detail, name="movie_detail"),  # Custom movie detail page

    # Actor related URLs
    path("actors/", views.actor_list, name="actor_list"),
    path("actors/<int:pk>/", views.actor_details, name="actor_details"),  # Actor detail page
    # For custom actors (using custom_id)
    path("actors/<str:pk>/", views.actor_detail, name="actor_detail"),  # Custom actor detail page
    

    # Director related URLs
    path("directors/", views.director_list, name="director_list"),
    path("directors/<int:pk>/", views.director_details, name="director_details"),  # Director detail page
    path("directors/<str:pk>/", views.director_detail, name="director_detail"),  # Custom director detail page


    # Authentication URLs
    path("signup/", views.signup, name="signup"),  # Signup page
    path("login/", views.user_login, name="user_login"),      # Login page
    path("logout/", views.user_logout, name="logout"),  # Logout path

    # Create page (for adding new movies, actors, directors)
    path("create/", views.create, name="create"),

    # Success page
    path("success/", views.success, name="success"),

    path('all_movies/', views.all_movies, name='all_movies'),
    path('recent_movies/', views.recent_movies, name='recent_movies'),

    #watchlist
    path('movies/<int:pk>/', views.movie_details, name='movie_details'),
    path('watchlist/toggle/<int:pk>/', views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.watchlist_view, name='watchlist'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



