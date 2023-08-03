#Import libraries
import json
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds

#Function that gets all the playlists from all the json files in the playlists folder
def get_json_files(file_path, json_list, playlist_output):
    for file in json_list:
        with open(os.path.join(file_path, file), 'r', encoding = 'utf-8') as f:
            data = json.load(f)
            playlists = data['playlists']
            playlist_output.extend(playlists)
    return playlist_output

# Path to the directory containing the downloaded JSON files
data_dir = 'C:/Users/kevoi/OneDrive/Desktop/ds-projects/spotify-recs/data'

# List all JSON files in the data directory
json_files = [file for file in os.listdir(data_dir) if file.endswith('.json')]

# Initialize an empty list to store all playlists
all_playlists = []

all_playlists = get_json_files(data_dir, json_files, all_playlists)[:2]

#Function that extracts the track_uri, track_name, artist_name, and duration_ms from all the tracks in all the playlists. Then goes through each track and gets the relevant audio features for each track Returns a dataframe
def extract_features(playlist_list):
    # Initialize the Spotify API client with client credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = creds.CLIENT_ID, client_secret = creds.CLIENT_SECRET))

    #Create empty lists to store relevant data
    track_uri_list = []
    track_name_list = []
    artist_name_list = []
    duration_ms_list = []

    for playlist in playlist_list:
        #Extract all tracks from a single playlist and store into tracks variable
        tracks = playlist['tracks']
        #Iterate through all tracks in tracks and extract relevant features
        for track_info in tracks: 
            track_uri_list.append(track_info['track_uri'])
            track_name_list.append(track_info['track_name'])
            artist_name_list.append(track_info['artist_name'])
            duration_ms_list.append(track_info['duration_ms'])
    
    #Create empty lists to store audio data
    danceability_list = []
    energy_list = []
    key_list = []
    loudness_list = []
    speechiness_list = []
    acousticness_list = []
    instrumentalness_list = []
    liveness_list = []
    valence_list = []
    tempo_list = []

    #Iterate through list of track uris and add to audio feature lists
    for track_uri in track_uri_list:
        #Extract audio feature using Spotify Web API
        extracted_audio_features = sp.audio_features(track_uri)

        danceability_list.append(extracted_audio_features[0]['danceability'])
        energy_list.append(extracted_audio_features[0]['danceability'])
        key_list.append(extracted_audio_features[0]['danceability'])
        loudness_list.append(extracted_audio_features[0]['danceability'])
        speechiness_list.append(extracted_audio_features[0]['danceability'])
        acousticness_list.append(extracted_audio_features[0]['danceability'])
        instrumentalness_list.append(extracted_audio_features[0]['danceability'])
        liveness_list.append(extracted_audio_features[0]['danceability'])
        valence_list.append(extracted_audio_features[0]['danceability'])
        tempo_list.append(extracted_audio_features[0]['danceability'])

    #Constructing  a dataframe from all features
    data = {
        'track_uri': track_uri_list,
        'track_name': track_name_list,
        'artist_name': artist_name_list,
        'duration_ms': duration_ms_list,
        'danceability' : danceability_list,
        'energy' : energy_list,
        'key' : key_list,
        'loudness' : loudness_list,
        'speechiness' : speechiness_list,
        'acousticness' : acousticness_list,
        'instrumentalness' : instrumentalness_list,
        'liveness' : liveness_list,
        'valence' : valence_list,
        'tempo_list' : tempo_list
    }

    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    return df

df = extract_features(all_playlists)

#Export dataframe to a csv file
df.to_csv('song_dataset.csv', index = False)

print('Finished exporting csv')


