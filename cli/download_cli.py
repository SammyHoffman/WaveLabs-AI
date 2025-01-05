"""
cli/download_cli.py

Base template for a CLI script that triggers downloading tasks.
"""

import argparse
from modules.download.downloader import process_links_interactively, process_links_from_file
from modules.download.post_process import organize_downloads
from core.color_utils import MSG_NOTICE, MSG_WARNING

def main():
    parser = argparse.ArgumentParser(description="CLI for audio downloading and organization.")
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

    args = parser.parse_args()

    if args.mode == "interactive":
        process_links_interactively()
    else:
        process_links_from_file()

    if args.organize:
        print(f"{MSG_NOTICE}Organizing downloaded files...")
        organize_downloads()

if __name__ == "__main__":
    main()