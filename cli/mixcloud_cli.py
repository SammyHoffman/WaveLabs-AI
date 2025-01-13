#!/usr/bin/env python3
"""
mixcloud_cli.py

A more robust and user-friendly CLI for uploading tracks to Mixcloud with OAuth, 
scheduled publishing, cover images, etc. Uses the advanced logic in:
  modules/mixcloud/uploader.py  (or scheduler.py if you prefer that naming)

Key Steps:
1. Checks if track directories have any files for upload (MP3 or M4A).
2. Checks if there are any cover images in the images directory (optional).
3. If everything looks good, calls the main Mixcloud upload function.
4. Prints colorful status messages to guide the user.
"""

import os
import sys
import argparse

# Adjust path if needed to ensure your modules are accessible
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import your core logic and color utilities
from modules.mixcloud.uploader import main as run_mixcloud_upload
# Or if you want to call a specialized function, e.g.:
# from modules.mixcloud.uploader import run_mixcloud_upload

from config.settings import (
    USE_EXTERNAL_TRACK_DIR,
    LOCAL_TRACK_DIR,
    EXTERNAL_TRACK_DIR,
    COVER_IMAGE_DIRECTORY,
    DEBUG_MODE
)
from core.color_utils import (
    MSG_STATUS, MSG_ERROR, MSG_NOTICE, MSG_WARNING,
    MSG_SUCCESS, COLOR_CYAN, COLOR_GREEN, COLOR_RESET
)


def banner():
    """
    Returns a colorful ASCII banner to greet the user.
    """
    return f"""{COLOR_CYAN}Hi there! Welcome to the Mixcloud CLI.{COLOR_RESET}"""


def check_directories():
    """
    Checks if the relevant directories have files.
    Returns (bool, str) indicating success and a message if any problem found.
    """
    if USE_EXTERNAL_TRACK_DIR:
        track_dir = EXTERNAL_TRACK_DIR
    else:
        track_dir = LOCAL_TRACK_DIR

    if not os.path.isdir(track_dir):
        return False, f"{MSG_ERROR}Track directory does not exist => {track_dir}"

    # Check for audio files
    audio_files = []
    for ext in (".mp3", ".m4a"):
        audio_files.extend([f for f in os.listdir(track_dir) if f.lower().endswith(ext)])

    if not audio_files:
        return False, f"{MSG_WARNING}No audio files found in => {track_dir}"

    # Optional: check cover images
    if not os.path.isdir(COVER_IMAGE_DIRECTORY):
        return False, f"{MSG_ERROR}Cover image directory does not exist => {COVER_IMAGE_DIRECTORY}"

    cover_images = []
    for ext in (".png", ".jpg", ".jpeg"):
        cover_images.extend([f for f in os.listdir(COVER_IMAGE_DIRECTORY) if f.lower().endswith(ext)])

    if not cover_images:
        # It's not strictly required, but we can warn if covers are missing
        print(f"{MSG_NOTICE}No cover images found in => {COVER_IMAGE_DIRECTORY}")
        # We won't fail here; the user might not want covers

    return True, f"{MSG_SUCCESS}Track directory and cover directory look good."


def handle_mixcloud_subcommand(args):
    """
    Orchestrates the checks before calling run_mixcloud_upload.
    """
    print(f"{MSG_STATUS}Checking directories before Mixcloud upload...")

    ok, message = check_directories()
    print(message)
    if not ok:
        print(f"{MSG_ERROR}Cannot proceed with Mixcloud upload.")
        sys.exit(1)

    print(f"{MSG_STATUS}Starting Mixcloud upload flow...\n")
    # Here we call run_mixcloud_upload from the modules/mixcloud/uploader.
    run_mixcloud_upload()


def main():
    """
    Main CLI entry point. Provides a subcommand 'upload' for Mixcloud,
    plus a banner and color-coded messages.
    """
    parser = argparse.ArgumentParser(
        description="Mixcloud CLI with scheduling and cover uploads.",
        epilog=f"{COLOR_GREEN}Tip:{COLOR_RESET} Use 'upload' to start the Mixcloud flow."
    )
    subparsers = parser.add_subparsers(dest="command", help="Mixcloud commands")

    upload_parser = subparsers.add_parser(
        "upload",
        help="Upload multiple tracks to Mixcloud with interactive scheduling."
    )
    # If you need extra args, add them here
    # e.g., upload_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    print(banner())

    if not args.command:
        parser.print_help()
        return

    if args.command == "upload":
        handle_mixcloud_subcommand(args)
    else:
        print(f"{MSG_WARNING}Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()