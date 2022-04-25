from django.shortcuts import render
from movie.models import Movie
from account.models import USER
from movie.views import get_movie,save_movie,get_movie_info
import random
from time import sleep
import pandas as pd

def generate_random_movie():
	data_set = pd.read_csv('movie/links.csv')
	x = data_set['tmdbId'].sample(n=1)
	try:
		int(x)
		return x
	except:
		return generate_random_movie()

def generate_movie_gener(gener):
	gener = gener.upper()
	while True:
		movie_id = generate_random_movie()
		try:
			movie = get_movie(int(movie_id))
			geners_list = movie["geners"]
		except:
			try:
				sleep(1)
				save_movie(movie_id, get_movie_info(int(movie_id)))
				movie = get_movie(int(movie_id))
				geners_list = movie["geners"]
				if gener in geners_list:
					break
			except:
				data = pd.read_csv('movie/links.csv')
				data = data.drop(index=data[data["tmdbId"]==int(movie_id)].index)
				data.to_csv('movie/links.csv')
	return movie


def get_20_movies(gener):
	# movies = []
	# while True:
	# 	movie = generate_movie_gener(gener)
	# 	if movie not in movies:
	# 		movies.append(movie)
	# 	if len(movies) == 30:
	# 		break
	#
	# return movies
	movies = Movie.objects.filter(geners__tag=gener.upper())
	x = random.randint(0,len(movies)-20)
	return movies[x:x+20]

# Create your views here.
def home_view(request):
	context = {
		'comedy':get_20_movies("Comedy"),
		'action':get_20_movies("Action"),
		'drama':get_20_movies("drama"),
		'thriller':get_20_movies("thriller")
	}
	if request.user.is_authenticated:
		context['favorite'] = USER.objects.get(pk=request.user.id).favorite

	return render(request, "mywebsite/index.html", context)
