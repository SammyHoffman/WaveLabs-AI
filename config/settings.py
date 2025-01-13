"""
config/settings.py

Central location for both general settings and Mixcloud-specific configurations.
Sensitive credentials (Mixcloud, Spotify, Last.fm, etc.) should be in .env only.
"""

import os
import json
import sys
import shutil
from dotenv import load_dotenv

# Color Codes
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_PURPLE = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_GREY = "\033[37m"

# Message Prefixes
MSG_ERROR = f"{COLOR_RED}[Error]{COLOR_RESET}: "
MSG_NOTICE = f"{COLOR_YELLOW}[Notice]{COLOR_RESET}: "
MSG_DEBUG = f"{COLOR_CYAN}[Debug]{COLOR_RESET}: "
MSG_SUCCESS = f"{COLOR_GREEN}[Success]{COLOR_RESET}: "
MSG_STATUS = f"{COLOR_GREEN}[Status]{COLOR_RESET}: "
MSG_WARNING = f"{COLOR_BLUE}[Warning]{COLOR_RESET}: "
LINE_BREAK = f"{COLOR_GREY}----------------------------------------{COLOR_RESET}"

# ----------------------------------------------------------------
#             LOAD .ENV FILE VARIABLES (IF PRESENT)
# ----------------------------------------------------------------

# Make sure .env is in your .gitignore, so secrets aren’t committed.
load_dotenv()

# ----------------------------------------------------------------
#      NON-SENSITIVE CONFIGURATIONS & PATHS
# ----------------------------------------------------------------

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CONFIG_DIR)

DJ_POOL_BASE_PATH = os.environ.get(
    "DJ_POOL_BASE_PATH",
    os.path.join(PROJECT_ROOT, "content", "download", "download_music")
)


DOWNLOAD_FOLDER_NAME = os.environ.get(
    "DOWNLOAD_FOLDER_NAME",
    os.path.expanduser("~/Downloads")
)

# ----------------------------------------------------------------
#      DOWNLOADING CONFUGURATION & PATHS
# ----------------------------------------------------------------

# Path to store downloaded music links
LINKS_FILE = os.environ.get(
    "LINKS_FILE",
    os.path.join(PROJECT_ROOT, "content", "download", "musicLinks.txt")
) # TODO: Refactor a Clearer Name

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

USER_CONFIG_DJCLI = os.path.expanduser("~/Documents/DJCLI")
PEXEL_DOWNLOAD_FOLDER = os.path.join(USER_CONFIG_DJCLI, "content", "download", "download_pexel")
PEXEL_LOG_FILE = os.path.join(USER_CONFIG_DJCLI, "content", "downloaded_pexel_photos.txt")

# ----------------------------------------------------------------
#   ALBUM COVER CONFIGURATION (JSON)
# ----------------------------------------------------------------

DEFAULT_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "default_albumCoverConfig.json"
)

USER_DOCS = os.path.expanduser("~/Documents")
USER_CONFIG_FOLDER = os.path.join(USER_DOCS, "DJCLI", "configuration")
USER_CONFIG_PATH = os.path.join(USER_CONFIG_FOLDER, "albumCoverConfig.json")

def ensure_album_cover_config():
    if not os.path.exists(USER_CONFIG_FOLDER):
        os.makedirs(USER_CONFIG_FOLDER, exist_ok=True)
    if not os.path.exists(USER_CONFIG_PATH):
        if not os.path.exists(DEFAULT_JSON_PATH):
            raise FileNotFoundError(f"Default album cover config not found at {DEFAULT_JSON_PATH}")
        shutil.copyfile(DEFAULT_JSON_PATH, USER_CONFIG_PATH)
        print(f"{MSG_NOTICE}Created user album cover config at {USER_CONFIG_PATH}. Please edit to customize album covers.")
    else:
        print(f"{MSG_STATUS}Loaded existing album cover config from: {USER_CONFIG_PATH}")
    return USER_CONFIG_PATH

ALBUM_COVER_CONFIG = {}
try:
    user_json_path = ensure_album_cover_config()
    with open(user_json_path, "r", encoding="utf-8") as f:
        ALBUM_COVER_CONFIG = json.load(f)
except Exception as e:
    print(f"{MSG_ERROR}Could not load albumCoverConfig.json: {e}")
    ALBUM_COVER_CONFIG = {}

GLOBAL_SETTINGS = ALBUM_COVER_CONFIG.get("GLOBAL_SETTINGS", {})
CONFIGURATIONS = ALBUM_COVER_CONFIG.get("CONFIGURATIONS", {})

