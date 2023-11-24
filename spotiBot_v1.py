import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from datetime import datetime, timedelta
import schedule
import time
import pytz
import random

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(filename='spotibot.log', level=logging.INFO)

# Set up authentication with the specified scopes and a temporary redirect URI
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
scopes = ["user-read-private", "user-read-email", "playlist-modify-public", "user-library-read"]
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope=scopes, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to get custom playlist name from the user
def get_custom_playlist_name():
    return input("Enter a custom playlist name: ")

# Function to update the playlist with the latest episodes of liked podcasts
def update_playlist():
    try:
        # Retrieve liked podcasts and print their names
        liked_podcasts = sp.current_user_saved_shows()
        print("Liked Podcasts:")
        for i, podcast in enumerate(liked_podcasts['items']):
            print(f"{i + 1}. {podcast['show']['name']}")

        # Prompt user to select podcasts
        selected_podcasts = input("Enter the numbers of the podcasts you want to include (comma-separated): ")
        selected_podcast_indices = [int(index) - 1 for index in selected_podcasts.split(',') if index.isdigit()]

        # Get the selected podcasts
        selected_podcasts = [liked_podcasts['items'][index] for index in selected_podcast_indices]

        # Get the latest episode of each selected podcast
        episode_uris = []
        for podcast in selected_podcasts:
            podcast_id = podcast['show']['id']
            episodes = sp.show_episodes(podcast_id, limit=1, offset=0)
            if episodes['items']:
                # Sort episodes by release date in descending order
                sorted_episodes = sorted(episodes['items'], key=lambda x: x['release_date'], reverse=True)
                episode_uris.append(sorted_episodes[0]['uri'])

        # Get random songs from liked songs
        liked_songs = sp.current_user_saved_tracks()
        random_song_uris = random.sample([song['track']['uri'] for song in liked_songs['items']], k=len(selected_podcasts) * 2)

        # Interleave episode URIs with random song URIs
        interleaved_uris = [uri for pair in zip(episode_uris, random_song_uris) for uri in pair]

        # Create a new playlist or get the existing one
        playlists = sp.user_playlists(sp.me()['id'])
        playlist = next((pl for pl in playlists['items'] if pl['name'] == playlist_name), None)

        if not playlist:
            playlist_description = 'A playlist containing selected podcasts and random songs'
            playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, description=playlist_description)

        # Update the playlist with the interleaved URIs
        sp.playlist_replace_items(playlist['id'], items=interleaved_uris)

        print(f"\nPlaylist '{playlist_name}' updated successfully with the latest episodes and random songs from selected podcasts!")

        # Log the successful update
        logging.info(f"Playlist '{playlist_name}' updated successfully at {datetime.now()}")

    except Exception as e:
        # Log any errors that occur during the update
        logging.error(f"Error during playlist update: {str(e)}")

# Ask the user whether to run in manual or auto mode
mode = input("Choose a mode (manual/auto): ").lower()

# Set a fixed playlist name or get a custom one from the user
if mode == "manual":
    use_custom_name = input("Do you want to use a custom playlist name? (yes/no): ").lower()
    if use_custom_name == "yes":
        playlist_name = get_custom_playlist_name()
    else:
        playlist_name = "Podcasts & Songs Daily Mix"
    update_playlist()  # Run the update immediately in manual mode
elif mode == "auto":
    use_custom_name = input("Do you want to use a custom playlist name? (yes/no): ").lower()
    if use_custom_name == "yes":
        playlist_name = get_custom_playlist_name()
    else:
        playlist_name = "Podcasts & Songs Daily Mix"

    # Run the initial update before entering the scheduling loop
    update_playlist()

    # Get the user's country from Spotify
    user_info = sp.current_user()
    country_code = user_info['country']

    # Get the time zone from the country code
    time_zone = pytz.country_timezones.get(country_code, 'UTC')[0]

    # Schedule the playlist update to occur daily at 8 AM
    schedule.every().day.at("08:00").do(update_playlist).tag('update_playlist')

    # Run the schedule loop
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    print("Invalid mode. Please choose either 'manual' or 'auto'.")
