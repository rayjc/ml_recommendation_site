import numpy as np

from movie_recommendation_app.models import Movie, Rating
from movie_recommendation_app.pca import PCA
from scipy.sparse import csr_matrix as sparse_matrix


class Recommendation:

    def __init__( self ):
        ( self.X,
            self.userMap,
            self.itemMap,
            self.userInvMap,
            self.itemInvMap,
            self.userInd,
            self.itemInd )= self.create_user_item_matrix(Rating)
        self.Xnew = None

    def create_user_item_matrix( self, ratings, userKey="user", itemKey="movie", ratingKey="rating" ):

        userMap = { 
            userId: index for index, userId in enumerate( 
                map( lambda q: q[ userKey ], 
                    ratings.objects.all()
                        .order_by( userKey ).values( userKey ).distinct() ) 
            ) 
        }
        itemMap = { 
            itemId: index for index, itemId in enumerate(
                np.unique( list( map( lambda q: q[ itemKey ], 
                                        ratings.objects.all()
                                            .order_by( userKey ).values( itemKey ) ) ) )
                # DISTINCT ON sql only works with postgre
                # map( lambda q: q[ itemKey ], 
                #     ratings.objects.all()
                #         .order_by( userKey ).values( itemKey ).distinct( itemKey ) )
            )
        }

        userInvMap = { 
            index: userId for index, userId in enumerate( 
                map( lambda q: q[ userKey ], 
                    ratings.objects.all()
                        .order_by( userKey ).values( userKey ).distinct() ) 
            ) 
        }
        itemInvMap = { 
            index: itemId for index, itemId in enumerate( 
                np.unique( list( map( lambda q: q[ itemKey ], 
                                        ratings.objects.all()
                                            .order_by( userKey ).values( itemKey ) ) ) )
                # DISTINCT ON sql only works with postgre
                # map( lambda q: q[ itemKey ], 
                #     ratings.objects.all()
                #         .order_by( userKey ).values( itemKey ).distinct() ) 
            ) 
        }

        userInd = [ 
            userMap[ userId ] 
            for userId in map( 
                lambda q: q[ userKey ],
                ratings.objects.all().order_by( userKey ).values( userKey ) ) 
        ]
        itemInd = [ 
            itemMap[ itemId ] 
            for itemId in map( 
                lambda q: q[ itemKey ],
                ratings.objects.all().order_by( userKey ).values( itemKey ) ) 
        ]

        n = len( userMap )
        d = len( itemMap )

        X = sparse_matrix( ( 
            list( map( lambda q: q[ ratingKey ],
                        ratings.objects.all().order_by( userKey ).values( ratingKey ) ) ),
            ( userInd, itemInd ) ), shape=( n, d ) )
        
        return X, userMap, itemMap, userInvMap, itemInvMap, userInd, itemInd


    def predictUserRating( self ):

        d = len( self.itemMap )
        print( "{} movies".format( d ) )
        
        ## predict movie rating for user through PCA
        model = PCA(k=d//70)
        model.fit( self.X )
        self.Xnew = model.expand( model.compress( self.X ) )


    def updatePredictedRating( self, userId ):
        ## Sort the prediction
        sortedMovieInds = np.argsort( -self.Xnew[ self.userMap[ userId ] ] ).getA1()
        sortedMovieIds = [ self.itemInvMap[ ind ] for ind in sortedMovieInds ]
        ## Find the movies that user likes and has submitted in the form
        moviesUserLiked = set( map( lambda q: q["movie"],
                                    Rating.objects.filter( user_id=userId, rating__gte=3.0 ).values( "movie" ) ) )
        ## Construct a list of ( movie, rating_predicted ) to be update/written to db
        ratingPairs = [
            ( movieId, self.Xnew[ self.userMap[ userId ], movieInd ] )
            for movieId, movieInd in zip( sortedMovieIds, sortedMovieInds )
            if self.Xnew[ self.userMap[ userId ], movieInd ] > 0 and movieId not in moviesUserLiked
        ]

        ## Update the first 100 top rating based on prediction
        numUpdates = 100 if len( ratingPairs ) > 100 else len( ratingPairs )
        Rating.objects.bulk_update( [
            Rating.objects.update_or_create( user_id=userId,
                                                movie=Movie.objects.get( id=movieId ),
                                                defaults={ "rating_predicted": movieRating } )[0]
            for movieId, movieRating in ratingPairs[:numUpdates]
        ], ['rating_predicted'] )
