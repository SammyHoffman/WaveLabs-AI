"""
cli/main.py

A base template for a main entry point that can orchestrate 
various parts of the DJ automation pipeline:
- Download
- Post-process
- AI cover generation
- Mixcloud upload
- Etc.
"""

import argparse
import sys
import os
# print("sys.path:", sys.path)
# print("Current working directory:", os.getcwd())
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from modules.download.downloader import process_links_from_file, process_links_interactively
from modules.download.post_process import organize_downloads
# from modules.covers.ai_cover_generator import generate_cover
# from modules.mixcloud.uploader import upload_to_mixcloud
from core.color_utils import MSG_NOTICE, MSG_WARNING, MSG_ERROR


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
    parser = argparse.ArgumentParser(description="Main pipeline for DJ automation.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Download Subcommand
    download_parser = subparsers.add_parser("download", help="Download audio from links")
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

    # Placeholder for future subcommands (examples)
    # covers_parser = subparsers.add_parser("covers", help="Generate AI covers")
    # covers_parser.add_argument("--prompt", help="Text prompt for AI cover generation")
    #
    # upload_parser = subparsers.add_parser("upload", help="Upload to Mixcloud")
    # upload_parser.add_argument("--file", help="Path to the audio file or folder to upload")

    return parser


def main():
    """
    Main function to orchestrate the DJ automation pipeline.
    """
    add_project_root_to_path()
    parser = setup_argparser()
    args = parser.parse_args()

    if args.command == "download":
        handle_download_subcommand(args)
    # elif args.command == "covers":
    #     if args.prompt:
    #         generate_cover(args.prompt)
    #     else:
    #         print(f"{MSG_WARNING}No prompt provided for AI cover generation.")
    #
    # elif args.command == "upload":
    #     if args.file:
    #         upload_to_mixcloud(args.file)
    #     else:
    #         print(f"{MSG_WARNING}No file specified for upload.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()