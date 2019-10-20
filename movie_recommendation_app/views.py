from django.shortcuts import render, redirect
from django.views.generic import ListView

from movie_recommendation_app.forms import RatingFormset
from movie_recommendation_app.models import Rating, Movie

# Create your views here.

def rate_movies( request ):
    template_name = 'movie_recommendation_app/rate_movies.html'
    heading_message = 'Movie Recommendation'
    if request.method == 'GET':
        formset = RatingFormset( request.GET or None )
    elif request.method == 'POST':
        formset = RatingFormset( request.POST )
        if formset.is_valid():
            ## For simplicity this creates a new userId without collision
            ## this is needed since there's no User model
            tempUserId = max( set( map( lambda q: q[ "userId" ], 
                                Rating.objects.all()
                                .values( "userId" ).distinct() ) ) ) + 1
            for form in formset:
                # extract user input
                movie = form.cleaned_data.get( 'movie' )
                star = form.cleaned_data.get( 'rating' )
                # create or update Rating table
                if movie and star:
                    newStar, created = Rating.objects.get_or_create( 
                        userId=tempUserId, movie=Movie.objects.get( id=movie ),
                        rating=star )
                    if not created:
                        Rating.objects.update_or_create( 
                            userId=tempUserId, movie=Movie.objects.get( id=movie ),
                            rating=star )
            # redirect to movie recommendation page
            #return redirect_lazy( 'recommendation' )
            # add newUserid used to create entry to queue and pass to session
            if not isinstance( request.session.get( "newUserIds" ), list ):
                request.session[ "newUserIds" ] = [ tempUserId ]
            else:
                request.session[ "newUserIds" ] = request.session[ "newUserIds" ].append( tempUserId )
            
            if int( request.POST.get( "form-TOTAL_FORMS" ) ) > 1:
                return redirect( "recommendation" )
    return render( request, template_name, {
        'formset': formset,
        'heading': heading_message,
    } )

# def loadingView( request ):
#     template_name = 'movie_recommendation_app/loading.html'
#     heading_message = 'Now Loading...'

#     # TODO: invoke ml algo on newUserId

# def recommendationView( request ):
#     newUserId = request.session.get( "newUserId" )
#     if newUserId:
#         ## TODO


#         recDict = { "movies": [] }
#         return render( request, "movie_recommendation_app/recommendation.html",
#                         context=recDict )
#     else:
#         return HttpResponse( "Nothing to show yet..." )

class RecommendationListView( ListView ):
    model = Rating
    template_name = "movie_recommendation_app/recommendation_list.html"
    context_object_name = "recommendation_list"
    
    def get_queryset(self):
        queryset = super(RecommendationListView, self).get_queryset()
        if self.request.session.get( "newUserIds" ):
            newUserId = self.request.session.get( "newUserIds" ).pop(0)
            queryset = queryset.filter( userId=newUserId )\
                                .order_by( "-rating" )[:10]
        return queryset

class MovieListView( ListView ):
    model = Movie
    template_name = "movie_recommendation_app/movie_list.html"
    ordering = [ "-title" ]