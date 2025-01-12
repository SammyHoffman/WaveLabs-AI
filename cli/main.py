#!/usr/bin/env python3
"""
cli/main.py

Now includes a 'config' subcommand that:
- Checks API keys from settings.py
- Reads/writes a .env file
- Honors `--set KEY=VALUE` flags to update or add new keys directly from the CLI
"""

import argparse
import sys
import os
import re

# 1) Add the project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2) Import your modules
from modules.download.downloader import (
    process_links_from_file,
    process_links_interactively
)
from modules.download.download_pexel import search_and_download_photos
from modules.organize.organize_files import organize_downloads
from mixcloud_cli import handle_mixcloud_subcommand
from core.color_utils import (
    COLOR_GREEN, COLOR_CYAN, COLOR_RESET,
    MSG_STATUS, MSG_NOTICE, MSG_WARNING, MSG_ERROR, LINE_BREAK, MSG_SUCCESS
)
from config.settings import (
    TAGS, DOWNLOAD_FOLDER_NAME,
    MIXCLOUD_CLIENT_ID, MIXCLOUD_CLIENT_SECRET,
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
    LASTFM_API_KEY, DEEZER_API_KEY,
    MUSICBRAINZ_API_TOKEN, PEXEL_API_KEY
)

def banner():
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
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.append(root_dir)

# ----------------------------------------------------------------
#          Existing Subcommand Handlers
# ----------------------------------------------------------------

def handle_download_music_subcommand(args):
    if args.mode == "interactive":
        process_links_interactively()
    else:
        process_links_from_file()

    if args.organize:
        print(f"{MSG_NOTICE}Organizing downloaded files...")
        organize_downloads()

def handle_download_pexel_subcommand(args):
    print(f"{MSG_NOTICE}Starting Pexel photo download...")
    search_and_download_photos(
        tags=TAGS,
        total_photos=args.num_photos,
        folder='content/albumCovers/pexel',
        log_file='content/downloaded_pexel_photos.txt'
    )
    if args.organize:
        print(f"{MSG_NOTICE}Organizing downloaded photos...")
        organize_downloads()

def handle_organize_subcommand(args):
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        print(f"{MSG_WARNING}Download folder '{DOWNLOAD_FOLDER_NAME}' not found.")
        return

    if args.requested:
        # If you have a function for requested songs:
        # from modules.organize.organize_files import move_to_date_based_folder_requested_songs
        print(f"{MSG_NOTICE}Organizing only requested songs...")
        # Example logic:
        # for file_name in os.listdir(DOWNLOAD_FOLDER_NAME):
        #     file_path = os.path.join(DOWNLOAD_FOLDER_NAME, file_name)
        #     if os.path.isfile(file_path):
        #         move_to_date_based_folder_requested_songs(file_path)
    else:
        print(f"{MSG_NOTICE}Organizing all downloaded files...")
        organize_downloads()

# ----------------------------------------------------------------
#                   CONFIG SUBCOMMAND
# ----------------------------------------------------------------

