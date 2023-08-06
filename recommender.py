#Import libraries
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file


#Get's user's inputted track name
def get_user_input():
    return input("Enter the name of the track: ")

#Function that calls the API to search the track the user inputted. Returns a dictionary of the audio features of the user track
def make_api_call(client_id, client_secret, user_input):
    # Initialize the Spotify API client with client credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    #Make API call to search for the user's song and extract the audio features of the song if a valid song
    search_results = sp.search(q=user_input, type='track', limit=1)
    if search_results['tracks']['items']:
        input_track = search_results['tracks']['items'][0]
        input_features = sp.audio_features(input_track['id'])[0]
    else:
        print("Song not found. Please try another song.")
        exit()
    return input_features

#Scales all data before computing cosine similarity matrix
def preprocess_data(input_features, df, selected_features):
    #Create an array of the user's track audio features
    user_song_features = pd.DataFrame(input_features, index = [0])[selected_features].copy()

    #Combine the user's song features with the song features in the dataset for feature scaling
    all_features = pd.concat([user_song_features, df])

    scaler = StandardScaler()
    all_features_scaled = scaler.fit_transform(all_features)

    user_features = all_features_scaled[:1, :].copy()
    dataset_features = all_features_scaled[1:, :].copy()
    
    return user_features, dataset_features

#Computes cosine similiarity matrix and then returns the recommended songs
def recommender(user_features, dataset_features, df_all_cols, n_songs):
    #Compute the cosine simliarity between the user's track and other songs
    cosine_similarity_scores = cosine_similarity(user_features, dataset_features)

    #Get the index of similar songs 
    similar_song_indices = np.argsort(cosine_similarity_scores)[0][-n_songs:][::-1]

    #Get recommended songs using the index
    recommended_songs = df_all_cols.iloc[similar_song_indices]

    return recommended_songs['name'].tolist()

#Main function that does the song recommendation in the terminal
def main():
    DATASET_NAME = 'tracks_features.csv'

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

    #(DELETE LATER) Use only ~200 rows of data because Drake has less than 200 tracks
    df = df[:200][selected_features].copy()

    #Getting user track
    user_input = get_user_input()

    #Make API call to search
    input_features = make_api_call(creds.CLIENT_ID, creds.CLIENT_SECRET, user_input)

    #Scale data
    user_features, dataset_features = preprocess_data(input_features, df, selected_features)

    #Recommending system
    print(recommender(user_features, dataset_features, df_all_cols, 5))

if __name__ == '__main__':
    main()


