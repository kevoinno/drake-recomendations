import time
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file

# Initialize the Spotify API client with client credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

# Step 1: Search for all of Drake's albums
results = sp.search(q='Drake', type='album', limit=50)  # Limit the search to 50 albums
albums = results['albums']['items']

print('Finished searching')
# Step 2 & 3: Fetch the tracks from each album and the audio features for each track
drake_tracks = []
for album in albums:
    album_id = album['id']
    album_name = album['name']

    tracks = sp.album_tracks(album_id)['items']
    for track in tracks:
        track_id = track['id']
        track_name = track['name']

        # Make API call for audio features and handle rate limiting
        audio_features = None
        while audio_features is None:
            try:
                audio_features = sp.audio_features(track_id)[0]
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    print("Rate limited. Waiting for 10 seconds before retrying...")
                    time.sleep(10)
                else:
                    raise

        drake_tracks.append({
            'track_uri': track['uri'],
            'track_name': track_name,
            'album_name': album_name,
            'duration_ms': track['duration_ms'],
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo'],
        })

# Step 7: Assemble the data into a DataFrame
df = pd.DataFrame(drake_tracks)

# Export the DataFrame to a CSV file
df.to_csv('drake_songs_dataset.csv', index=False)
