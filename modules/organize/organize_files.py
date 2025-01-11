"""
modules/organize/organize_files.py

Provides functions to organize or move downloaded files into
date-based folders, as well as other post-download tasks:
- Renaming
- Metadata gleaning/embedding
- Folder creation
"""

import os
import shutil
import datetime
from config.settings import DJ_POOL_BASE_PATH, DOWNLOAD_FOLDER_NAME
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING, LINE_BREAK
)

def move_to_date_based_folder(file_path):
    """
    Moves a file from the download folder to a date-based folder structure.
    Example: DJ_POOL_BASE_PATH/YYYY/YYYY-MM/YYYY-MM-DD/file.mp3
    Returns the new file path or None if move fails.
    """
    now = datetime.datetime.now()
    year_str  = now.strftime("%Y")
    month_str = now.strftime("%Y-%m")
    day_str   = now.strftime("%Y-%m-%d")

    final_folder = os.path.join(
        DJ_POOL_BASE_PATH,
        year_str,
        month_str,
        day_str,
    )
    try:
        if not os.path.exists(final_folder):
            os.makedirs(final_folder)

        destination_path = os.path.join(final_folder, os.path.basename(file_path))
        shutil.move(file_path, destination_path)
        print(f"{MSG_SUCCESS}Moved: {file_path} => {destination_path}")
        return destination_path
    except Exception as e:
        print(f"{MSG_ERROR}Could not move file: {file_path}")
        print(f"{MSG_ERROR}{str(e)}")
        return None
    
def move_to_date_based_folder_requested_songs(file_path):
    """
    Moves a file from the download folder to a date-based folder structure.
    Example: DJ_POOL_BASE_PATH/Requested Songs/YYYY/YYYY-MM/YYYY-MM-DD/file.mp3
    Returns the new file path or None if move fails.
    """
    now = datetime.datetime.now()
    year_str  = now.strftime("%Y")
    month_str = now.strftime("%Y-%m")
    day_str   = now.strftime("%Y-%m-%d")

    final_folder = os.path.join(
        DJ_POOL_BASE_PATH,
        "Requested Songs",
        year_str,
        month_str,
        day_str,
    )
    try:
        if not os.path.exists(final_folder):
            os.makedirs(final_folder)

        destination_path = os.path.join(final_folder, os.path.basename(file_path))
        shutil.move(file_path, destination_path)
        print(f"{MSG_SUCCESS}Moved: {file_path} => {destination_path}")
        return destination_path
    except Exception as e:
        print(f"{MSG_ERROR}Could not move file: {file_path}")
        print(f"{MSG_ERROR}{str(e)}")
        return None


def organize_downloads():
    """
    Looks for files in DOWNLOAD_FOLDER_NAME, then moves each one
    to a date-based folder structure in DJ_POOL_BASE_PATH.
    """
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        print(f"{MSG_ERROR}Download folder '{DOWNLOAD_FOLDER_NAME}' not found.")
        return

    files = [
        f for f in os.listdir(DOWNLOAD_FOLDER_NAME)
        if os.path.isfile(os.path.join(DOWNLOAD_FOLDER_NAME, f))
    ]

    if not files:
        print(f"{MSG_WARNING}No files to organize in '{DOWNLOAD_FOLDER_NAME}'.")
        return

    print(f"{MSG_STATUS}Organizing {len(files)} file(s) from '{DOWNLOAD_FOLDER_NAME}' to DJ Pool...{LINE_BREAK}")

    for file_name in files:
        source_path = os.path.join(DOWNLOAD_FOLDER_NAME, file_name)
        new_path = move_to_date_based_folder(source_path)
        if new_path:
            # Optionally do more post-move actions, like ID3 tagging, renaming, etc.
            pass

    print(f"{MSG_NOTICE}All available files have been organized.")


def main():
    """
    Quick CLI to trigger the post-processing flow.
    """
    organize_downloads()

if __name__ == "__main__":
    main()