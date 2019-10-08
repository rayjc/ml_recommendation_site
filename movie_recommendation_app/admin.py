from django.contrib import admin
from movie_recommendation_app.models import Movie, Rating

# Register your models here.
admin.site.register( Movie )
admin.site.register( Rating )