# mixcloud_cli.py

#!/usr/bin/env python3
"""
mixcloud_cli.py

CLI entrypoint that uses the advanced scheduler logic in 'modules/mixcloud/scheduler.py'
for uploading tracks to Mixcloud with OAuth, scheduling, covers, etc.
"""

import os
import sys
import argparse

# Adjust if you need to:
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.mixcloud.scheduler import run_mixcloud_upload
from config.mixcloud.settings import MSG_STATUS, MSG_ERROR

def handle_mixcloud_subcommand(args):
    """
    Ties to the 'upload' subcommand for Mixcloud.
    """
    print(f"{MSG_STATUS}Starting Mixcloud upload flow...")
    run_mixcloud_upload()

def main():
    parser = argparse.ArgumentParser(
        description="Mixcloud CLI with advanced scheduling and covers."
    )
    subparsers = parser.add_subparsers(dest="command", help="Mixcloud commands")

    upload_parser = subparsers.add_parser("upload", help="Upload multiple tracks to Mixcloud with scheduling.")
    # We might not need extra args since run_mixcloud_upload does interactive prompts.

    args = parser.parse_args()

    if args.command == "upload":
        handle_mixcloud_subcommand(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()