"""
config/settings.py

Central location for both general settings and Mixcloud-specific configurations.
Sensitive credentials (Mixcloud, Spotify, Last.fm, etc.) should be in .env only.
"""

import os
import sys
from dotenv import load_dotenv

# ----------------------------------------------------------------
#             LOAD .ENV FILE VARIABLES (IF PRESENT)
# ----------------------------------------------------------------

# Make sure .env is in your .gitignore, so secrets aren’t committed.
load_dotenv()

# ----------------------------------------------------------------
#      NON-SENSITIVE CONFIGURATIONS & PATHS
# ----------------------------------------------------------------

DJ_POOL_BASE_PATH = os.getenv("DJ_POOL_BASE_PATH", os.path.abspath("./tests/test_download/"))
DOWNLOAD_FOLDER_NAME = os.getenv("DOWNLOAD_FOLDER_NAME", "/Users/haleakala/Downloads/")
LINKS_FILE = os.getenv("LINKS_FILE", "links.txt") # TODO: Refactor a Clearer Name

# ----------------------------------------------------------------
#          LOGGING & GENERAL TOGGLES
# ----------------------------------------------------------------

USE_COLOR_LOGS = os.getenv("USE_COLOR_LOGS", "True").strip().lower() == "true"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").strip().lower() == "true"

# ----------------------------------------------------------------
#   MIXCLOUD + OTHER SENSITIVE CREDENTIALS (FROM .ENV)
# ----------------------------------------------------------------

MIXCLOUD_CLIENT_ID = os.getenv("MIXCLOUD_CLIENT_ID", "")
MIXCLOUD_CLIENT_SECRET = os.getenv("MIXCLOUD_CLIENT_SECRET", "")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")
DEEZER_API_KEY = os.getenv("DEEZER_API_KEY", "")
MUSICBRAINZ_API_TOKEN = os.getenv("MUSICBRAINZ_API_TOKEN", "")

# ----------------------------------------------------------------
#   MIXCLOUD SETTINGS
# ----------------------------------------------------------------

# Example toggles or parameters for your Mixcloud logic:
MIXCLOUD_ENABLED = True  # If you disable it, code won’t attempt uploads
MIXCLOUD_PORT = int(os.getenv("MIXCLOUD_PORT", "8001"))
MIXCLOUD_REDIRECT_URI = f"http://localhost:{MIXCLOUD_PORT}/"
MIXCLOUD_AUTH_URL = (
    "https://www.mixcloud.com/oauth/authorize"
    f"?client_id={MIXCLOUD_CLIENT_ID}&redirect_uri={MIXCLOUD_REDIRECT_URI}"
)

# If you’re a Mixcloud Pro user, can schedule uploads
MIXCLOUD_PRO_USER = True

# Optional paths or toggles for track & cover uploads
USE_EXTERNAL_TRACK_DIR = os.getenv("USE_EXTERNAL_TRACK_DIR", "True").strip().lower() == "true"
LOCAL_TRACK_DIR = os.getenv("LOCAL_TRACK_DIR", "/Users/haleakala/Documents/PythonAutomation/AutomaticSoundCloudUpload/tracks/")
EXTERNAL_TRACK_DIR = os.getenv("EXTERNAL_TRACK_DIR", "/Volumes/DJKatazui-W/DJ Mixes")
COVER_IMAGE_DIRECTORY = os.getenv("COVER_IMAGE_DIRECTORY", "/Users/haleakala/Documents/PythonAutomation/AutomaticSoundCloudUpload/images/")
FINISHED_DIRECTORY = os.getenv("FINISHED_DIRECTORY", "/Users/haleakala/Documents/PythonAutomation/AutomaticSoundCloudUpload/finished/")
PUBLISHED_DATES = os.getenv("PUBLISHED_DATES", "/Users/haleakala/Documents/PythonAutomation/AutomaticSoundCloudUpload/dates.txt")
TITLES_FILE = os.getenv("TITLES_FILE", "/Users/haleakala/Documents/PythonAutomation/AutomaticSoundCloudUpload/titles.csv")
UPLOAD_LINKS_FILE = os.getenv("UPLOAD_LINKS_FILE", "content/mixcloudContent/uploadLinks.txt")  # Where you store uploaded URLs

# Max tracks to upload per run
MAX_UPLOADS = int(os.getenv("MAX_UPLOADS", "8"))

# Publish Time (for scheduled uploads)
PUBLISHED_HOUR = int(os.getenv("PUBLISHED_HOUR", "12"))
PUBLISHED_MINUTE = int(os.getenv("PUBLISHED_MINUTE", "00"))

# Mixcloud track tags (max 5)
TRACK_TAGS = [
    "Open Format",
    "Disc Jockey",
    "Live Performance",
    "Katazui",
    "Archive"
]

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
        "enabled": MIXCLOUD_ENABLED,
        "client_id": MIXCLOUD_CLIENT_ID,
        "client_secret": MIXCLOUD_CLIENT_SECRET,
        "auth_url": MIXCLOUD_AUTH_URL,
        # Additional endpoints or keys if needed
    },
}

# ----------------------------------------------------------------
#   PEXEL API CONFIGURATION
# ----------------------------------------------------------------

# Pexels Configuration
PEXEL_API_KEY = os.getenv('PEXEL_API_KEY', '')
PEXEL_API_URL = 'https://api.pexels.com/v1/search'

# Tags for Photo Search 
TAGS = [ # TODO: Refactor a Clearer Name
    'minimalist', 'simple background', 'clean background', 'abstract', 'white background', 'black background',
    'nature', 'landscape', 'mountains', 'forest', 'sky', 'sea', 'beach', 'sunset', 'sunrise', 'desert',
    'cityscape', 'urban', 'architecture', 'buildings', 'skyline', 'street',
    'texture', 'pattern', 'fabric', 'wood', 'marble', 'brick', 'concrete', 'metal',
    'gradient', 'blurred background', 'soft colors', 'pastel colors', 'bokeh', 'aesthetic', 'empty space'
]

# ----------------------------------------------------------------
#   REMINDER FOR STORING CREDENTIALS
# ----------------------------------------------------------------
"""
All sensitive credentials (Mixcloud, Spotify, Last.fm, etc.) 
are read from .env to avoid committing secrets to source control.
Make sure your .env is in .gitignore and never pushed publicly.

Sample .env fields:

MIXCLOUD_CLIENT_ID=""
MIXCLOUD_CLIENT_SECRET=""
SPOTIFY_CLIENT_ID=""
SPOTIFY_CLIENT_SECRET=""
LASTFM_API_KEY=""
DEEZER_API_KEY=""
MUSICBRAINZ_API_TOKEN=""
"""