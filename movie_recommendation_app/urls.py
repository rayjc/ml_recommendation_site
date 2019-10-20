from django.urls import path
from movie_recommendation_app import views

urlpatterns = [
    path( '', views.rate_movies, name="rate_movies" ),
    path( 'recommendation/<int:userId>', views.RecommendationListView.as_view(), name="recommendation" ),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
]