#Import libraries
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file

DATASET_NAME = 'tracks_features.csv'

#Read in data as a dataframe
df = pd.read_csv(DATASET_NAME)

#Get audio features
selected_features = [
    'danceability', 'energy', 'key', 'loudness',
    'speechiness', 'acousticness', 'instrumentalness', 
    'liveness', 'valence', 'tempo'
]

#Keeps all columns so that we can extract the recommended song names and artists later
df_all_cols = df.copy()

#(DELETE LATER) Use only ~200 rows of data because Drake has less than 200 tracks
df = df[:100][selected_features].copy()


#Get user's inputted track name
user_input = input("Enter the name of the track: ")

# Initialize the Spotify API client with client credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

#Make API call to search for the user's song and extract the audio features of the song if a valid song
search_results = sp.search(q=user_input, type='track', limit=1)
if search_results['tracks']['items']:
    input_track = search_results['tracks']['items'][0]
    input_features = sp.audio_features(input_track['id'])[0]
else:
    print("Song not found. Please try another song.")
    exit()

#Create an array of the user's track audio features
user_song_features = pd.DataFrame(input_features, index = [0])[selected_features].copy()

#Combine the user's song features with the song features in the dataset for feature scaling
all_features = pd.concat([user_song_features, df])

scaler = StandardScaler()
all_features_scaled = scaler.fit_transform(all_features)

user_features = all_features_scaled[:1, :].copy()
dataset_features = all_features_scaled[1:, :].copy()

#Compute the cosine simliarity between the user's track and other songs
cosine_similarity_scores = cosine_similarity(user_features, dataset_features)
TOP_N = 5 #Top n songs to recommend

#Get the index of similar songs 
similar_song_indices = np.argsort(cosine_similarity_scores)[0][-TOP_N:][::-1]

#Get recommended songs using the index
recommended_songs = df_all_cols.iloc[similar_song_indices]

cosine_similarity
print()
print(recommended_songs)

for i, index in enumerate(similar_song_indices):
    similarity_score = cosine_similarity_scores[0][index]
    print(f"Cosine Similarity Score for recommended song {i + 1}: {similarity_score:.4f}")