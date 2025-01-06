#!/usr/bin/env python3
"""
cli/main.py

A base template for a main entry point that can orchestrate 
various parts of the DJ automation pipeline:
- Download
- Post-process
- AI cover generation (future)
- Mixcloud upload (future)
- Etc.
"""

import argparse
import sys
import os

# 1) Add the project root to sys.path, so Python sees 'core/' and 'modules/' as importable packages
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2) Now import your modules
from modules.download.downloader import process_links_from_file, process_links_interactively
from modules.download.post_process import organize_downloads
from mixcloud_cli import handle_upload_subcommand
# from modules.covers.ai_cover_generator import generate_cover
# from modules.mixcloud.uploader import upload_to_mixcloud
from core.color_utils import (
    COLOR_GREEN, COLOR_CYAN, COLOR_RESET, MSG_STATUS, MSG_NOTICE, MSG_WARNING, MSG_ERROR, MSG_SUCCESS, LINE_BREAK
)


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


def handle_download_subcommand(args):
    """
    Handles the `download` subcommand logic.
    """
    if args.mode == "interactive":
        process_links_interactively()
    else:
        process_links_from_file()

    if args.organize:
        print(f"{MSG_NOTICE}Organizing downloaded files...")
        organize_downloads()


def setup_argparser():
    """
    Sets up the argument parser and subcommands.
    """
    parser = argparse.ArgumentParser(
        description="Main pipeline for DJ automation.",
        epilog=f"{COLOR_GREEN}Tip:{COLOR_RESET} Try 'download --mode file --organize' to run a full process."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Download Subcommand
    download_parser = subparsers.add_parser("download", help="Download audio from links.")
    download_parser.add_argument(
        "--mode",
        choices=["interactive", "file"],
        default="interactive",
        help="Download mode (interactive or file-based). Default is 'interactive'."
    )
    download_parser.add_argument(
        "--organize",
        action="store_true",
        help="Organize files after downloading."
    )

    # Placeholder for future subcommands
    # covers_parser = subparsers.add_parser("covers", help="Generate AI covers")
    # covers_parser.add_argument("--prompt", help="Text prompt for AI cover generation")

    # UPLOAD (Mixcloud)
    upload_parser = subparsers.add_parser("upload", help="Upload to Mixcloud")
    upload_parser.add_argument("--file", help="Path to the audio file to upload")

    return parser


def main():
    """
    Main function to orchestrate the DJ automation pipeline.
    """
    add_project_root_to_path()
    # Print a banner on startup
    print(banner())

    parser = setup_argparser()
    args = parser.parse_args()

    if not args.command:
        # No subcommand provided, just show help
        parser.print_help()
        return

    if args.command == "download":
        print(f"{MSG_STATUS}Starting 'download' subcommand...")
        handle_download_subcommand(args)

    elif args.command == "upload":
        print(f"{MSG_STATUS}Starting 'upload' subcommand...")
        handle_upload_subcommand(args)

    # elif args.command == "covers":
    #     if args.prompt:
    #         print(f"{MSG_STATUS}Generating AI cover with prompt: {args.prompt}")
    #         generate_cover(args.prompt)
    #     else:
    #         print(f"{MSG_WARNING}No prompt provided for AI cover generation.")
    #
    # elif args.command == "upload":
    #     if args.file:
    #         print(f"{MSG_STATUS}Uploading file/folder: {args.file} to Mixcloud...")
    #         upload_to_mixcloud(args.file)
    #     else:
    #         print(f"{MSG_WARNING}No file specified for upload.")

    else:
        print(f"{MSG_ERROR}Unknown subcommand: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()