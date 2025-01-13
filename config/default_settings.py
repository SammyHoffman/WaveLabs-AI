"""
default_settings.py

This file is a fallback Python-based configuration for DJ Automation.
When first run, your application can copy this default to a user-writable
location (e.g. ~/Documents/DJCLI/configuration/user_settings.py). Users
can then fill in or modify the values here without altering the original
package.

All secrets or credentials are placeholders. For production, ensure you
store real credentials in user_settings.py or a .env file, not in version
control.
"""

import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NON-SENSITIVE PATHS & TOGGLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DJ_POOL_BASE_PATH = "content/download/download_music"
DOWNLOAD_FOLDER_NAME = os.path.expanduser("~/Downloads")
LINKS_FILE = "content/download/musicLinks.txt"

USE_COLOR_LOGS = True
DEBUG_MODE = False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MIXCLOUD + OTHER SENSITIVE CREDENTIALS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Replace "PUT_YOUR_VALUE_HERE" with real credentials or leave them
# empty if you plan to use environment variables or .env.
MIXCLOUD_CLIENT_ID     = "PUT_YOUR_VALUE_HERE"
MIXCLOUD_CLIENT_SECRET = "PUT_YOUR_VALUE_HERE"

SPOTIFY_CLIENT_ID      = "PUT_YOUR_VALUE_HERE"
SPOTIFY_CLIENT_SECRET  = "PUT_YOUR_VALUE_HERE"

LASTFM_API_KEY         = "PUT_YOUR_VALUE_HERE"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MIXCLOUD SETTINGS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MIXCLOUD_ENABLED = True
MIXCLOUD_PORT = 8001
MIXCLOUD_REDIRECT_URI = f"http://localhost:{MIXCLOUD_PORT}/"
MIXCLOUD_AUTH_URL = "https://www.mixcloud.com/oauth/authorize?client_id=PUT_YOUR_VALUE_HERE&redirect_uri=PUT_YOUR_VALUE_HERE" 
MIXCLOUD_PRO_USER = True

USE_EXTERNAL_TRACK_DIR = True
LOCAL_TRACK_DIR = "/Users/username/Documents/PythonAutomation/AutomaticSoundCloudUpload/tracks/"
EXTERNAL_TRACK_DIR = "/Volumes/DJKatazui-W/DJ Mixes"

COVER_IMAGE_DIRECTORY = "/Users/username/Documents/PythonAutomation/AutomaticSoundCloudUpload/images/"
FINISHED_DIRECTORY    = "/Users/username/Documents/PythonAutomation/AutomaticSoundCloudUpload/finished/"
PUBLISHED_DATES       = "/Users/username/Documents/PythonAutomation/AutomaticSoundCloudUpload/dates.txt"
TITLES_FILE           = "/Users/username/Documents/PythonAutomation/AutomaticSoundCloudUpload/titles.csv"
UPLOAD_LINKS_FILE     = "content/mixcloudContent/uploadLinks.txt"

MAX_UPLOADS      = 8
PUBLISHED_HOUR   = 12
PUBLISHED_MINUTE = 0

TRACK_TAGS = [
    "Open Format",
    "Disc Jockey",
    "Live Performance",
    "Katazui",
    "Archive"
]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPTIONAL: CENTRALIZED API INFO
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# If you want to unify them here, place placeholders:
APIS = {
    "spotify": {
        "enabled": True,
        "url": "https://api.spotify.com/v1/search",
        "auth_url": "https://accounts.spotify.com/api/token",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    },
    "deezer": {
        "enabled": True,
        "url": "https://api.deezer.com/search",
    },
    "lastfm": {
        "enabled": True,
        "api_key": LASTFM_API_KEY,
        "url": "http://ws.audioscrobbler.com/2.0/",
    },
    "musicbrainz": {
        "enabled": True,
        "url": "https://musicbrainz.org/ws/2/recording",
        "cover_art_url": "https://coverartarchive.org/release/",
    },
    "mixcloud": {
        "enabled": MIXCLOUD_ENABLED,
        "client_id": MIXCLOUD_CLIENT_ID,
        "client_secret": MIXCLOUD_CLIENT_SECRET,
        "auth_url": MIXCLOUD_AUTH_URL,
    },
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PEXELS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PEXEL_API_KEY = "PUT_YOUR_VALUE_HERE"
PEXEL_API_URL = "https://api.pexels.com/v1/search"

TAGS = [
    "minimalist", "simple background", "clean background", "abstract", 
    "white background", "black background", "nature", "landscape", "mountains",
    "forest", "sky", "sea", "beach", "sunset", "sunrise", "desert",
    "cityscape", "urban", "architecture", "buildings", "skyline", "street",
    "texture", "pattern", "fabric", "wood", "marble", "brick", "concrete", "metal",
    "gradient", "blurred background", "soft colors", "pastel colors", "bokeh",
    "aesthetic", "empty space"
]

"""
Feel free to add or remove any settings as needed. The user can override them
by editing this file once copied to their local config directory.
"""