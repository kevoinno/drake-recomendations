import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file

# Initialize the Spotify API client with client credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

# List of playlist IDs
playlist_ids = ['5lWxcrl0MTLPS6iEtzYMb6', '0t06SW8VdtNeluu1qSFSNg', '2XF1Qyb2mk2bAi7D0cvhoz', '2WnlmsV0BPt6ydSYK5AoCT', '35WYwjJedrQevOlzBNmXt5']

# Function to retrieve audio features for a list of track IDs
def get_audio_features(track_ids):
    audio_features = sp.audio_features(tracks=track_ids)
    return audio_features

# Function to fetch track name using track ID
def get_track_name(track_id):
    track_details = sp.track(track_id)
    return track_details['name']


# Create an empty list to store playlist data
playlist_data = []

for j, playlist in enumerate(playlist_ids):
    playlist_tracks = sp.playlist_tracks(playlist, fields='items.track.id')
    track_ids = [track['track']['id'] for track in playlist_tracks['items']]
    audio_features = get_audio_features(track_ids)

    for i, track_id in enumerate(track_ids):
        # Fetch track name using track ID
        track_name = get_track_name(track_id)

        # Get track details including artist information
        track_details = sp.track(track_id)
        artists = track_details['artists']
        
        # Create a string of artists for the track in case there are multiple artists
        artists_names = []
        for artist in artists:
            artists_names.append(artist['name'])
        artist_string = ', '.join(artists_names) # Combines all elements of artist_names list into a string separated by a ", "

        # Check if any artist for the track is Drake
        if 'Drake' in artist_string:
            playlist_data.append(
                {
                    'track_uri': track_details['uri'],
                    'track_name' : track_name,
                    'duration_ms': audio_features[i]['duration_ms'],
                    'danceability': audio_features[i]['danceability'],
                    'energy': audio_features[i]['energy'],
                    'key': audio_features[i]['key'],
                    'loudness': audio_features[i]['loudness'],
                    'speechiness': audio_features[i]['speechiness'],
                    'acousticness': audio_features[i]['acousticness'],
                    'instrumentalness': audio_features[i]['instrumentalness'],
                    'liveness': audio_features[i]['liveness'],
                    'valence': audio_features[i]['valence'],
                    'tempo': audio_features[i]['tempo'],
                    'artist' : artist_string
                }
            )

    df = pd.DataFrame(playlist_data)
    df.to_csv(f"playlist_{j + 1}.csv", index=False)
