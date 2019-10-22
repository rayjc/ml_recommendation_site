from django import forms
#from django.forms import formset_factory

from movie_recommendation_app.models import Movie

class RatingForm(forms.Form):
    ## iterable of 2-tuples of ( primary key, title )
    #movieChoices = list( map( lambda q: ( q[ "id" ], q[ "title" ] ),
    #                    Movie.objects.all().order_by( "title" ).values( "id", "title" ) ) )
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


    # movie = forms.CharField( label="Movie Name", widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Enter Movie Name here'
    #     }))
    
    #movieChoices.insert( 0, ( "", "-Select Movie-") )
    movie = forms.CharField( label='Movie', required=True )
    movie.widget.attrs.update( { 'class': 'form-control textSearch',
                                    #'id': 'textSearch',
                                    'name': 'movie',
                                    'placeholder': 'Enter Movie',
                                    'required': 'required' } )
    ratingChoices.insert( 0, ( "","-" ) )
    rating = forms.ChoiceField( label='Rating', choices=ratingChoices )
    rating.widget.attrs.update( { 'class': 'form-control',
                                    'placeholder': 'Select Rating' } )

    def clean( self ):
        super( RatingForm, self ).clean()

        movie = self.cleaned_data.get( 'movie' )
        rating = self.cleaned_data.get( 'rating' )

        if movie == "":
            self._errors['movie'] = self.error_class(['Invalid movie choice']) 
        if rating == "-":
            self._errors['rating'] = self.error_class(['Invalid rating choice'])

        return self.cleaned_data


RatingFormset = forms.formset_factory( RatingForm, extra=1 )