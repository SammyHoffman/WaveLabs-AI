"""
config/settings.py

Central location for non-sensitive configuration and environment variables.
Sensitive credentials (Mixcloud, Spotify, Last.fm, etc.) belong in .env only.
"""

import os
import sys
from dotenv import load_dotenv

# ----------------------------------------------------------------
#             LOAD .ENV FILE VARIABLES (IF PRESENT)
# ----------------------------------------------------------------

# This makes any environment variables in .env accessible via os.getenv(...)
# Make sure .env is in your .gitignore so secrets aren't committed.
load_dotenv()

# For clarity, print out the current path if debugging:
# print("Settings loaded from:", __file__)
# print("Python version:", sys.version)


# ----------------------------------------------------------------
#      NON-SENSITIVE CONFIGURATIONS & PATHS
# ----------------------------------------------------------------

# Base path for where your DJ Pool or music library is stored.
# Default points to a relative path for testing; override via DJ_POOL_BASE_PATH in .env.
DJ_POOL_BASE_PATH = os.getenv("DJ_POOL_BASE_PATH", os.path.abspath("./tests/test_download/"))

# Directory containing the initial downloaded files (before organization).
DOWNLOAD_FOLDER_NAME = os.getenv("DOWNLOAD_FOLDER_NAME", "audio_320")

# File that holds links for the batch download.
LINKS_FILE = os.getenv("LINKS_FILE", "links.txt")


# ----------------------------------------------------------------
#          LOGGING & GENERAL TOGGLES
# ----------------------------------------------------------------

# If True, terminal output uses ANSI color codes (use False for plain text).
USE_COLOR_LOGS = os.getenv("USE_COLOR_LOGS", "True").strip().lower() == "true"

# If True, shows more verbose logging info for debugging.
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").strip().lower() == "true"


# ----------------------------------------------------------------
#       SENSITIVE CREDENTIALS LOADED FROM .ENV
# ----------------------------------------------------------------

# Mixcloud (example)
MIXCLOUD_CLIENT_ID = os.getenv("MIXCLOUD_CLIENT_ID", "")
MIXCLOUD_CLIENT_SECRET = os.getenv("MIXCLOUD_CLIENT_SECRET", "")

# Spotify
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# Last.fm
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")

# Deezer
DEEZER_API_KEY = os.getenv("DEEZER_API_KEY", "")

# MusicBrainz
MUSICBRAINZ_API_TOKEN = os.getenv("MUSICBRAINZ_API_TOKEN", "")


# ----------------------------------------------------------------
#   OPTIONAL: APIS DICTIONARY FOR CENTRALIZED API ENDPOINTS
# ----------------------------------------------------------------

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
        "api_key": DEEZER_API_KEY,
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
        "api_token": MUSICBRAINZ_API_TOKEN,
    },
    "mixcloud": {
        "enabled": True,
        "client_id": MIXCLOUD_CLIENT_ID,
        "client_secret": MIXCLOUD_CLIENT_SECRET,
        # ... any additional Mixcloud endpoints if needed
    },
}

# For any other APIs (e.g., YouTube, SoundCloud), you can add entries here:
# APIS["youtube"] = {...}
# APIS["soundcloud"] = {...}


# ----------------------------------------------------------------
#   ADVISORY ABOUT STORING API CREDENTIALS IN .ENV ONLY
# ----------------------------------------------------------------
"""
All sensitive credentials (e.g. MIXCLOUD_CLIENT_ID, SPOTIFY_CLIENT_ID, LASTFM_API_KEY, etc.)
are retrieved exclusively from .env to avoid exposing them in source control.

Ensure .env is NOT committed to GitHub or any public repository.

Examples in your .env:

    MIXCLOUD_CLIENT_ID=""
    MIXCLOUD_CLIENT_SECRET=""

    SPOTIFY_CLIENT_ID=""
    SPOTIFY_CLIENT_SECRET=""

    LASTFM_API_KEY=""
    DEEZER_API_KEY=""
    MUSICBRAINZ_API_TOKEN=""
"""