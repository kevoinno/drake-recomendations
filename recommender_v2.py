# Import libaries
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler

# Reading in song dataset
df = pd.read_csv('drake_songs_dataset.csv')


# Get features we want to include in the cosine similarity calculation
features = [
        'danceability', 'energy', 'key', 'loudness',
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo'
    ]


# Function that calculates cosine similarity and makes recommendations
def cosine_recs(drake_dataset, features, n_recs, user_track):
    # Check if valid track
    if user_track is not None:
        # Check if track is in the drake song dataset
        if user_track in drake_dataset['track_name'].values:
            # Start recommendation system
            
            # Create an indices series to get the index of a track given its name
            indices = pd.Series(drake_dataset.index, index = drake_dataset['track_name'])
            user_idx = indices[user_track]

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

# Function that calculates euclidean distance similarity and makes recommendations
def euclidean_recs(drake_dataset, features, n_recs, user_track):
    # Check if valid track
    if user_track is not None:
        # Check if track is in the drake song dataset
        if user_track in drake_dataset['track_name'].values:
            # Start recommendation system
            
            # Create an indices series to get the index of a track given its name
            indices = pd.Series(drake_dataset.index, index = drake_dataset['track_name'])
            user_idx = indices[user_track]

            # Scale data
            scaler =  StandardScaler()
            scaled_df = scaler.fit_transform(drake_dataset[features])

            # Calculate euclidean distance matrix
            cos_matrix = euclidean_distances(scaled_df, scaled_df)

            # Create a series with the similarity scores in descending order
            scores = pd.Series(cos_matrix[user_idx]).sort_values(ascending = False)

            # Get indexes of top N recommendations
            rec_indexes = list(scores.iloc[1:(n_recs + 1)].index)

            return df.iloc[rec_indexes]
            
    return None
    
