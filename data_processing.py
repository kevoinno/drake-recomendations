import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import creds  # Import your credentials from a separate file

# Helper function that checks if Drake is an artist for the track. Return bool
def is_drake_song(track):
    for artist in track['artists']:
        if artist['name'] == 'Drake':
            return True
    return False


# Initialize the Spotify API client with client credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.CLIENT_ID, client_secret=creds.CLIENT_SECRET))

# Initialize a list to store the collected tracks
all_tracks = []

# Set the desired limit for each API call
limit = 50

# Initialize the offset to 0
offset = 0

# Continue making API calls until you have collected all the desired tracks
while True:
    # Make the API request with the current offset
    results = sp.search(q='Drake', type='track', limit=limit, offset=offset)

    # Check if there are any tracks in the results
    if not results['tracks']['items']:
        break

    # Add the retrieved tracks to the list
    all_tracks.extend(results['tracks']['items'])

    # Increment the offset by the limit to retrieve the next batch of tracks
    offset += limit

    # Check if you've reached the end of available tracks
    if offset >= results['tracks']['total']:
        break

# Extract relevant information from the collected tracks
drake_tracks = []

for track in all_tracks:
    if is_drake_song(track):
        drake_tracks.append({
            'track_uri': track['uri'],
            'track_name': track['name'],
            'album_name': track['album']['name'],
            'duration_ms': track['duration_ms'],
            'danceability': None,  # Placeholder for audio features (to be fetched later)
            'energy': None,
            'key': None,
            'loudness': None,
            'speechiness': None,
            'acousticness': None,
            'instrumentalness': None,
            'liveness': None,
            'valence': None,
            'tempo': None,
        })

# Fill in audio features for each track
for i, track in enumerate(drake_tracks):
    audio_features = sp.audio_features(track['track_uri'])[0]  # Fetch audio features for the track
    drake_tracks[i].update(audio_features)  # Update the track's dictionary with the retrieved audio features

# Assemble the data into a DataFrame
df = pd.DataFrame(drake_tracks)
df = df.drop_duplicates()

# Export the DataFrame to a CSV file
df.to_csv('drake_songs_dataset.csv', index=False)
