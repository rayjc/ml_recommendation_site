from django import forms
#from django.forms import formset_factory

from movie_recommendation_app.models import Movie

class RatingForm(forms.Form):
    ## iterable of 2-tuples of ( primary key, title )
    movieChoices = map( lambda q: ( q[ "id" ], q[ "title" ] ),
                        Movie.objects.all().order_by( "title" ).values( "id", "title" ) )
    ratingChoices = [ ( val * 0.5, str( val * 0.5 ) ) for val in range( 0, 11 ) ]

    # movieName = forms.CharField( label='Movie Name', 
    #     widget=forms.Select(
    #         choices=movieChoices,
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Enter Book Name here' 
    #         } 
    #     )
    # )
    # movie = forms.ModelChoiceField( queryset=Movie.objects.all(),
    #                                 to_field_name="title",
    #                                 empty_label="(Nothing)" )

    movie = forms.ChoiceField( label='Movie', choices=movieChoices )
    movie.widget.attrs.update( { 'class': 'form-control',
                                    'placeholder': 'Select Movie' } )
    rating = forms.ChoiceField( label='Rating', choices=ratingChoices )
    rating.widget.attrs.update( { 'class': 'form-control',
                                    'placeholder': 'Select Rating' } )

RatingFormset = forms.formset_factory( RatingForm, extra=1 )