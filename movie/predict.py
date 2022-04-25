import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

def convert_TMDB_to_id(TMDB_id):
    data_set = pd.read_csv('links.csv')
    data_set = data_set.set_index("tmdbId")
    try:
        id = int(data_set.loc[TMDB_id, 'movieId'])
        return id
    except:
        return None

def convert_id_to_TMDB(id):
    data_set = pd.read_csv('links.csv')
    data_set = data_set.set_index("movieId")
    TMDB_id = int(data_set.loc[id, 'tmdbId'])
    return TMDB_id

def predict(movies):
    ratings = pd.read_csv('ratings.csv')
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
        movie_list.append(convert_id_to_TMDB(movie))


    return movie_list

predict({9387,315011,399035,5820,9334,847,45408,24825,11536,22,284052,68726,27205})