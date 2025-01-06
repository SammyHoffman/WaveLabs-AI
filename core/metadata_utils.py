"""
core/metadata_utils.py

Functions for:
- Gleaning artist/title/year/genre from local ID3 tags or external info dicts
- Checking metadata in final MP3s
- Fetching genre from APIs (Last.fm, Deezer, Spotify, MusicBrainz)
"""

import re
import requests
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, error, TIT2, TPE1, TDRC, TCON
from config.settings import DEBUG_MODE
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING
)
from core.file_utils import remove_unwanted_brackets, log_debug_info

# If you keep an APIS dict or similar in settings.py, import it here:
from config.settings import APIS

######################
# ARTIST/TITLE GLEANING
######################

def parse_title_for_artist_track(youtube_title: str) -> tuple:
    """
    If the YouTube title is in the form 'Artist - Track', split it.
    Otherwise return ('', '').
    """
    if " - " in youtube_title:
        parts = youtube_title.split(" - ", 1)
        guess_artist = parts[0].strip()
        guess_track  = parts[1].strip()
        return guess_artist, guess_track
    return "", ""


def glean_artist_title(file_path: str, info_dict: dict) -> tuple:
    """
    1) Check existing MP3 tags for artist/title
    2) If unknown, parse info_dict
    3) Remove bracketed text that doesn't contain 'feat' or 'featuring'
    4) Return (artist, title)
    """
    metadata = mutagen.File(file_path, easy=True)
    if metadata:
        id3_title  = metadata.get('title', [""])[0]  or ""
        id3_artist = metadata.get('artist', [""])[0] or ""
    else:
        id3_title, id3_artist = "", ""

    # If ID3 title is empty or "Unknown Title," glean from info_dict
    if not id3_title.strip() or id3_title.strip().lower() == "unknown title":
        possible_title = info_dict.get("title") or ""
        guess_artist, guess_track = parse_title_for_artist_track(possible_title)

        final_title = guess_track if guess_track else possible_title
        if not final_title.strip():
            final_title = "Unknown Title"

        possible_artist = info_dict.get("artist") or info_dict.get("creator") or ""
        if not possible_artist.strip():
            possible_artist = info_dict.get("uploader") or ""

        final_artist = guess_artist if guess_artist else possible_artist
        if not final_artist.strip():
            final_artist = "Unknown Artist"

        # Clean bracketed text from final
        final_title  = remove_unwanted_brackets(final_title)
        final_artist = remove_unwanted_brackets(final_artist)

        return final_artist.strip(), final_title.strip()

    else:
        # We do have ID3
        final_artist = remove_unwanted_brackets(id3_artist) or "Unknown Artist"
        final_title  = remove_unwanted_brackets(id3_title)  or "Unknown Title"
        return final_artist.strip(), final_title.strip()


##################
# YEAR/GENRE LOGIC
##################

def glean_year_genre(info_dict: dict, artist: str, title: str) -> tuple:
    """
    Attempt to glean year from the upload_date if available.
    Attempt to glean genre from info_dict or external APIs.
    """
    # Attempt to glean year from 'upload_date'
    raw_year = "Unknown Year"
    upload_date = info_dict.get("upload_date", "")
    if len(upload_date) >= 4:
        raw_year = upload_date[:4]

    # Attempt to glean genre from info_dict
    raw_genre = info_dict.get("genre", "")
    if not raw_genre.strip():
        raw_genre = "Unknown Genre"

    # If still unknown => fallback to external calls
    if raw_genre.lower() == "unknown genre":
        # Example usage if you store logic externally:
        # possible_genre = fetch_genre(artist, title)
        # if possible_genre:
        #     raw_genre = possible_genre
        pass

    return raw_year, raw_genre


def fetch_genre(artist: str, title: str) -> str:
    """
    Example placeholder for genre fetching. You'd do something like:
    1) Try lastfm_genre(...)
    2) Try deezer_genre(...)
    3) Try spotify_genre(...)
    Return the first real match or None.
    """
    # if artist.lower() == "unknown artist" or title.lower() == "unknown title":
    #     return None

    # ... Logic to call your external APIs.
    return None


###############################
# ID3/Metadata Checking/Updating
###############################

def update_id3_tags(file_path: str, artist: str, title: str, year: str, genre: str) -> bool:
    """
    Update the ID3 tags (artist, title, year, genre).
    Returns True if successful, False otherwise.
    """
    try:
        audio = MP3(file_path, ID3=ID3)

        # Title & Artist
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TPE1"] = TPE1(encoding=3, text=artist)

        # Year & Genre
        if not year.strip():
            year = "Unknown Year"
        if not genre.strip():
            genre = "Unknown Genre"

        audio["TDRC"] = TDRC(encoding=3, text=year)
        audio["TCON"] = TCON(encoding=3, text=genre)

        audio.save(v2_version=3)
        return True
    except Exception as e:
        print(f"{MSG_ERROR}Could not update ID3 for {file_path}: {str(e)}")
        return False


def check_metadata(file_path: str) -> None:
    """
    Print final ID3 tags: Title, Artist, Year, Genre, 
    and note if cover art is present.
    """
    try:
        audio = MP3(file_path, ID3=ID3)

        title_tag  = audio.get("TIT2", "No Title")
        artist_tag = audio.get("TPE1", "No Artist")
        year_tag   = audio.get("TDRC", "No Year")
        genre_tag  = audio.get("TCON", "No Genre")

        title  = title_tag.text  if hasattr(title_tag,  'text') else str(title_tag)
        artist = artist_tag.text if hasattr(artist_tag, 'text') else str(artist_tag)
        year   = year_tag.text   if hasattr(year_tag,   'text') else str(year_tag)
        genre  = genre_tag.text  if hasattr(genre_tag,  'text') else str(genre_tag)

        has_art = bool(audio.tags.getall("APIC"))

        print(f"{MSG_NOTICE}Title:      {title}")
        print(f"{MSG_NOTICE}Artist:     {artist}")
        print(f"{MSG_NOTICE}Year:       {year}")
        print(f"{MSG_NOTICE}Genre:      {genre}")
        print(f"{MSG_NOTICE}Cover Art:  {'Present' if has_art else 'None'}")

    except Exception as e:
        print(f"{MSG_ERROR}Error reading metadata from {file_path}: {e}")