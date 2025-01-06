"""
core/cover_utils.py

Contains functions for:
- Checking if MP3 files have embedded covers
- Fetching album covers via external APIs (Last.fm, MusicBrainz, Deezer, Spotify)
- Downloading, cropping, and embedding album covers
"""

import os
import requests
from io import BytesIO
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_WARNING
)
from config.settings import DEBUG_MODE
# If APIS, get_spotify_token, etc. are stored in settings or a separate module, import them below:
from config.settings import APIS
# from modules.download.some_spotify_file import get_spotify_token

# ----------------------------------------------------------------
#                   HAS EMBEDDED COVER
# ----------------------------------------------------------------

def has_embedded_cover(file_path):
    """
    Checks whether the MP3 file has an embedded cover (ID3:APIC) tag.
    Returns True if cover art is present, False otherwise.
    """
    try:
        metadata = MP3(file_path, ID3=ID3)
        if metadata and metadata.tags.getall('APIC'):
            return True
    except error:
        pass
    return False

# ----------------------------------------------------------------
#                 FETCH ALBUM COVER (HIGH-LEVEL)
# ----------------------------------------------------------------

def fetch_album_cover(title, artist):
    """
    Decide which external API to query to retrieve a cover URL.
    Return the cover URL or None if nothing is found.

    Steps in your snippet:
      1) lastfm_cover(...)
      2) musicbrainz_cover(...)
      3) spotify_cover(...)
      4) deezer_cover(...)
    """
    if artist.lower() == "unknown artist" and title.lower() == "unknown title":
        return None

    # 1) Last.fm
    url = lastfm_cover(title, artist)
    if url:
        return url

    # 2) MusicBrainz
    url = musicbrainz_cover(title, artist)
    if url:
        return url

    # 3) Spotify
    url = spotify_cover(title, artist)
    if url:
        return url

    # 4) Deezer
    url = deezer_cover(title, artist)
    if url:
        return url

    return None

# ----------------------------------------------------------------
#                 LAST.FM COVER
# ----------------------------------------------------------------

def lastfm_cover(title, artist):
    """
    Fetch album art from Last.fm based on track info.
    Relies on APIS['lastfm'].
    Returns a cover image URL or None.
    """
    try:
        from config.settings import APIS  # Or your own location for APIS dict
        if not APIS["lastfm"]["enabled"]:
            return None

        params = {
            "method": "track.getInfo",
            "api_key": APIS["lastfm"]["api_key"],
            "artist": artist,
            "track": title,
            "format": "json",
        }
        r = requests.get(APIS["lastfm"]["url"], params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            # Attempt to parse out album images
            album_images = data["track"]["album"]["image"]
            if album_images:
                # The last image is often the largest
                return album_images[-1]["#text"]
    except Exception:
        return None
    return None

# ----------------------------------------------------------------
#                MUSICBRAINZ COVER
# ----------------------------------------------------------------

def musicbrainz_cover(title, artist):
    """
    Fetch album art from MusicBrainz based on track info.
    Relies on APIS['musicbrainz'].
    Returns a cover image URL or None.
    """
    try:
        from config.settings import APIS
        if not APIS["musicbrainz"]["enabled"]:
            return None

        params = {"query": f"recording:{title} AND artist:{artist}", "fmt": "json"}
        r = requests.get(APIS["musicbrainz"]["url"], params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data["recordings"] and data["recordings"][0]["releases"]:
                release_id = data["recordings"][0]["releases"][0]["id"]
                # Example: https://coverartarchive.org/release/<RELEASE_ID>/front
                return f"{APIS['musicbrainz']['cover_art_url']}{release_id}/front"
    except Exception:
        return None
    return None

# ----------------------------------------------------------------
#                   DEEZER COVER
# ----------------------------------------------------------------

def deezer_cover(title, artist):
    """
    Fetch album art from Deezer based on track info.
    Relies on APIS['deezer'].
    Returns a cover image URL or None.
    """
    try:
        from config.settings import APIS
        if not APIS["deezer"]["enabled"]:
            return None

        search_url = APIS["deezer"]["url"]
        query = f"{title} {artist}"
        r = requests.get(search_url, params={"q": query}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("data"):
                # Take the first match
                track_obj = data["data"][0]
                album_obj = track_obj.get("album", {})
                return album_obj.get("cover_big")
    except Exception:
        return None
    return None

# ----------------------------------------------------------------
#                   SPOTIFY COVER
# ----------------------------------------------------------------

def spotify_cover(title, artist):
    """
    Fetch album art from Spotify based on track info.
    Relies on APIS['spotify'] and get_spotify_token().
    Returns the first available album image URL or None.
    """
    try:
        from config.settings import APIS
        from modules.download.downloader import get_spotify_token  # or wherever you keep this function

        if not APIS["spotify"]["enabled"]:
            return None

        token = get_spotify_token()
        if not token:
            return None

        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": f"{title} {artist}", "type": "track", "limit": 1}
        search_url = APIS["spotify"]["url"]
        r = requests.get(search_url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            items = data["tracks"]["items"]
            if items:
                images = items[0]["album"]["images"]
                # The first image in the list is typically the largest or highest priority
                return images[0]["url"] if images else None
    except Exception:
        return None
    return None

# ----------------------------------------------------------------
#           DOWNLOAD + CROP + ATTACH COVER
# ----------------------------------------------------------------

def download_crop_and_attach_cover(file_path, cover_url):
    """
    Download the cover from cover_url, crop it to a square,
    then embed it into the MP3 file as an ID3 APIC frame.
    """
    try:
        r = requests.get(cover_url, timeout=10)
        if r.status_code == 200:
            image_data = r.content
            image = Image.open(BytesIO(image_data))

            cropped_image_data = crop_image_to_square(image)
            attach_cover_to_mp3(file_path, cropped_image_data)
        else:
            print(f"{MSG_ERROR}Failed to download album cover: {r.status_code}\n")
    except Exception as e:
        print(f"{MSG_ERROR}Error attaching cover to {file_path}: {e}\n")

def attach_cover_to_mp3(file_path, cover_data):
    """
    Embed the given cover_data (JPEG) into the MP3 file as an ID3 APIC frame.
    """
    try:
        audio = MP3(file_path, ID3=ID3)
        audio.tags.delall('APIC')  # remove existing covers
        audio.tags.add(APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,  # front cover
            desc="Cover",
            data=cover_data,
        ))
        audio.save()
        print(f"{MSG_SUCCESS}Album cover added to {file_path}\n")
    except Exception as e:
        print(f"{MSG_ERROR}Failed embedding cover in {file_path}: {e}\n")

# ----------------------------------------------------------------
#                 IMAGE CROPPING HELPERS
# ----------------------------------------------------------------

def crop_image_to_square(image):
    """
    Crop a PIL Image to a square based on the shorter side,
    then return the resulting image as raw JPEG bytes.
    """
    width, height = image.size
    if width == 0 or height == 0:
        print(f"{MSG_WARNING}Image has invalid size; skipping crop.")
        return image_to_jpeg_bytes(image)

    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    right = left + side
    bottom = top + side

    cropped = image.crop((left, top, right, bottom))
    return image_to_jpeg_bytes(cropped)

def image_to_jpeg_bytes(pil_image):
    """
    Convert a PIL Image to raw JPEG bytes.
    """
    if pil_image.mode not in ("RGB", "L"):
        pil_image = pil_image.convert("RGB")
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG')
    return buffer.getvalue()