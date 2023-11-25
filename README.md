
# Spotibot Documentation

_Prouly made using ChatGPT_

## Introduction

Spotibot is a Python script that automates the creation and updating of a Spotify playlist with the latest episodes of selected podcasts and random songs from your liked tracks. It uses the Spotify API for authentication and playlist manipulation.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [Main Components](#main-components)
5. [Scheduled Updates](#scheduled-updates)
6. [Error Handling](#error-handling)
7. [Liked Podcasts](#liked-podcasts)
8. [Requirements](#requirements)
9. [Contributing](#contributing)
10. [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dzxx1/spotibot.git
   cd spotibot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Spotibot uses two configuration files: `config.ini` and `secrets.ini`. Make sure to set up these files before running the script.

### `config.ini`

- **Playlist Section**
  - `USE_CUSTOM_NAME`: Set to `True` if you want a custom playlist name.
  - `PLAYLIST_NAME`: The name of the playlist.

- **Mode Section**
  - `SELECTED_MODE`: Set to `Auto` for automatic updates or `Manual` for manual updates.
  - `DEBUG_MODE`: Set to `True` for debugging (optional).

- **Podcasts Section**
  - Configure the podcasts you are interested in under the `[Podcasts]` section.

### `secrets.ini`

- **Spotify Section**
  - Set your Spotify API credentials in this section.

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

## Liked Podcasts<a name="liked-podcasts"></a>

Use the `liked_podcasts.py` script to retrieve your liked podcasts. Run the following command:

```bash
python liked_podcasts.py
```

The script will save liked podcasts to a text file (`liked_podcasts.txt`). You can use this list to select podcasts for the playlist configuration.

## Requirements<a name="requirements"></a>

Spotibot requires the following dependencies:

- [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/)
- [python-decouple](https://pypi.org/project/python-decouple/)
- [schedule](https://schedule.readthedocs.io/en/stable/)

Make sure to install these dependencies before running the script.

## Contributing<a name="contributing"></a>


## License<a name="license"></a>

