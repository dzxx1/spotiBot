import os
import time
import random
import logging
import schedule
from datetime import datetime, timedelta
import pytz
import configparser
from decouple import config
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Constants
CONFIG_FILE = 'config/config.ini'
SECRETS_FILE = 'config/secrets.ini'
LOG_FILE = 'logs/spotibot.log'
PLAYLIST_SCOPE = ["user-read-private", "user-read-email", "playlist-modify-public", "user-library-read"]

# Configuration
config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_FILE)

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.NOTSET, filemode='w')

USE_CUSTOM_NAME = config_parser['Playlist']['USE_CUSTOM_NAME']
PLAYLIST_NAME = config_parser['Playlist']['PLAYLIST_NAME']
SELECTED_MODE = config_parser['Mode']['SELECTED_MODE']
DEBUG_MODE = config_parser['Mode'].get('DEBUG_MODE', fallback=False)  # Read boolean value with fallback to False
if isinstance(DEBUG_MODE, str):
    DEBUG_MODE = DEBUG_MODE.lower() == 'true'
PODCAST_NAMES = {f'Podcast{i + 1}': value for i, (_, value) in enumerate(config_parser['Podcasts'].items())}

# Load sensitive information from secrets.ini
secrets_parser = configparser.ConfigParser()
secrets_parser.read(SECRETS_FILE)

SPOTIPY_CLIENT_ID = secrets_parser['Spotify']['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = secrets_parser['Spotify']['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = secrets_parser['Spotify']['SPOTIPY_REDIRECT_URI']

# ... (Other configurations)

# Execution
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, scope=PLAYLIST_SCOPE, redirect_uri=SPOTIPY_REDIRECT_URI)
sp = Spotify(auth_manager=auth_manager)


# ... (Other setup)

def get_all_liked_tracks():
    """Retrieve all liked tracks with popularity information."""
    liked_tracks = sp.current_user_saved_tracks()['items']
    return [{'uri': track['track']['uri'], 'popularity': track['track']['popularity']} for track in liked_tracks if 'popularity' in track['track']]

def create_or_get_playlist():
    """Create a new playlist or get the existing one."""
    playlists = sp.user_playlists(sp.me()['id'])
    playlist = next((pl for pl in playlists['items'] if pl['name'] == PLAYLIST_NAME), None)

    if not playlist:
        playlist_description = 'A playlist containing selected podcasts and random songs'
        playlist = sp.user_playlist_create(user=sp.me()['id'], name=PLAYLIST_NAME, description=playlist_description)

    return playlist

def update_playlist():
    """Update the playlist with the latest episodes of liked podcasts."""
    try:
        # Retrieve liked podcasts and print their names
        liked_podcasts = sp.current_user_saved_shows()
        print("Liked Podcasts:")

        # Create a dictionary with podcast indices and names
        podcast_dict = {i + 1: value for i, (_, value) in enumerate(config_parser['Podcasts'].items())}

        for i, podcast in podcast_dict.items():
            print(f"{i}. {podcast}")

        # Use the podcasts specified in the config directly
        selected_podcasts = list(PODCAST_NAMES.values())

        # Get the latest episode of each selected podcast
        episode_uris = []
        for podcast in selected_podcasts:
            podcast_id = sp.search(q=podcast, type='show')['shows']['items'][0]['id']
            episodes = sp.show_episodes(podcast_id, limit=1, offset=0)
            if episodes['items']:
                # Sort episodes by release date in descending order
                sorted_episodes = sorted(episodes['items'], key=lambda x: x['release_date'], reverse=True)
                episode_uris.append(sorted_episodes[0]['uri'])

        # Get all liked songs with popularity information
        all_liked_songs = get_all_liked_tracks()

        # Shuffle the list of liked songs
        random.shuffle(all_liked_songs)

        # Take a subset of liked songs equal to twice the length of selected_podcasts
        random_song_uris = [song['uri'] for song in all_liked_songs[:len(selected_podcasts) * 2]]

        # Interleave episode URIs with random song URIs
        interleaved_uris = [uri for pair in zip(episode_uris, random_song_uris) for uri in pair]

        # Initialize a set to keep track of added songs
        added_songs = set()

        # Loop through interleaved URIs and filter out duplicates
        filtered_uris = []
        for uri in interleaved_uris:
            if uri not in added_songs:
                filtered_uris.append(uri)
                added_songs.add(uri)

        # Create a new playlist or get the existing one
        playlist = create_or_get_playlist()

        # Update the playlist with the filtered URIs
        sp.playlist_replace_items(playlist['id'], items=filtered_uris)

        print(f"\nPlaylist '{PLAYLIST_NAME}' updated successfully with the latest episodes and random songs from selected podcasts!")

        # Log the successful update
        logging.info(f"Playlist '{PLAYLIST_NAME}' updated successfully at {datetime.now()}")

    except Exception as e:
        # Log any errors that occur during the update
        logging.error(f"Error during playlist update: {str(e)}")

def schedule_playlist_update():
    """Schedule the playlist update."""
    if DEBUG_MODE:
        schedule.every(30).seconds.do(update_playlist).tag('update_playlist')
    else:
        schedule.every().day.at("08:00").do(update_playlist).tag('update_playlist')

def run_schedule_loop():
    """Run the schedule loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """Main function to execute the script based on the selected mode."""
    print(f"SELECTED_MODE: {SELECTED_MODE}")
    mode = SELECTED_MODE.lower()

    if mode == "manual":
        use_custom_name = USE_CUSTOM_NAME.lower()
        if use_custom_name == "yes":
            playlist_name = input("Enter a custom playlist name: ")
        else:
            playlist_name = PLAYLIST_NAME
        update_playlist()  # Run the update immediately in manual mode
    elif mode == "auto":
        use_custom_name = USE_CUSTOM_NAME.lower()
        if use_custom_name == "yes":
            playlist_name = input("Enter a custom playlist name: ")
        else:
            playlist_name = PLAYLIST_NAME

        # Run the initial update before entering the scheduling loop
        update_playlist()

        # Get the user's country from Spotify
        user_info = sp.current_user()
        country_code = user_info['country']

        # Get the time zone from the country code
        time_zone = pytz.country_timezones.get(country_code, 'UTC')[0]

        # Schedule the playlist update
        schedule_playlist_update()

        # Run the schedule loop
        run_schedule_loop()
    else:
        print("Invalid mode. Please choose either 'auto' or 'manual'.")

if __name__ == "__main__":
    main()
