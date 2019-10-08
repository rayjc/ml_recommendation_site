import os
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "ml_recommendation_site.settings" )
import django
django.setup()

import csv
import os

from movie_recommendation_app.models import Movie, Rating

MOVIES_CSV_PATH = os.path.join( "data", "MovieLens-Sept-2018", "movies.csv")
RATINGS_CSV_PATH = os.path.join( "data", "MovieLens-Sept-2018", "ratings.csv")

def addMovie( movieId, title, genres ):
    movie = Movie.objects.get_or_create( id=movieId, title=title,
                                        genres=genres )[ 0 ]
    movie.save()
    return movie

def addRating( userId, movieQueryObj, rating, timestamp ):
    ## Note: using get_or_create() would may return a query set since Rating
    ##       uses composite key
    Rating.objects.create( userId=userId, movie=movieQueryObj, rating=rating,
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
            addRating( userId=row[ "userId" ],
                        movieQueryObj=Movie.objects.get( id=row[ "movieId" ] ),
                        rating=row[ "rating" ],
                        timestamp=row[ "timestamp"] )


if __name__ == "__main__":
    populate()