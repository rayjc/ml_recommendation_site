from django.urls import path
from movie_recommendation_app import views

urlpatterns = [
    path( '', views.rate_movies, name="rate_movies" ),
    path( 'recommendation/<int:user_Id>', views.RecommendationListView.as_view(), name="recommendation" ),
    path( 'movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
    path( 'ajax/search/', views.movie_autocomplete, name="movie_autocomplete"),
    path( 'register', views.RegistrationTemplateView.as_view(), name="register" )
]