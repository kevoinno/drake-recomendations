#Import libraries
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
from sklearn.cluster import KMeans

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

    # Scale data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[selected_features])

    # Perform KMeans
    num_clusters = 5
    kmeans = KMeans(n_clusters = num_clusters, random_state = 42)
    kmeans.fit(scaled_features)

    # Get input track and get features
    user_input = get_user_input()
    
    # Initialize the Spotify API client with client credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

    # Make API call to search for the user's song made by Drake and extract the audio features of the song if a valid song
    search_results = sp.search(q='track:' + user_input + ' artist:Drake', type='track', limit=1)
    if search_results['tracks']['items']:
        pass
    else:
        print("Drake song not found. Please try another song.")
        exit()
    
    print(search_results)
    # Get index of target song
    target_song_index = df.index[df['track_name'] == search_results['tracks']['items'][0]['name']].tolist()[0]

    # Identify the cluster to which the target song belongs
    target_song_features = scaled_features[target_song_index]  # Replace target_song_index with the index of your target song
    target_song_cluster = kmeans.predict([target_song_features])[0]
   
    # Find songs in the same cluster as the target song
    df['cluster'] = kmeans.labels_
    
    songs_in_same_cluster = df[df['cluster'] == target_song_cluster]

    # Now you can recommend songs from the same cluster
    recommended_songs = songs_in_same_cluster.sample(n=5)
    print("Recommended Songs:", recommended_songs)

    


if __name__ == '__main__':
    main()

