#Import libraries
import streamlit as st
from streamlit_searchbox import st_searchbox
from recommender import make_api_call
from recommender import preprocess_data
from recommender import recommender
import pandas as pd
import creds

df = pd.read_csv('tracks_features.csv')
df = df[:200].copy()
df = df.dropna(axis = 0, how = 'any')
df_all_cols = df[:200]

#function that will output recommendations on the streamlit app
def streamlit_recs(user_input, n_songs, df):

    selected_features = [
        'danceability', 'energy', 'key', 'loudness',
        'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo'
    ]

    df_all_cols = df.copy()
    df = df[selected_features].copy()

    input_features = make_api_call(creds.CLIENT_ID, creds.CLIENT_SECRET, user_input)

    user_features, dataset_features = preprocess_data(input_features, df, selected_features)

    recommended_songs = recommender(user_features, dataset_features, df_all_cols, n_songs)

    return recommended_songs


#3 columns
col1, col2, col3 = st.columns(3)

#Centering title and image
with col2:
    st.title('Drake Recs')
    st.image('drake.webp')

#Container for description of app
description_container = st.container()    
with description_container:
    st.markdown('Are you a new Drake , or just want to discover more his music? This app helps you explore more of Drake\'s songs by providing personalized recommendations based on one of his songs that you like.')

#Search function for autofill
def get_suggestions(query):
    suggestions = df[df['name'].str.contains(query, case=False)]['name'].tolist()
    return suggestions

#Container for user to enter song and choose # of songs to recommend
user_input_container = st.container()
with user_input_container:
    col1, col2 = st.columns(2)
    with col1:
        #autocomplete searchbox for music
        user_input = st_searchbox(
            label = "Search for a song: ", search_function = get_suggestions
        )
        
        #slider to determine # of recommended songs
        n_songs = st.slider('Number of songs to recommend', min_value=1, max_value=5, value = 3, step = 1)

        #button that starts the recommendation system
        rec_button = st.button('Get recommendations')

    if rec_button:
        with col2:
            song_output = streamlit_recs(user_input, n_songs, df)
            st.write('You should check out:')
            for i, song in enumerate(song_output):
                st.write(f"{i+1}. {song}")

        