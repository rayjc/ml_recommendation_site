import json

from django.contrib.auth import authenticate, decorators, get_user_model, login, logout
from django.db.models import Avg, Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView

from movie_recommendation_app.forms import RatingFormSet, SignUpForm
from movie_recommendation_app.models import Rating, Movie
from movie_recommendation_app.recommendation import Recommendation

USER = get_user_model()
# Create your views here.

def rate_movies( request ):
    template_name = 'movie_recommendation_app/rate_movies.html'
    heading_message = 'Movie Recommendation'
    # if request.method == 'GET':
    #     formset = RatingFormSet( request.GET or None )
    # elif request.method == 'POST':
    if request.method == 'POST':
        formset = RatingFormSet( request.POST )
        if formset.is_valid():
            ## Create a new user
            tempUserId = USER.objects.all().aggregate( Max( 'id' ) )[ "id__max" ] + 1
            userObj = USER.objects.create_user( username=str(tempUserId),
                                                email=(str(tempUserId)+"@sample.com"),
                                                is_active=False )
            for form in formset:
                # extract user input
                movie = form.cleaned_data.get( 'movie' )
                star = form.cleaned_data.get( 'rating' )
                # create or update Rating table
                if movie and star:
                    newStar, created = Rating.objects.get_or_create( 
                        user=userObj, movie=Movie.objects.get( title=movie ),
                        rating=star )
                    if not created:
                        Rating.objects.update_or_create( 
                            user=userObj, movie=Movie.objects.get( title=movie ),
                            defaults={ "rating": star } )

            recommendation = Recommendation()
            recommendation.predictUserRating()
            recommendation.updatePredictedRating( userObj.id )

            # redirect to movie recommendation page
            #return redirect_lazy( 'recommendation' )
            return redirect( "recommendation", user_Id=userObj.id )
    else:
        formset = RatingFormSet( None )
    return render( request, template_name, {
        'formset': formset,
        'heading': heading_message,
    } )

def movie_autocomplete( request ):
    if request.is_ajax():
        data = request.GET.get('term', '')
        queryResult = Movie.objects.filter(title__startswith=data).order_by("title")
        results = []
        print( queryResult )
        for movie in queryResult:
            results.append(movie.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class RecommendationListView( ListView ):
    model = Rating
    template_name = "movie_recommendation_app/recommendation_list.html"
    context_object_name = "recommendation_list"
    
    def get_queryset(self):
        queryset = super(RecommendationListView, self).get_queryset()
        if self.kwargs.get("user_Id"):
            newUserId = self.kwargs.get("user_Id")
            queryset = queryset.filter( user_id=newUserId )\
                                .order_by( "-rating_predicted" )[:20]
        return queryset

class MovieDetailView( DetailView ):
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie_rating"] = round( 
            Rating.objects.filter( movie__pk=kwargs.get("object").pk )
                                                    .aggregate( Avg( "rating" ) )
                                                    .get( "rating__avg" ), 2
        )
        return context

class MovieListView( ListView ):
    model = Movie
    template_name = "movie_recommendation_app/movie_list.html"
    ordering = [ "-title" ]
