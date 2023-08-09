# Import libraries
import streamlit as st
from streamlit_searchbox import st_searchbox
from recommender import make_api_call, preprocess_data, recommender
import pandas as pd
import creds
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.markdown(
    """
    <link rel="stylesheet" type="text/css" href="styles.css">
    """,
    unsafe_allow_html=True,
)

df = pd.read_csv('drake_songs_dataset.csv')
df_all_cols = df.copy()


#function that will output recommendations on the streamlit app
def streamlit_recs(user_input, n_songs, df):
    selected_features = [
        'danceability', 'energy', 'key', 'loudness',
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo'
    ]

    df_all_cols = df.copy()

    input_features = make_api_call(creds.CLIENT_ID, creds.CLIENT_SECRET, user_input)

    df = df[df['track_uri'] != input_features['uri']]
    df = df[selected_features].copy()

    user_features, dataset_features = preprocess_data(input_features, df, selected_features)

    recommended_songs = recommender(user_features, dataset_features, df_all_cols, n_songs)

    return recommended_songs

# 3 columns
col1, col2, col3 = st.columns(3)

# Centering title and image
with col2:
    st.title('Drake Recs')
    st.image('drake.webp')

# Container for description of app
description_container = st.container()    
with description_container:
    st.markdown('Are you a new Drake listener, or just want to discover more of his music? This app helps you explore more of Drake\'s songs by providing personalized recommendations based on one of his songs that you like.')

# Search function for autofill
def get_suggestions(query):
    suggestions = df[df['track_name'].str.contains(query, case=False)]['track_name'].tolist()
    return suggestions

# Container for user to enter song and choose # of songs to recommend
user_input_container = st.container()
with user_input_container:
    col1, col2 = st.columns(2)
    with col1:
        # Autocomplete searchbox for music
        user_input = st_searchbox(
            label="Search for a song: ", search_function=get_suggestions
        )
        
        # Slider to determine # of recommended songs
        n_songs = st.slider('Number of songs to recommend', min_value=1, max_value=5, value=3, step=1)

        # Button that starts the recommendation system
        rec_button = st.button('Get recommendations')

    if rec_button:
        with col2:
            song_output = streamlit_recs(user_input, n_songs, df)
            st.write('You should check out:')
            
            # Embed Spotify Web Playback SDK for each recommended track
            for i, song in song_output.iterrows():
                track_uri = song['track_uri']
                
                # Extract the track ID from the track URI
                track_id = track_uri.split(":")[-1]
                
                # Embed Spotify Web Playback SDK using HTML and JavaScript
                iframe_width = 300
                iframe_height = 80

                st.components.v1.html(
                    f"""
                    <div class="custom-iframe-container">
                        <iframe src="https://open.spotify.com/embed/track/{track_id}"
                            width="{iframe_width}" height="{iframe_height}" frameborder="0" allowtransparency="true" allow="encrypted-media">
                        </iframe>
                    </div>
                    """
                )
