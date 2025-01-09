"""
modules/download/downloader.py

Handles the logic for downloading audio from YouTube or SoundCloud
using yt_dlp. Also includes interactive or file-based link processing.
"""

import os
import yt_dlp  # Make sure yt-dlp is installed: pip install yt-dlp
from config.settings import DOWNLOAD_FOLDER_NAME, LINKS_FILE, DEBUG_MODE
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING, LINE_BREAK
)

def download_track(link, output_dir, quality="320"):
    """
    Downloads an audio track from a given link (YouTube, SoundCloud, etc.)
    using yt_dlp. Returns the path to the downloaded file or None on error.
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
                return None

            # The new file path
            downloaded_file_path = None
            if 'requested_downloads' in info_dict and info_dict['requested_downloads']:
                downloaded_file_path = info_dict['requested_downloads'][0].get('filepath')

            if downloaded_file_path and os.path.exists(downloaded_file_path):
                print(f"{MSG_SUCCESS}Downloaded file: {downloaded_file_path}")
                return downloaded_file_path, info_dict
            else:
                print(f"{MSG_ERROR}File not found after download. Possibly a postprocessing error.")
                return None, info_dict

    except Exception as e:
        if DEBUG_MODE:
            print(f"{MSG_ERROR}Exception: {str(e)}")
        else:
            print(f"{MSG_ERROR}Download failed for link: {link}")
        return None


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
    """
    if not os.path.exists(LINKS_FILE):
        print(f"{MSG_ERROR}File '{LINKS_FILE}' not found. Create it or use interactive mode.")
        return

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