def handle_config_subcommand(args):
    """
    1. Reads current .env into a dict.
    2. If user provided flags like `--mc_id`, `--deezer` etc., update .env accordingly.
    3. Checks which keys in settings.py are still missing or empty.
    4. Optionally offers to add placeholders for missing keys.
    """

    dotenv_path = os.path.join(project_root, ".env")
    env_dict = parse_env_file(dotenv_path)  # read existing or empty

    # 1) Collect user-provided keys from flags
    changed_anything = False
    updated_keys = {}

    # If the user provided e.g. --mc_id "abc123", we store it
    if args.mc_id is not None:
        env_dict["MIXCLOUD_CLIENT_ID"] = args.mc_id
        updated_keys["MIXCLOUD_CLIENT_ID"] = args.mc_id
    if args.mc_secret is not None:
        env_dict["MIXCLOUD_CLIENT_SECRET"] = args.mc_secret
        updated_keys["MIXCLOUD_CLIENT_SECRET"] = args.mc_secret
    if args.spotify_id is not None:
        env_dict["SPOTIFY_CLIENT_ID"] = args.spotify_id
        updated_keys["SPOTIFY_CLIENT_ID"] = args.spotify_id
    if args.spotify_secret is not None:
        env_dict["SPOTIFY_CLIENT_SECRET"] = args.spotify_secret
        updated_keys["SPOTIFY_CLIENT_SECRET"] = args.spotify_secret
    if args.lastfm is not None:
        env_dict["LASTFM_API_KEY"] = args.lastfm
        updated_keys["LASTFM_API_KEY"] = args.lastfm
    if args.deezer is not None:
        env_dict["DEEZER_API_KEY"] = args.deezer
        updated_keys["DEEZER_API_KEY"] = args.deezer
    if args.musicbrainz is not None:
        env_dict["MUSICBRAINZ_API_TOKEN"] = args.musicbrainz
        updated_keys["MUSICBRAINZ_API_TOKEN"] = args.musicbrainz
    if args.pexel is not None:
        env_dict["PEXEL_API_KEY"] = args.pexel
        updated_keys["PEXEL_API_KEY"] = args.pexel

    if updated_keys:
        changed_anything = True
        write_env_file(dotenv_path, env_dict)
        for k, v in updated_keys.items():
            print(f"{MSG_NOTICE}Set {k}={v} in .env")

    # 2) Build a list of (key_name, current_value_in_settings)
    api_keys = [
        ("MIXCLOUD_CLIENT_ID",     MIXCLOUD_CLIENT_ID),
        ("MIXCLOUD_CLIENT_SECRET", MIXCLOUD_CLIENT_SECRET),
        ("SPOTIFY_CLIENT_ID",      SPOTIFY_CLIENT_ID),
        ("SPOTIFY_CLIENT_SECRET",  SPOTIFY_CLIENT_SECRET),
        ("LASTFM_API_KEY",         LASTFM_API_KEY),
        ("DEEZER_API_KEY",         DEEZER_API_KEY),
        ("MUSICBRAINZ_API_TOKEN",  MUSICBRAINZ_API_TOKEN),
        ("PEXEL_API_KEY",          PEXEL_API_KEY),
    ]

    # 3) Check which keys are still missing in `settings.py`
    missing = []
    for key_name, val in api_keys:
        if not val:
            missing.append(key_name)

    # If none missing, we are good
    if not missing:
        if changed_anything:
            print(f"{MSG_SUCCESS}All provided keys saved. No missing keys in settings.py.")
        else:
            print(f"{MSG_SUCCESS}All keys appear to be set. No action required.")
        return

    # Otherwise, missing keys remain
    print(f"{MSG_WARNING}The following keys are missing or empty in settings.py: {', '.join(missing)}")

    # 4) See if .env has them but is blank
    not_in_env = []
    blank_in_env = []
    for k in missing:
        if k not in env_dict:
            not_in_env.append(k)
        elif env_dict[k].strip() == "":
            blank_in_env.append(k)

    if not_in_env or blank_in_env:
        print(f"{MSG_WARNING}Keys either not in .env or blank: {', '.join(not_in_env + blank_in_env)}")
        choice = input("Would you like to add placeholders to .env? [y/N]: ").strip().lower()
        if choice == "y":
            for k in not_in_env:
                env_dict[k] = "PUT_YOUR_VALUE_HERE"
            for k in blank_in_env:
                if env_dict[k] == "":
                    env_dict[k] = "PUT_YOUR_VALUE_HERE"

            write_env_file(dotenv_path, env_dict)
            print(f"{MSG_SUCCESS}Added placeholders for missing keys. Please edit .env to set real values.")
        else:
            print(f"{MSG_NOTICE}Skipping .env placeholder creation.")
    else:
        # Means they're actually in .env with real values, but environment wasn't loaded into settings.py
        # Possibly the user needs to 'export' them or re-run the program so .env is read.
        print(f"{MSG_WARNING}They exist in .env with some value, but are not loaded into settings.py? Check your load logic.")

# ----------------------------------------------------------------
#             .env HELPER FUNCTIONS
# ----------------------------------------------------------------

def parse_env_file(env_path):
    """
    Returns a dict of KEY=VALUE from the given .env file, or an empty dict if not found.
    Ignores lines starting with # or blank lines.
    """
    if not os.path.exists(env_path):
        return {}
    env_dict = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r'([^=]+)=(.*)', line)
            if match:
                key = match.group(1).strip()
                val = match.group(2).strip()
                env_dict[key] = val
    return env_dict

