# Spotibot Documentation

## Overview
Spotibot is a Python script designed to create an updated daily playlist with the latest liked podcast episodes and music. The script utilizes the Spotify API to retrieve information about the user's liked podcasts and songs, allowing them to create a dynamic playlist that combines the latest podcast episodes with random songs from their liked tracks.

## How It Works
Spotibot operates in two modes: **manual** and **auto**.

### Manual Mode
In manual mode, the user has the option to either use a fixed playlist name or provide a custom one. The script prompts the user to select podcasts from their liked shows and then generates a playlist by interleaving the latest episodes of the selected podcasts with random songs from their liked tracks.

To run Spotibot in manual mode, execute the script and choose "manual" when prompted for the mode. Follow the on-screen instructions to customize the playlist name and select podcasts.

### Auto Mode
In auto mode, Spotibot automatically updates the playlist daily at 8 AM. Similar to manual mode, the user can choose a fixed or custom playlist name. The script determines the user's country from their Spotify account, extracts the time zone, and schedules the playlist update accordingly.

To run Spotibot in auto mode, execute the script and choose "auto" when prompted for the mode. Follow the on-screen instructions to customize the playlist name and initiate the automated daily updates.

## Authentication
Spotibot uses the Spotify API for authentication. It requires environment variables for the Spotify client ID, client secret, and redirect URI. These variables should be set in a `.env` file in the same directory as the script.

## Logging
Spotibot logs successful updates and any errors that occur during the playlist update process. The log file is named `spotibot.log` and is located in the same directory as the script.

## Dependencies
Spotibot relies on the following Python libraries, which can be installed using `pip install <library>`:
- `os`
- `dotenv`
- `spotipy`
- `logging`
- `datetime`
- `schedule`
- `time`
- `pytz`
- `random`

## Usage
1. Ensure the required dependencies are installed.
2. Set up the Spotify API credentials in a `.env` file.
3. Execute the script and choose the desired mode (manual/auto).
4. Follow the on-screen instructions to customize the playlist name and select podcasts (applicable to manual mode).

Feel free to reach out if you have any questions or encounter issues with Spotibot!

---

*Proudly made with ChatGPT.*
