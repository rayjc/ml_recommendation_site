import numpy as np

from scipy.sparse import csr_matrix as sparse_matrix
from movie_recommendation_app.models import Movie, Rating 

def create_user_item_matrix( ratings, userKey="userId", itemKey="movie", ratingKey="rating" ):

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


X, userMap, itemMap, userInvMap, itemInvMap, userInd, itemInd = create_user_item_matrix(Rating)