def write_env_file(env_path, env_dict):
    """
    Overwrites the .env with KEY=VALUE lines from env_dict.
    """
    with open(env_path, "w", encoding="utf-8") as f:
        for key, val in env_dict.items():
            f.write(f"{key}={val}\n")

# ----------------------------------------------------------------
#           Argparser with separate flags for each API
# ----------------------------------------------------------------

def setup_argparser():
    parser = argparse.ArgumentParser(
        prog="djcli",
        description="https://github.com/Katazui/DJAutomation",
        epilog=f"{COLOR_GREEN}Tip:{COLOR_RESET} Use 'djcli config --mc_id YOUR_ID --mc_secret YOUR_SECRET' to update .env."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Download Music
    download_music_parser = subparsers.add_parser("download_music", help="Download audio from links.")
    download_music_parser.add_argument("--mode",
        choices=["interactive", "file"],
        default="interactive",
        help="Download mode (interactive or file-based). Default is 'interactive'."
    )
    download_music_parser.add_argument("--organize",
        action="store_true",
        help="Organize files after downloading."
    )

    # Download Pexels
    download_pexel_parser = subparsers.add_parser("download_pexel", help="Download photos from Pexel API.")
    download_pexel_parser.add_argument("--num_photos",
        type=int,
        default=5,
        help="Number of photos to download per tag. Default is 5."
    )

    # Organize
    organize_parser = subparsers.add_parser("organize", help="Organize downloaded files.")
    organize_parser.add_argument("--requested",
        action="store_true",
        help="Organize only requested songs."
    )

    # Mixcloud Upload
    subparsers.add_parser("upload", help="Upload multiple tracks to Mixcloud.")

    # Testing
    test_parser = subparsers.add_parser("test", help="Run internal debug checks or custom tests.")
    test_parser.add_argument("--mixcloud", action="store_true", help="Run Mixcloud-specific tests.")
    test_parser.add_argument("--download", action="store_true", help="Run download-specific tests.")

    # Config Subcommand
    config_parser = subparsers.add_parser("config", help="Check or set API keys via flags.")
    config_parser.add_argument("--mc_id",       type=str, help="Set Mixcloud Client ID in .env.")
    config_parser.add_argument("--mc_secret",   type=str, help="Set Mixcloud Client Secret in .env.")
    config_parser.add_argument("--spotify_id",  type=str, help="Set Spotify Client ID in .env.")
    config_parser.add_argument("--spotify_secret", type=str, help="Set Spotify Client Secret in .env.")
    config_parser.add_argument("--lastfm",      type=str, help="Set Last.fm API key in .env.")
    config_parser.add_argument("--deezer",      type=str, help="Set Deezer API key in .env.")
    config_parser.add_argument("--musicbrainz", type=str, help="Set MusicBrainz API token in .env.")
    config_parser.add_argument("--pexel",       type=str, help="Set Pexel API key in .env.")

    return parser

# ----------------------------------------------------------------
#                       Main
# ----------------------------------------------------------------

def main():
    add_project_root_to_path()
    print(banner())

    parser = setup_argparser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "download_music":
        print(f"{MSG_STATUS}Starting 'download_music' subcommand...{LINE_BREAK}")
        handle_download_music_subcommand(args)

    elif args.command == "download_pexel":
        print(f"{MSG_STATUS}Starting 'download_pexel' subcommand...{LINE_BREAK}")
        handle_download_pexel_subcommand(args)

    elif args.command == "organize":
        print(f"{MSG_STATUS}Starting 'organize' subcommand...{LINE_BREAK}")
        handle_organize_subcommand(args)

    elif args.command == "upload":
        print(f"{MSG_STATUS}Starting 'upload' subcommand...{LINE_BREAK}")
        handle_mixcloud_subcommand(args)

    elif args.command == "test":
        print(f"{MSG_STATUS}Running custom tests or debug checks...{LINE_BREAK}")
        from cli.test_cli import handle_test_subcommand
        handle_test_subcommand(args)

    elif args.command == "config":
        print(f"{MSG_STATUS}Starting 'config' subcommand...{LINE_BREAK}")
        handle_config_subcommand(args)

    else:
        print(f"{MSG_ERROR}Unknown subcommand: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()