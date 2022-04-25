import json
import requests
import tempfile
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import tmdbsimple as tmdb
from movie.API_KEY import API_KEY

from django.core import files
from django.shortcuts import render, HttpResponse

from .models import Movie,Genre
from account.models import USER

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
    if len(trailer['results'])>0:
        trailer = "https://www.youtube.com/embed/" + trailer['results'][0]["key"]
    else:
        trailer =  ""
    movie = movie.info()
    context = {
        "id":id,
        "title": movie['title'],
        "overview": movie['overview'].replace('\"',"'"),
        "trailer": trailer,
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

def temp_file_image(poster):
    response = requests.get(poster, stream=True)

    lf = tempfile.NamedTemporaryFile()

    for block in response.iter_content(1024 * 8):
        if not block:
            break
        lf.write(block)
    return files.File(lf)

def get_movie(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    geners_list = [gener.tag for gener in movie.geners.all()]
    return {
        "id":movie_id,
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

def save_movie(movie_id,context):
    movie = Movie(id=int(movie_id), title=context['title'],
                                 overview=context['overview'], trailer=context["trailer"],
                                 duration=context["duration"], release_date=context["release_date"],
                                 rating=context["rating"], votes=context["votes"],
                                 poster=temp_file_image(context["poster"])
                                 )
    movie.save()
    for gener in context["geners"]:
        movie.geners.add(get_gener(gener))

def get_gener(tag):
    try:
        return Genre.objects.get(tag=tag.upper())
    except:
        return Genre.objects.create(tag=tag.upper()).save()

def predict(request):
    movies = USER.objects.get(pk=request.user.id).favorite
    ratings = pd.read_csv('movie/ratings.csv')
    if not movies:
        return HttpResponse("Add Movies to your favorite first")

    for movie in movies:
        movie = convert_TMDB_to_id(int(movie))
        if movie:
            ratings.loc[-1] = [611,int(movie),5,0]
            ratings= ratings.reset_index(drop=True)

    ratings.loc[-1] = [611, 2, 5, 0]
    ratings = ratings.reset_index(drop=True)
    X_train, X_test = train_test_split(ratings, test_size = 0.30, random_state = 42)

    # pivot ratings into movie features
    user_data = X_train.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(0)

    # make a copy of train and test datasets
    dummy_train = X_train.copy()
    dummy_test = X_test.copy()

    dummy_train['rating'] = dummy_train['rating'].apply(lambda x: 0 if x > 0 else 1)
    dummy_test['rating'] = dummy_test['rating'].apply(lambda x: 1 if x > 0 else 0)

    # The movies not rated by user is marked as 1 for prediction
    dummy_train = dummy_train.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(1)

    # The movies not rated by user is marked as 0 for evaluation
    dummy_test = dummy_test.pivot(index ='userId', columns = 'movieId', values = 'rating').fillna(0)


    # User Similarity Matrix using Cosine similarity as a similarity measure between Users
    user_similarity = cosine_similarity(user_data)

    user_similarity[np.isnan(user_similarity)] = 0

    user_predicted_ratings = np.dot(user_similarity, user_data)


    user_final_ratings = np.multiply(user_predicted_ratings, dummy_train)

    moviearray = user_final_ratings.iloc[610].sort_values(ascending = False)[0:49]

    movie_list = []

    for movie in list(moviearray.index.values):
        movie_id=convert_id_to_TMDB(movie)
        try:
            context = get_movie(movie_id)
        except:
            context = get_movie_info(int(movie_id))
            save_movie(movie_id, context)
            context = get_movie(movie_id)
        movie_list.append(context)

    print(movie_list)
    return render(request,'movie/suggestion.html',{"suggestions":movie_list})

# Create your views here.
def movie_view(request, movie_id, *args, **kwargs):
    if not convert_TMDB_to_id(int(movie_id)):
        return HttpResponse('Error 404')

    try:
        context = get_movie(movie_id)
        return render(request,'movie/movie_detail.html', context)
    except:
        context = get_movie_info(int(movie_id))
        save_movie(movie_id, context)
        context = get_movie(movie_id)
        return render(request,'movie/movie_detail.html', context)  # return render(request,"account/profile.html",context)
