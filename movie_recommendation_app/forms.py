from django import forms
#from django.forms import formset_factory

from movie_recommendation_app.models import Movie

class RatingForm(forms.Form):
    ## iterable of 2-tuples of ( primary key, title )
    movieChoices = set( map( lambda q: q[ "title" ],
                       Movie.objects.all().order_by( "title" ).values( "title" ) ) )
    ratingChoices = [ ( val * 0.5, str( val * 0.5 ) ) for val in range( 0, 11 ) ]

    movie = forms.CharField( label='Movie', required=True )
    movie.widget.attrs.update( { 'class': 'form-control textSearch',
                                    #'id': 'textSearch',
                                    'name': 'movie',
                                    'placeholder': 'Enter Movie',
                                    'required': 'required' } )
    rating = forms.ChoiceField( label='Rating', choices=([(-1, " ")] + ratingChoices ) )
    rating.widget.attrs.update( { 'class': 'form-control',
                                    'placeholder': ' ' } )

    def clean( self ):
        super( RatingForm, self ).clean()

        movie = self.cleaned_data.get( 'movie' )
        rating = self.cleaned_data.get( 'rating' )

        if movie not in RatingForm.movieChoices:
            raise forms.ValidationError( "Invalid movie detected! "
                                        "Sorry this movie does not exist in database, "
                                        "please select a movie through autocomplete." )
        validRatingChoices = set( map( lambda pair: pair[1], RatingForm.ratingChoices ) )
        if rating not in validRatingChoices:
            raise forms.ValidationError( "Invalid rating detected!" )

        # if movie == "":
        #     self._errors['movie'] = self.error_class(['Invalid movie choice']) 
        # if rating == "-":
        #     self._errors['rating'] = self.error_class(['Invalid rating choice'])`

        return self.cleaned_data


class BaseRatingFromSet( forms.BaseFormSet ):
    """
    Override formset level data validation.
    """
    def clean( self ):
        if any( self.errors ):
            return
        
        movies = set()
        for form in self.forms:
            movie = form.cleaned_data.get( "movie" )
            if movie in movies:
                raise forms.ValidationError( "Multiple ratings on the same movie detected!" )
            movies.add( movie )
        
        if len( movies ) < 2:
            raise forms.ValidationError( "Please rate at least two movies for the best result!" )


RatingFormSet = forms.formset_factory( RatingForm, formset=BaseRatingFromSet,
                                        extra=1, max_num=50 )