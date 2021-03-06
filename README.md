# movie_recommendation_app

## Movie Recommendation Web Application

This web application employs the use of Principal Component Analysis (PCA) for recommending movies based on user submitted movie ratings. <br />
1. Movie Ratings Form:
This form consists of dynamically generated rows for movie ratings and autocomplete fields. Users can fill in several movies they like or dislike and their corresponding ratings for each movie.
![1: Movie Ratings Submission](figures/autocomplete.png)
1. Movie Recommendation List:
A list of movie recommendations will be generated based on the submitted form. This list is the result of executing PCA to predict user-ratings of other movies in the database. Users may click on each movie to be redirected the respected detail page. Note: any movie that an user has rated will not be in this list of recommendation.
![2: Movie Recommendations ](figures/recommendation.png)
1. User Authentication:
This web app keeps track of movie ratings submitted by authenticated users and continually updates recommendations.
![3: Login ](figures/login.png)
![4: Personalized Recommendation ](figures/user_recommendation.png)

### Included:
* source code
* movie data (data/) released by MovieLens
* populate_movie_app.py: a script to extract .csv movie data and populate database

### Requirement:
* 3rd party python packages: numpy, scipy
* Python 3 (tested with 3.7.3 on Windows)
* Django (tested with 2.2.3 on Windows)

### To run:
```
python manage.py runserver
```

### Live Site:
[~~Live on AWS Elastic Beanstalk~~](http://movie-recommendation.us-west-1.elasticbeanstalk.com/) <br/>
Note: please refer to [deploy branch](https://github.com/rayjc/ml_recommendation_site/tree/deploy) for source!
