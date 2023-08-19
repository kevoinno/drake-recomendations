# Currently Working On...
Testing a Euclidean-distance based recommendation system
# Drake-recs

## About this Project
This project helps users get more personalized recommendations for specifically Drake songs. To read a more detailed analysis on the creation of this recommendation system, scroll down to the Analysis section.

## Usage of streamlit app
To use the recommendation system for yourself, check out LINK:

1. Enter a Drake song that you like
2. Choose the number of songs you want recommended to you
3. Click the Get Recommendations button
4. Listen to the recommendations

## Analysis of Drake recommendation system

### Overall structure of recommendation system
The basic structure structure of the recommendation system is as follows:

![](system_flowchart.png)

The recommendation system computes the cosine simliarity of the inputted track and and all other Drake songs in the database based on features such as danceability, energy, key, loudness, speechiness, acousticness, instrumentalness, liveness, valence, and tempo. Currently, only songs made by Drake are in the database (features are not included) 

### The Data and Assumptions
The data was collected using the Spotify web API and the spotipy library. To see the code, check out data_processing.py and user_playlist_dataset.py.

The drake_songs_dataset.csv was the dataset of Drake tracks that the recommendation system would pull from to recommend based on the user's inputted track.

playlist_1.csv to playlist_5.csv were popular playlists made by users containing Drake songs that captured the moods of Sad, Hype, Chill, Romatic, and Party respectively. These different playlist datasets were used to evaluate the recommendation system's performance. 

### Testing the recommendation system

To test my recommendation system, I used an offline evaluation method. I collected data from playlists created by users that contained only Drake songs. Each playlist fit a specific mood of Drake. I would then split each playlist into training and testing datasets, to see if my model could recommend the correct songs based on the training data.

Because my recommendation system works by inputting only 1 song and generating for example 5 recommendations, to test the performance of the system on an entire playlist, the playlist will be split into train and test data. I will run the system on each song in the train data, and add the recommendations to a list. Then, I will check if those recommendations are present in the test data.

I subjectively determined that ths following moods were the primary moods present in Drake songs:
Playlists from users to test recommendation system:

- Sad: https://open.spotify.com/playlist/5lWxcrl0MTLPS6iEtzYMb6
- Hype: https://open.spotify.com/playlist/0t06SW8VdtNeluu1qSFSNg
- Chill: https://open.spotify.com/playlist/2XF1Qyb2mk2bAi7D0cvhoz
- Romantic: https://open.spotify.com/playlist/2WnlmsV0BPt6ydSYK5AoCT
- Party: https://open.spotify.com/playlist/35WYwjJedrQevOlzBNmXt5

The assumption about this data is that the songs in the playlist accurate capture the mood. I subjectively determined this by listening to a few songs in each playlist. A limitation with this project is that I only used 1 playlist per mood. The problem with this is that different people can think that the same song can convey a different mood. Sampling the most popular playlist for each mood was my "fix" to this, but in the future, I would collect more data (more playlists) per mood to get a more accurate idea of what each mood .




