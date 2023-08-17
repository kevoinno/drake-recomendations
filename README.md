# Currently Working On
Testing recommendation system

# Drake-recs

## About this Project
This project helps users get more personalized recommendations for specifically Drake songs. To read a more detailed analysis on the creation of this recommendation system, scroll down.

## Usage of streamlit app
To use the recommendation for yourself, check out:

1. Enter a Drake song that you like
2. Choose the number of songs you want recommended to you
3. Click the Get Recommendations button
4. Listen to the recommendations

## Analysis of Drake recommendation system


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

The assumption about this data is that the songs in the playlist accurate capture the mood. I subjectively determined this by listening to a few songs in each playlist. A limitation with this project is that I only used 1 playlist per mood. The problem with this is that different people can think that the same song can convey a different mood. Sampling the most popular playlist for each mood was my "fix" to this, but in the future, I would collect more data (more playlists) per mood.




