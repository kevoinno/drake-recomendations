#Import libariers and helper functions
from recommender import get_user_input
from recommender import make_api_call
from recommender import preprocess_data
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file
from sklearn.metrics.pairwise import euclidean_distances


def recommender_euclidean(user_features, dataset_features, df_all_cols, n_songs):
    # Compute the Euclidean distances between the user's track and other songs
    euclidean_distances_scores = euclidean_distances(user_features, dataset_features)

    # Get the index of similar songs based on minimum Euclidean distances
    similar_song_indices = np.argsort(euclidean_distances_scores)[0][:n_songs]

    # Get recommended songs using the index
    recommended_songs = df_all_cols.iloc[similar_song_indices]

    return recommended_songs

#Main function that does the song recommendation in the terminal
def main():
    DATASET_NAME = 'drake_songs_dataset.csv'

    #Read in data as a dataframe
    df = pd.read_csv(DATASET_NAME)

    #Get desired audio features
    selected_features = [
        'danceability', 'energy', 'key', 'loudness',
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo'
    ]

    #Keeps all columns so that we can extract the recommended song names and artists later
    df_all_cols = df.copy()

    #Getting user track
    user_input = get_user_input()

    #Make API call to search
    input_features = make_api_call(creds.CLIENT_ID, creds.CLIENT_SECRET, user_input)

    print(input_features)

    #Remove the user's inputted track from original dataset so it isn't recommended later on
    print(input_features)
    print(f"Shape before removing input track: {df.shape}")
    df = df[df['track_uri'] != input_features['uri']]
    print(f"Shape after removing input track: {df.shape}")
    

    #Remove unnecessary columns so that data can be properly scaled
    df = df[selected_features].copy()

    #Scale data
    user_features, dataset_features = preprocess_data(input_features, df, selected_features)

    #Recommending system
    print(recommender_euclidean(user_features, dataset_features, df_all_cols, 5))

if __name__ == '__main__':
    main()