PASTE_LOGO = GLOBAL_SETTINGS.get("PASTE_LOGO", True)
ORIGINAL_IMAGES_FOLDER = os.path.join(USER_DOCS, "DJCLI", "content", "albumCovers", "pexel")
DESTINATION_FOLDER = os.path.join(USER_DOCS, "DJCLI", "content", "albumCovers", "pexel_processed")
OUTPUT_FOLDER = os.path.join(USER_DOCS, "DJCLI", "content", "albumCovers", "albumCovers_output")

# ----------------------------------------------------------------
#   PYTHON-BASED SETTINGS CONFIGURATION (for user overrides)
# ----------------------------------------------------------------

# Set the default Python settings file (packaged with your code)
DEFAULT_PY_SETTINGS = os.path.join(CONFIG_DIR, "default_settings.py")
# Set the destination user settings file (user-writable folder)
USER_PY_SETTINGS = os.path.join(USER_CONFIG_FOLDER, "user_settings.py")

def ensure_user_py_settings():
    if not os.path.exists(USER_CONFIG_FOLDER):
        os.makedirs(USER_CONFIG_FOLDER, exist_ok=True)
    if not os.path.exists(USER_PY_SETTINGS):
        if not os.path.exists(DEFAULT_PY_SETTINGS):
            raise FileNotFoundError(f"Default Python settings not found at {DEFAULT_PY_SETTINGS}")
        shutil.copyfile(DEFAULT_PY_SETTINGS, USER_PY_SETTINGS)
        print(f"[Notice]: Copied default_settings.py to {USER_PY_SETTINGS}.")
    return USER_PY_SETTINGS

def load_user_py_settings_as_dict():
    user_file = ensure_user_py_settings()
    # if user_file:
    #     print(f"{MSG_STATUS}Found user settings from {user_file}")
    user_namespace = {}
    try:
        with open(user_file, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code, user_namespace, user_namespace)
    except Exception as e:
        print(f"{MSG_ERROR}Could not execute user_settings.py: {e}")
    return user_namespace

USER_PY_CFG = load_user_py_settings_as_dict()
# Override environment-derived variables only if not already set via .env
if not MIXCLOUD_CLIENT_ID and "MIXCLOUD_CLIENT_ID" in USER_PY_CFG:
    MIXCLOUD_CLIENT_ID = USER_PY_CFG["MIXCLOUD_CLIENT_ID"]
if not MIXCLOUD_CLIENT_SECRET and "MIXCLOUD_CLIENT_SECRET" in USER_PY_CFG:
    MIXCLOUD_CLIENT_SECRET = USER_PY_CFG["MIXCLOUD_CLIENT_SECRET"]
if not SPOTIFY_CLIENT_ID and "SPOTIFY_CLIENT_ID" in USER_PY_CFG:
    SPOTIFY_CLIENT_ID = USER_PY_CFG["SPOTIFY_CLIENT_ID"]
if not SPOTIFY_CLIENT_SECRET and "SPOTIFY_CLIENT_SECRET" in USER_PY_CFG:
    SPOTIFY_CLIENT_SECRET = USER_PY_CFG["SPOTIFY_CLIENT_SECRET"]
if not LASTFM_API_KEY and "LASTFM_API_KEY" in USER_PY_CFG:
    LASTFM_API_KEY = USER_PY_CFG["LASTFM_API_KEY"]
if not DEEZER_API_KEY and "DEEZER_API_KEY" in USER_PY_CFG:
    DEEZER_API_KEY = USER_PY_CFG["DEEZER_API_KEY"]
if not MUSICBRAINZ_API_TOKEN and "MUSICBRAINZ_API_TOKEN" in USER_PY_CFG:
    MUSICBRAINZ_API_TOKEN = USER_PY_CFG["MUSICBRAINZ_API_TOKEN"]
if not PEXEL_API_KEY and "PEXEL_API_KEY" in USER_PY_CFG:
    PEXEL_API_KEY = USER_PY_CFG["PEXEL_API_KEY"]

# ----------------------------------------------------------------
#   REMINDER: DO NOT STORE SECRETS IN THIS FILE; USE .env INSTEAD.
# ----------------------------------------------------------------
"""
All sensitive credentials (Mixcloud, Spotify, Last.fm, etc.) 
are read from .env to avoid committing secrets to source control.
Make sure your .env is in .gitignore and not pushed publicly.

Sample .env fields:

MIXCLOUD_CLIENT_ID=""
MIXCLOUD_CLIENT_SECRET=""
SPOTIFY_CLIENT_ID=""
SPOTIFY_CLIENT_SECRET=""
LASTFM_API_KEY=""
DEEZER_API_KEY=""
MUSICBRAINZ_API_TOKEN=""
PEXEL_API_KEY=""
"""