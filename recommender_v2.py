# Import libaries
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Reading in song dataset
df = pd.read_csv('drake_songs_dataset.csv')

# Checking for null values
df.isna().sum()

# Get features we want to include in the cosine similarity calculation
features = [
        'danceability', 'energy', 'key', 'loudness',
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo'
    ]

# Function to get information about the user's track, returns track info (dictionary) or None if not a valid song
def get_user_track(user_track):
    # Make API call to verify if it is a spotify song
    # Initialize the Spotify API client with client credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

    # Make API call to search for the user's song made by Drake and extract the audio features of the song if a valid song
    search_results = sp.search(q='track:' + user_track, type='track', limit=1)

    # Check if song is an actual track in Spotify
    if search_results['tracks']['items']:
        return search_results
    return None

# Function that calculates cosine similarity and makes recommendations
def cosine_recs(drake_dataset, features, n_recs, user_track):
    # Get the user's track
    user_track = get_user_track(user_track)
    # Check if valid track
    if user_track is not None:
        # Check if track is in the drake song dataset
        if user_track['tracks']['items'][0]['name'] in drake_dataset['track_name'].values:
            # Start recommendation system
            
            # Create an indices series to get the index of a track given its name
            indices = pd.Series(drake_dataset.index, index = drake_dataset['track_name'])
            user_idx = indices[user_track['tracks']['items'][0]['name']]

            # Scale data
            scaler =  StandardScaler()
            scaled_df = scaler.fit_transform(drake_dataset[features])

            # Calculate cosine similarity matrix
            cos_matrix = cosine_similarity(scaled_df, scaled_df)

            # Create a series with the similarity scores in descending order
            scores = pd.Series(cos_matrix[user_idx]).sort_values(ascending = False)

            # Get indexes of top N recommendations
            rec_indexes = list(scores.iloc[1:(n_recs + 1)].index)

            return df.iloc[rec_indexes]
            
    return None
    
