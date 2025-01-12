"""
cli/organize_cli.py

Base template for a CLI script that triggers organizing tasks.
"""

import argparse
import os
from modules.organize.organize_files import organize_downloads, move_to_date_based_folder_requested_songs
from core.color_utils import MSG_NOTICE, MSG_WARNING
from config.settings import DOWNLOAD_FOLDER_NAME

def main():
    parser = argparse.ArgumentParser(
        description="CLI for file organizing tasks."
    )
    parser.add_argument(
        "--requested",
        action="store_true",
        help="Organizes only requested songs into a date-based folder under 'Requested Songs'."
    )

    args = parser.parse_args()

    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        print(f"{MSG_WARNING}Download folder '{DOWNLOAD_FOLDER_NAME}' not found.")
        return

    if args.requested:
        print(f"{MSG_NOTICE}Organizing only requested songs...")
        # Loop over files in DOWNLOAD_FOLDER_NAME to move them individually.
        for f in os.listdir(DOWNLOAD_FOLDER_NAME):
            file_path = os.path.join(DOWNLOAD_FOLDER_NAME, f)
            if os.path.isfile(file_path):
                move_to_date_based_folder_requested_songs(file_path)
    else:
        print(f"{MSG_NOTICE}Organizing all downloaded files...")
        organize_downloads()

if __name__ == "__main__":
    main()