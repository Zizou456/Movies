import json
import pandas as pd
import tmdbsimple as tmdb
from movie.API_KEY import API_KEY

from django.shortcuts import render, HttpResponse

from .models import Movie


def get_movie_info(id):
    # BASE URL = 'https://image.tmdb.org/t/p/original'
    # movie.info()
    # poster			info['poster_path']
    # title 			info['title'] => Str
    # genres			info['genres'] => [{'id': 35, 'name': 'Comedy'}]
    # overview		info['overview']
    # duration		info['runtime']
    # release date	info['release_date']
    # Rating			info['vote_average']
    # Vote Count		info['vote_count']
    tmdb.API_KEY = API_KEY
    movie = tmdb.Movies(id)
    trailer = movie.videos()
    movie = movie.info()
    context = {
        "title": movie['title'],
        "overview": movie['overview'].replace('\"',"'"),
        "trailer": "https://www.youtube.com/watch?v="+trailer['results'][0]["key"],
        "geners": [gener['name'] for gener in movie['genres']],
        "duration": movie['runtime'],
        "release_date": movie['release_date'],
        "rating": movie['vote_average'],
        "votes": movie['vote_count'],
        "poster": 'https://image.tmdb.org/t/p/original'+movie['poster_path']
    }
    return context

def convert_id_to_TMDB(id):
    data_set = pd.read_csv('movie/links.csv')
    data_set = data_set.set_index("movieId")
    TMDB_id = int(data_set.loc[id, 'tmdbId'])
    return TMDB_id

def convert_TMDB_to_id(TMDB_id):
    data_set = pd.read_csv('movie/links.csv')
    data_set = data_set.set_index("tmdbId")
    try:
        id = int(data_set.loc[TMDB_id, 'movieId'])
        return id
    except:
        return None


# Create your views here.
def movie_view(request, movie_id, *args, **kwargs):
    if not convert_TMDB_to_id(int(movie_id)):
        return HttpResponse('Error 404')

    try:
        movie = Movie.objects.get(pk=movie_id)
        geners_list = [gener.tag for gener in movie.geners.all()]
        context = {
            "title": movie.title,
            "overview": movie.overview,
            "trailer": movie.trailer,
            "geners": geners_list,
            "duration": movie.duration,
            "release_date": movie.release_date,
            "rating": movie.rating,
            "votes": movie.votes,
            "poster": movie.poster.url
        }

        return HttpResponse(json.dumps(context), content_type="application/json")
    except:
        context = get_movie_info(int(movie_id))
        return HttpResponse(json.dumps(context), content_type="application/json")  # return render(request,"account/profile.html",context)
