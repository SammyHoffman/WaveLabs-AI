"""
modules/download/downloader.py

Handles logic for downloading audio from YouTube or SoundCloud using yt_dlp,
then updates:
- ID3 tags (artist, title, year, genre)
- Album artwork (if none present)
- File renaming ("Artist - Title.mp3" for YouTube; keep parentheses if SoundCloud)

Utilizes:
- core.file_utils (sanitize_filename, remove_unwanted_brackets)
- core.cover_utils (has_embedded_cover, fetch_album_cover, download_crop_and_attach_cover)
- core.metadata_utils (glean_year_genre, glean_artist_title, update_id3_tags, check_metadata)
"""

import os
import yt_dlp

from config.settings import DOWNLOAD_FOLDER_NAME, LINKS_FILE, DEBUG_MODE
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING, LINE_BREAK
)
from core.file_utils import sanitize_filename, remove_unwanted_brackets
from core.cover_utils import (
    has_embedded_cover,
    fetch_album_cover,
    download_crop_and_attach_cover
)
from core.metadata_utils import (
    glean_artist_title,
    glean_year_genre,
    update_id3_tags,
    check_metadata
)


def download_track(link, output_dir, quality="320"):
    """
    Downloads an audio track from a link (YouTube, SoundCloud, etc.) using yt_dlp.
    Returns (final_file_path, info_dict) or (None, info_dict).

    After download:
      1) Identify if it's SoundCloud or YouTube (or other).
      2) Gather artist/title from info_dict or ID3 (depending on source).
      3) Glean year/genre.
      4) Update ID3 tags.
      5) If missing cover, fetch + embed.
      6) Rename the file:
         - SoundCloud => "title.mp3" (keep parentheses).
         - Others     => "Artist - Title.mp3" (remove bracketed text).
      7) Print final metadata.
    """
    print(f"{MSG_STATUS}Downloading from link: {link}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)

            if not info_dict:
                print(f"{MSG_ERROR}No info returned by yt_dlp.")
                return None, None

            downloaded_file_path = None
            if 'requested_downloads' in info_dict and info_dict['requested_downloads']:
                downloaded_file_path = info_dict['requested_downloads'][0].get('filepath')

            if not downloaded_file_path or not os.path.exists(downloaded_file_path):
                print(f"{MSG_ERROR}File not found after download. Possibly a postprocessing error.")
                return None, info_dict

            print(f"{MSG_SUCCESS}Downloaded file: {downloaded_file_path}")

            # 1) Check if it's SoundCloud
            soundcloud = ("soundcloud.com" in link.lower())

            # 2) Glean or read artist/title differently for SoundCloud vs others
            if soundcloud:
                # SoundCloud logic
                artist = info_dict.get("uploader", "Unknown Artist")
                # Keep the exact title from SoundCloud
                title = info_dict.get("title", "Unknown Title")
                print(f"{MSG_DEBUG}SoundCloud link detected; using SoundCloud-specific logic.")
            else:
                # YouTube or other logic
                artist, title = glean_artist_title(downloaded_file_path, info_dict)
                # Typically remove bracket text for YouTube style
                title = remove_unwanted_brackets(title)

            # 3) glean year & genre
            year, genre = glean_year_genre(info_dict, artist, title)

            # 4) update ID3 tags
            success = update_id3_tags(downloaded_file_path, artist, title, year, genre)

            final_path = downloaded_file_path
            if success:
                # 5) if missing cover, embed
                if not has_embedded_cover(downloaded_file_path):
                    cover_url = None
                    # If SoundCloud, try the thumbnail first
                    if soundcloud:
                        cover_url = info_dict.get("thumbnail")

                    if not cover_url:
                        cover_url = fetch_album_cover(title, artist)

                    if cover_url:
                        download_crop_and_attach_cover(downloaded_file_path, cover_url)
                    else:
                        print(f"{MSG_WARNING}No album cover found.")

                # 6) rename the file
                final_path = rename_file(downloaded_file_path, artist, title, soundcloud)

                # 7) print final metadata
                check_metadata(final_path)

            return final_path, info_dict

    except Exception as e:
        if DEBUG_MODE:
            print(f"{MSG_ERROR}Exception: {str(e)}")
        else:
            print(f"{MSG_ERROR}Download failed for link: {link}")
        return None, None


def rename_file(original_path, artist, title, soundcloud=False):
    """
    For SoundCloud:
      - filename => title.mp3 (keep parentheses, do not remove bracket text).
    For others (YouTube, etc.):
      - filename => Artist - Title.mp3 (remove bracket text).
    """
    try:
        if soundcloud:
            # SoundCloud: just 'title.mp3'
            new_basename = sanitize_filename(f"{title}.mp3")
        else:
            # Non-SoundCloud: "Artist - Title.mp3"
            if not artist.strip():
                artist = "Unknown Artist"
            if not title.strip():
                title = "Unknown Title"
            new_basename = sanitize_filename(f"{artist} - {title}.mp3")

        new_path = os.path.join(os.path.dirname(original_path), new_basename)

        if new_path != original_path:
            os.rename(original_path, new_path)
            print(f"{MSG_SUCCESS}Renamed file to: {new_path}")
            return new_path
        return original_path

    except Exception as e:
        print(f"{MSG_ERROR}Could not rename file: {e}")
        return original_path


def process_links_interactively():
    """
    Asks user for links in a loop and downloads them. Type 'q' to quit.
    """
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        os.makedirs(DOWNLOAD_FOLDER_NAME)
        print(f"{MSG_NOTICE}Created download folder: {DOWNLOAD_FOLDER_NAME}")

    while True:
        link = input("Enter YouTube/SoundCloud link (or 'q' to quit): ").strip()
        if link.lower() in ("q", "quit", "exit"):
            print(f"{MSG_NOTICE}Exiting interactive link mode.\n")
            break
        if not link:
            print(f"{MSG_WARNING}No link provided. Try again.\n")
            continue

        download_track(link, DOWNLOAD_FOLDER_NAME)


def process_links_from_file():
    """
    Reads a list of links from LINKS_FILE (default: links.txt) and downloads them.
    If the file doesn't exist, it will be created, and the user is prompted
    to add links or switch to interactive mode.
    """
    # Make sure the directory for LINKS_FILE exists
    dir_path = os.path.dirname(LINKS_FILE)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    # Create file if missing
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "w", encoding="utf-8"):
            pass
        print(f"{MSG_WARNING}File '{LINKS_FILE}' not found, so a new file has been created.")
        print(f"{MSG_WARNING}Please edit '{LINKS_FILE}' to add your links or return to interactive mode.")
        return

    # Collect links
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    if not links:
        print(f"{MSG_WARNING}No links found in '{LINKS_FILE}'.")
        return

    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        os.makedirs(DOWNLOAD_FOLDER_NAME)
        print(f"{MSG_NOTICE}Created download folder: {DOWNLOAD_FOLDER_NAME}")

    print(f"{MSG_STATUS}Processing {len(links)} links from file '{LINKS_FILE}'\n{LINE_BREAK}")

    for link in links:
        download_track(link, DOWNLOAD_FOLDER_NAME)

    print(f"{MSG_NOTICE}All downloads completed from {LINKS_FILE}")


def main():
    """
    Example main function to run either interactive or file-based mode.
    """
    print(f"{MSG_NOTICE}Download options:")
    print("  1) Interactive mode (enter links manually)")
    print("  2) File-based mode (links.txt)")
    choice = input("Choose (1 or 2): ").strip()
    if choice == "1":
        process_links_interactively()
    else:
        process_links_from_file()


if __name__ == "__main__":
    main()