from django.contrib.auth import authenticate, decorators, get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from movie_recommendation_app.forms import ActiveAuthenticationForm, SignUpForm

USER = get_user_model()

class RegisterTemplateView( TemplateView ):
    template_name = "movie_recommendation_app/register.html"
    context_object_name = "signup_form"

    def post( self, request, *args, **kwargs ):
        signUpForm = SignUpForm( request.POST )

        if signUpForm.is_valid():
            name = signUpForm.cleaned_data.get( 'userName' )
            password = signUpForm.cleaned_data.get( 'userPassword' )
            email = signUpForm.cleaned_data.get( 'userEmail' )
            userQueryObj = USER.objects.create_user( username=name,
                                                        password=password,
                                                        email=email,
                                                        is_active=True )
            return redirect( "movie_recommendation_app:signup-complete" )

        return self.render_to_response( { 'signup_form': signUpForm } )
    
    def get_context_data( self, **kwargs ):
        context = super( RegisterTemplateView, self ).get_context_data( **kwargs )
        context[ 'signup_form' ] = SignUpForm()
        context[ 'heading' ] = "Registration"
        return context

    # def get( self, request, *args, **kwargs ):
    #     context = {
    #         'signup_form': SignUpForm(),
    #         'heading': "Registration",
    #     }
    #     return super( RegisterTemplateView, self ).render_to_response( context )

class SignUpCompleteTemplateView( TemplateView ):
    template_name = "movie_recommendation_app/signup_complete.html"

class LoginTemplateView( TemplateView ):
    template_name = "movie_recommendation_app/login.html"

    def post( self, request ):
        userName = request.POST.get( 'username' )
        userPassword = request.POST.get( 'password' )

        user = authenticate( username=userName, password=userPassword )
        if user:
            if user.is_active:
                login( request, user )
                return redirect( "movie_recommendation_app:rate_movies" )
            else:
                return HttpResponse( "ACCOUNT IS CURRENTLY NOT ACTIVE" )
        else:
            print( "Username: {} and password {} failed to login".format( userName, userPassword ) )

class ActiveLoginView( LoginView ):
    template_name = "movie_recommendation_app/login.html"
    authentication_form = ActiveAuthenticationForm