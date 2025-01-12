"""
cli/organize_cli.py

CLI script that triggers the newly enhanced organizing tasks with folder strategy prompts.
"""

import argparse
import os
from modules.organize.organize_files import organize_downloads
from core.color_utils import MSG_NOTICE, MSG_WARNING
from config.settings import DOWNLOAD_FOLDER_NAME

def main():
    parser = argparse.ArgumentParser(
        description="CLI for file organizing tasks."
    )
    parser.add_argument(
        "--requested",
        action="store_true",
        help="Organizes songs as 'Requested,' affecting the date-based folder path."
    )

    args = parser.parse_args()

    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        print(f"{MSG_WARNING}Download folder '{DOWNLOAD_FOLDER_NAME}' not found.")
        return

    if args.requested:
        print(f"{MSG_NOTICE}Organizing only requested songs...")
        organize_downloads(requested=True)
    else:
        print(f"{MSG_NOTICE}Organizing all downloaded files...")
        organize_downloads(requested=False)

if __name__ == "__main__":
    main()