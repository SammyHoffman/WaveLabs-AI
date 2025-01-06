"""
config/settings.py

Central location for configuration and environment variables.
If you have a .env file, this will load variables from there.
"""

import os
from dotenv import load_dotenv

# Load .env file variables (if present)
load_dotenv()

# Base path for where your DJ Pool or music library is stored
DJ_POOL_BASE_PATH = os.getenv("DJ_POOL_BASE_PATH", "/Users/haleakala/Music/Local DJ Pool/DJ Pool")

# Directory containing the initial downloaded files (before organization)
DOWNLOAD_FOLDER_NAME = os.getenv("DOWNLOAD_FOLDER_NAME", "audio_320")

# File that holds links for the batch download
LINKS_FILE = os.getenv("LINKS_FILE", "links.txt")

# Example API credentials (replace with your actual keys or store them in .env)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# Additional configuration toggles
USE_COLOR_LOGS = True   # Set to False if you want plain text logs without color
DEBUG_MODE = True      # If True, shows more verbose logging info