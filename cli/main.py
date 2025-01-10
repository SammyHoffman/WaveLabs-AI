#!/usr/bin/env python3
"""
cli/main.py

A base template for a main entry point that can orchestrate 
various parts of the DJ automation pipeline:
- Download Music
- Download Pexel Photos
- Post-process
- AI cover generation (future)
- Mixcloud upload
- Etc.

Now includes separate `download_music` and `download_pexel` subcommands.
"""

import argparse
import sys
import os

# 1) Add the project root to sys.path, so Python sees 'core/' and 'modules/' as importable packages
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2) Import your modules
from modules.download.downloader import process_links_from_file, process_links_interactively
from modules.download.post_process import organize_downloads
from modules.download.download_pexel import search_and_download_photos
from mixcloud_cli import handle_mixcloud_subcommand
from core.color_utils import (
    COLOR_GREEN, COLOR_CYAN, COLOR_RESET,
    MSG_STATUS, MSG_NOTICE, MSG_WARNING, MSG_ERROR, MSG_SUCCESS, LINE_BREAK
)
from config.settings import TAGS

def banner():
    """
    Returns a colorful ASCII banner for the CLI.
    """
    return f"""{COLOR_CYAN}
            _                  _ 
  /\ /\__ _| |_ __ _ _____   _(_)
 / //_/ _` | __/ _` |_  / | | | |
/ __ \ (_| | || (_| |/ /| |_| | |
\/  \/\__,_|\__\__,_/___|\__,_|_|
************************************************
*  Welcome to the DJ Automation CLI!           *
*  Control your entire DJ workflow in one place*
************************************************
{COLOR_RESET}"""

def add_project_root_to_path():
    """
    Ensures the project root is in the Python path, so all imports work correctly.
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.append(root_dir)


def handle_download_music_subcommand(args):
    """
    Handles the `download_music` subcommand logic.
    """
    if args.mode == "interactive":
        process_links_interactively()
    else:
        process_links_from_file()

    if args.organize:
        print(f"{MSG_NOTICE}Organizing downloaded files...")
        organize_downloads()


def handle_download_pexel_subcommand(args):
    """
    Handles the `download_pexel` subcommand logic.
    """
    print(f"{MSG_NOTICE}Starting Pexels photo download...")
    search_and_download_photos(
        tags=TAGS,
        total_photos=args.num_photos,
        folder='content/albumCovers/pexel',
        log_file='content/downloaded_pexel_photos.txt'  # Corrected path
    )

    # if args.organize:
    #     print(f"{MSG_NOTICE}Organizing downloaded photos...")
    #     organize_downloads()


def setup_argparser():
    """
    Sets up the argument parser and subcommands.
    """
    parser = argparse.ArgumentParser(
        description="Main pipeline for DJ automation.",
        epilog=f"{COLOR_GREEN}Tip:{COLOR_RESET} Try 'download_music --mode file --organize' or 'download_pexel --num_photos 10' to run specific processes."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Download Music Subcommand
    download_music_parser = subparsers.add_parser("download_music", help="Download audio from links.")
    download_music_parser.add_argument(
        "--mode",
        choices=["interactive", "file"],
        default="interactive",
        help="Download mode (interactive or file-based). Default is 'interactive'."
    )
    download_music_parser.add_argument(
        "--organize",
        action="store_true",
        help="Organize files after downloading."
    )

    # Download Pexels Subcommand
    download_pexel_parser = subparsers.add_parser("download_pexel", help="Download photos from Pexels based on predefined tags.")
    download_pexel_parser.add_argument(
        "--num_photos",
        type=int,
        default=5,
        help="Number of photos to download per tag. Default is 5."
    )
    download_pexel_parser.add_argument(
        "--organize",
        action="store_true",
        help="Organize photos after downloading."
    )

    # Mixcloud Upload Subcommand (matches the subcommand in mixcloud_cli)
    upload_parser = subparsers.add_parser("upload", help="Upload multiple tracks to Mixcloud.")

    # Test Subcommand - references a new file in cli/test_cli.py
    test_parser = subparsers.add_parser("test", help="Run internal debug checks or custom tests")
    test_parser.add_argument(
        "--mixcloud",
        action="store_true",
        help="Run Mixcloud-specific tests (tests/test_mixcloud.py)"
    )
    test_parser.add_argument(
        "--download",
        action="store_true",
        help="Run download-specific tests (tests/test_download.py)"
    )
    return parser


def main():
    """
    Main function to orchestrate the DJ automation pipeline.
    """
    add_project_root_to_path()
    print(banner())

    parser = setup_argparser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "download_music":
        print(f"{MSG_STATUS}Starting 'download_music' subcommand...")
        handle_download_music_subcommand(args)

    elif args.command == "download_pexel":
        print(f"{MSG_STATUS}Starting 'download_pexel' subcommand...")
        handle_download_pexel_subcommand(args)

    elif args.command == "upload":
        print(f"{MSG_STATUS}Starting 'upload' subcommand...")
        handle_mixcloud_subcommand(args)

    elif args.command == "test":
        print(f"{MSG_STATUS}Running custom tests or debug checks...")
        from cli.test_cli import handle_test_subcommand
        handle_test_subcommand(args)

    else:
        print(f"{MSG_ERROR}Unknown subcommand: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()