# Spotibot Documentation

_Proudly made using ChatGPT_

## Introduction

Spotibot is a Python script that automates the creation and updating of a Spotify playlist with the latest episodes of selected podcasts and random songs from your liked tracks. It uses the Spotify API for authentication and playlist manipulation.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Liked Podcasts](#liked-podcasts)  <!-- Updated suggestion -->
4. [Usage](#usage)
5. [Main Components](#main-components)
6. [Scheduled Updates](#scheduled-updates)
7. [Error Handling](#error-handling)
8. [Contributing](#contributing)
9. [License](#license)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/dzxx1/spotibot.git
cd spotibot
```

### 2. Install dependencies:

Before running Spotibot, make sure to install the required dependencies. You can do this by running:

```bash
pip install -r config/requirements.txt
```

The `requirements.txt` file, located in the `config` folder, includes the following dependencies:

```plaintext
spotipy
schedule
pytz
python-decouple
```

Make sure to execute this command in your virtual environment or the environment where you plan to run Spotibot.

Now you're all set to use Spotibot!

## Configuration

Spotibot uses two configuration files: `config.ini` and `secrets.ini`. __Make sure to set up these files before running the script.__

### `config.ini`

- **Playlist Section**
  - `USE_CUSTOM_NAME`: Set to `True` if you want a custom playlist name.
  - `PLAYLIST_NAME`: The name of the playlist.

- **Mode Section**
  - `SELECTED_MODE`: Set to `Auto` for automatic updates or `Manual` for manual updates.
  - `DEBUG_MODE`: Set to `True` for debugging (optional).

- **Podcasts Section**
  - Configure the podcasts you are interested in having updated in the playlist under the `[Podcasts]` section.

### `secrets.ini`

- **Spotify Section**
  - Set your Spotify API credentials in this section.

## Get Liked Podcasts<a name="liked-podcasts"></a>

Before running the main script, it's a good idea to know the names of your liked podcasts. You can use the `getLikedPodcasts.py` script to retrieve this information. Run the following command:

```bash
python getLikedPodcasts.py
```

The script will save the names of your liked podcasts to a text file (`liked_podcasts.txt`). You can use this list to easily configure your playlist in the `config.ini`

## Usage

Run the script using the following command:

```bash
python spotiBot.py
```

Follow the prompts to set up the playlist name and other details if needed.

## Main Components

### `get_all_liked_tracks()`

- Retrieves all liked tracks with popularity information.

### `create_or_get_playlist()`

- Creates a new playlist or retrieves the existing one.

### `update_playlist()`

- Updates the playlist with the latest episodes of liked podcasts and random songs.

### `schedule_playlist_update()`

- Schedules the playlist update based on the selected mode.

### `run_schedule_loop()`

- Runs the schedule loop for automatic updates.

### `main()`

- The main function to execute the script based on the selected mode.

## Scheduled Updates

Spotibot supports both manual and automatic updates. In automatic mode, the script schedules daily updates at 8:00 AM. In debug mode, updates occur every 30 seconds.

## Error Handling

Any errors that occur during the playlist update are logged in the `spotibot.log` file.


## Contributing<a name="contributing"></a>

## License<a name="license"></a>


