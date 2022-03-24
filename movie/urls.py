from django.urls import path

from movie.views import movie_view


app_name = 'movie'

urlpatterns = [
    #Profile
    path('<movie_id>/',movie_view,name='view'),

]