import os
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "ml_recommendation_site.settings" )
import django
django.setup()

import csv
import os

from django.contrib.auth.models import User
from movie_recommendation_app.models import Movie, Rating

MOVIES_CSV_PATH = os.path.join( "data", "MovieLens-Sept-2018", "movies.csv")
RATINGS_CSV_PATH = os.path.join( "data", "MovieLens-Sept-2018", "ratings.csv")

def addMovie( movieId, title, genres ):
    movie = Movie.objects.get_or_create( id=movieId, title=title,
                                        genres=genres )[ 0 ]
    movie.save()
    return movie

def addRating( user, movieQueryObj, rating, timestamp ):
    ## Note: using get_or_create() would may return a query set since Rating
    ##       uses composite key
    Rating.objects.create( user=user, movie=movieQueryObj, rating=rating,
                            timestamp=timestamp )

def populate():

    ## load movies.csv to database
    with open( MOVIES_CSV_PATH, newline="", encoding='utf-8' ) as f:
        reader = csv.DictReader( f )
        for row in reader:
            print( "Inserting {} {} {}".format( row[ "movieId" ], row[ "title" ],
                                                row[ "genres" ] ) )
            
            addMovie( movieId=row[ "movieId" ], title=row[ "title" ],
                        genres=row[ "genres" ] )

    ## load ratings.csv and create relation
    with open( RATINGS_CSV_PATH, newline="", encoding='utf-8' ) as f:
        reader = csv.DictReader( f )
        for row in reader:
            print( "Inserting {} {} {} {}".format( row[ "userId" ], row[ "movieId" ],
                                                    row[ "rating" ],
                                                    row[ "timestamp" ] ) )
            
            try:
                userQueryObj = User.objects.get( username=row["userId"] )
            except django.core.exceptions.ObjectDoesNotExist:
                userQueryObj = User.objects.create_user( username=row["userId"],
                                                    email=(row["userId"]+"@sample.com"),
                                                    is_active=False )

            addRating( user=userQueryObj,
                        movieQueryObj=Movie.objects.get( id=row[ "movieId" ] ),
                        rating=row[ "rating" ],
                        timestamp=row[ "timestamp"] )


if __name__ == "__main__":
    ## Friendly note: In order to reset the database, please remove db.sqlite3 
    ## and migrations/* except __init__.py prior to running "makemigrations" and
    ## "migrate". You may also need to comment out urlpatterns to prevent 
    ## model imports.
    populate()