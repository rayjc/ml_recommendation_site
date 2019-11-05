from django.contrib.auth.views import logout_then_login
from django.urls import path, include
from movie_recommendation_app.views import core, registration

app_name = 'movie_recommendation_app'

urlpatterns = [
    path( '', core.rate_movies, name="rate_movies" ),
    path( 'recommendation/<int:user_Id>', core.RecommendationListView.as_view(), name="recommendation" ),
    path( 'movie/<int:pk>', core.MovieDetailView.as_view(), name='movie-detail'),
    path( 'ajax/search/', core.movie_autocomplete, name="movie_autocomplete"),
    path( 'user-movies/', core.UserRatedMoviesListView.as_view(), name="user-rated-movies"),
    path( 'accounts/register/', registration.RegisterTemplateView.as_view(), name="register" ),
    path( 'accounts/login/', registration.ActiveLoginView.as_view(), name="login" ),
    path( 'accounts/logout/', logout_then_login, name="logout" ),
    path( 'accounts/signup-complete/', registration.SignUpCompleteTemplateView.as_view(), name="signup-complete" ),
]