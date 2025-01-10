"""
cli/download_cli.py

Base template for a CLI script that triggers downloading tasks.
"""

import argparse
from modules.download.downloader import process_links_interactively, process_links_from_file
from modules.download.post_process import organize_downloads
from modules.download.download_pexel import search_and_download_photos
from core.color_utils import MSG_NOTICE, MSG_WARNING
from config.settings import TAGS

def main():
    parser = argparse.ArgumentParser(
        description="CLI for audio downloading and organization."
    )
    parser.add_argument(
        "--mode", 
        choices=["interactive", "file"], 
        default="interactive",
        help="Download mode: 'interactive' or 'file'. Default is 'interactive'."
    )
    parser.add_argument(
        "--organize", 
        action="store_true",
        help="If set, automatically organize downloaded files after download."
    )
    parser.add_argument(
        "--pexel",
        action="store_true",
        help="If set, download photos from Pexels based on predefined tags."
    )
    parser.add_argument(
        "--num_photos",
        type=int,
        default=5,
        help="Number of photos to download per tag when using --pexel. Default is 5."
    )

    args = parser.parse_args()

    if args.mode == "interactive":
        process_links_interactively()
    else:
        process_links_from_file()

    if args.pexel:
        print(f"{MSG_NOTICE}Starting Pexels photo download...")
        search_and_download_photos(
            tags=TAGS,
            num_photos=args.num_photos,
            folder='content/albumCovers/pexel',
            log_file='module/download_photos.txt'
        )

    if args.organize:
        print(f"{MSG_NOTICE}Organizing downloaded files...")
        organize_downloads()

if __name__ == "__main__":
    main()