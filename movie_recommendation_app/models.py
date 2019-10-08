from django.db import models

# Create your models here.
class Movie( models.Model ):
    #movieId = models.PositiveIntegerField( primary_key=True  )
    title = models.CharField( max_length=128, default="" )
    genres = models.CharField( max_length=128, default="" )

    def __str__( self ):
        return "[{}] {} {}".format( self.id, self.title, self.genres )

class Rating( models.Model ):
    class Meta:
        unique_together = ( ( "userId", "movie" ), )

    userId = models.PositiveIntegerField()
    movie = models.ForeignKey( "Movie", on_delete=models.PROTECT )
    rating = models.FloatField( default=0.0 )
    rating_predicted = models.FloatField( default=0.0 )
    timestamp = models.FloatField( default=0.0 )

    def __str__( self ):
        return "[{}] {} {} {} {}".format( self.userId, self.movie, self.rating,
                                            self.rating_predicted, self.timestamp )