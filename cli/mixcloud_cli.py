# mixcloud_cli.py

#!/usr/bin/env python3
"""
mixcloud_cli.pyq

CLI for Mixcloud uploads. Depends on modules.mixcloud.uploader.
"""

import os
import sys
import argparse

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.mixcloud.uploader import upload_to_mixcloud
from core.color_utils import MSG_STATUS, MSG_ERROR


def handle_upload_subcommand(args):
    if not args.file:
        print(f"{MSG_ERROR}No file specified for upload. Use --file <path>.")
        return

    print(f"{MSG_STATUS}Uploading to Mixcloud => {args.file}")
    success = upload_to_mixcloud(args.file)
    if success:
        print(f"{MSG_STATUS}Mixcloud upload complete.")
    else:
        print(f"{MSG_ERROR}Mixcloud upload failed.")


def main():
    parser = argparse.ArgumentParser(
        description="Mixcloud upload CLI.",
        epilog="Usage example: python mixcloud_cli.py upload --file <audiofile>"
    )
    subparsers = parser.add_subparsers(dest="command", help="Mixcloud commands")

    upload_parser = subparsers.add_parser("upload", help="Upload files to Mixcloud")
    upload_parser.add_argument("--file", help="Path to the audio file or folder to upload")

    args = parser.parse_args()

    if args.command == "upload":
        handle_upload_subcommand(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()