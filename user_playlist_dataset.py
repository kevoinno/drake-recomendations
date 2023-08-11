import time
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file

# Initialize the Spotify API client with client credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

# List of playlist IDs
playlist_ids = ['playlist_id_1', 'playlist_id_2', 'playlist_id_3', 'playlist_id_4', 'playlist_id_5']

# Function to retrieve audio features for a list of track IDs
def get_audio_features(track_ids):
    audio_features = sp.audio_features(tracks=track_ids)
    return audio_features

# Iterate over each playlist
for playlist_id in playlist_ids:
    # Retrieve playlist tracks
    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items.track.id')

    # Extract track IDs
    track_ids = [track['track']['id'] for track in playlist_tracks['items']]

    # Retrieve audio features for the tracks
    audio_features = get_audio_features(track_ids)

   
