"""
modules/organize/organize_files.py

Enhances the organizing logic to prompt the user for a destination folder strategy:
1) Create a new date-based folder (default).
2) Reuse a previously used folder (if any).
3) Manually enter a path to create or reuse.

Usage:
- If 'requested' is True, uses 'Requested Songs' subdirectory when choosing date-based.
- If a manual or reused folder is chosen, it overrides the date-based logic.
"""

import os
import shutil
import datetime
from config.settings import DJ_POOL_BASE_PATH, DOWNLOAD_FOLDER_NAME
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING, LINE_BREAK
)

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma", ".aiff", ".alac"}

# Keeps track of a previously used (manually entered or reused) folder in this session.
_last_used_folder = None


def is_audio_file(file_path):
    """
    Checks if the file has an audio extension.
    """
    _, ext = os.path.splitext(file_path.lower())
    return ext in AUDIO_EXTENSIONS


def build_date_based_folder(requested=False):
    """
    Builds a date-based folder path under DJ_POOL_BASE_PATH.
    If 'requested' is True, subfolder is "Requested Songs".
    Example:
      DJ_POOL_BASE_PATH[/Requested Songs]/YYYY/YYYY-MM/YYYY-MM-DD
    """
    now = datetime.datetime.now()
    subfolders = [now.strftime("%Y"), now.strftime("%Y-%m"), now.strftime("%Y-%m-%d")]
    
    base_parts = [DJ_POOL_BASE_PATH]
    if requested:
        base_parts.append("Requested Songs")
    base_parts.extend(subfolders)

    return os.path.join(*base_parts)


def ask_folder_choice(requested=False):
    """
    Asks the user for a folder strategy:
      1) Create a new date-based folder
      2) Use the last folder (if available)
      3) Manually specify a folder path

    Returns the chosen folder path as a string.
    """
    global _last_used_folder

    options_text = (
        "\nChoose a folder strategy:\n"
        "1) Create a new date-based folder\n"
        "2) Use the last folder" + (f" ({_last_used_folder})" if _last_used_folder else " [N/A]") + "\n"
        "3) Manually specify a folder path\n"
        "Enter 1, 2, or 3: "
    )
    
    while True:
        choice = input(options_text).strip()

        # OPTION 1: Build a new date-based folder
        if choice == "1":
            folder = build_date_based_folder(requested=requested)
            print(f"Using date-based folder: {folder}")
            break

        # OPTION 2: Use the last-used folder (if any)
        elif choice == "2":
            if _last_used_folder:
                folder = _last_used_folder
                print(f"Reusing folder: {folder}")
                break
            else:
                print("No previously used folder found. Try again.")

        # OPTION 3: Manually specify a path
        elif choice == "3":
            folder = input("Enter the folder path: ").strip()
            if not folder:
                print("Folder path cannot be empty. Try again.")
                continue
            print(f"Manually using folder: {folder}")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # Ensure folder exists, or create it
    if not os.path.exists(folder):
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"{MSG_SUCCESS}Created new folder: {folder}")
        except Exception as e:
            print(f"{MSG_ERROR}Could not create folder '{folder}': {e}")
            return None

    # Update the last-used folder for future runs
    _last_used_folder = folder
    return folder


def move_audio_file(file_path, destination_folder):
    """
    Moves 'file_path' to 'destination_folder' if it's an audio file.
    Returns the new path or None on failure/skip.
    """
    if not is_audio_file(file_path):
        print(f"{MSG_DEBUG}Skipping non-audio file: {file_path}")
        return None
    try:
        dest = os.path.join(destination_folder, os.path.basename(file_path))
        shutil.move(file_path, dest)
        print(f"{MSG_SUCCESS}Moved: {file_path} => {dest}")
        return dest
    except Exception as e:
        print(f"{MSG_ERROR}Could not move file: {file_path}")
        print(f"{MSG_ERROR}{str(e)}")
        return None


def organize_downloads(requested=False):
    """
    - Looks for files in DOWNLOAD_FOLDER_NAME.
    - Asks the user for a folder strategy (new date-based / reuse / manual).
    - Moves any audio files to that folder.

    If 'requested=True', the date-based folder automatically goes to ".../Requested Songs/YYYY/..."
    """
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        print(f"{MSG_ERROR}Download folder '{DOWNLOAD_FOLDER_NAME}' not found.")
        return

    all_files = [
        f for f in os.listdir(DOWNLOAD_FOLDER_NAME)
        if os.path.isfile(os.path.join(DOWNLOAD_FOLDER_NAME, f))
    ]
    audio_files = [f for f in all_files if is_audio_file(os.path.join(DOWNLOAD_FOLDER_NAME, f))]

    if not audio_files:
        print(f"{MSG_WARNING}No audio files to organize in '{DOWNLOAD_FOLDER_NAME}'.")
        return

    folder_path = ask_folder_choice(requested=requested)
    if not folder_path:
        print(f"{MSG_ERROR}No valid destination folder selected. Aborting.")
        return

    print(
        f"{MSG_STATUS}Organizing {len(audio_files)} file(s) from '{DOWNLOAD_FOLDER_NAME}'...\n"
        f"Destination: {folder_path}\n{LINE_BREAK}"
    )
    for fname in audio_files:
        src = os.path.join(DOWNLOAD_FOLDER_NAME, fname)
        move_audio_file(src, folder_path)

    print(f"{MSG_NOTICE}All available audio files have been organized.")


def main():
    """
    CLI flow:
    1) Check if user wants requested or normal
    2) Then call 'organize_downloads'.
    """
    choice = input("Organize 'Requested' songs? [y/N]: ").strip().lower()
    is_requested = (choice == "y")

    organize_downloads(requested=is_requested)


if __name__ == "__main__":
    main()