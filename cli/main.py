#!/usr/bin/env python3
"""
cli/main.py

Now includes a 'config' subcommand that:
- Checks API keys from settings.py
- Reads/writes a .env file
- Honors `--set KEY=VALUE` flags to update or add new keys directly from the CLI
- Allows initialization of user_settings.py with --init-settings flag.
"""

import argparse
import sys
import os
import re
# from djautomation import __version__

# 1) Add the project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    # sys.path.append(project_root)
    sys.path.insert(0, project_root)

# 2) Import modules and settings
from modules.download.downloader import (
    process_links_from_file,
    process_links_interactively
)
from modules.covers.create_album_cover import main as create_album_covers_main, test_run_album_covers
from modules.download.download_pexel import search_and_download_photos
from modules.organize.organize_files import organize_downloads
from cli.mixcloud_cli import handle_mixcloud_subcommand
from core.color_utils import (
    COLOR_GREEN, COLOR_CYAN, COLOR_RESET, COLOR_BLUE, COLOR_YELLOW,
    MSG_STATUS, MSG_NOTICE, MSG_WARNING, MSG_ERROR, LINE_BREAK, MSG_SUCCESS, MSG_DEBUG
)
from config.settings import (
    TAGS, DOWNLOAD_FOLDER_NAME,
    MIXCLOUD_CLIENT_ID, MIXCLOUD_CLIENT_SECRET,
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
    LASTFM_API_KEY, DEEZER_API_KEY,
    MUSICBRAINZ_API_TOKEN, PEXEL_API_KEY,
    DEBUG_MODE, LINKS_FILE, USER_CONFIG_FOLDER,
    ensure_user_py_settings, load_user_py_settings_as_dict,
    LOCAL_TRACK_DIR, EXTERNAL_TRACK_DIR, USE_EXTERNAL_TRACK_DIR,
    DJ_POOL_BASE_PATH, COVER_IMAGE_DIRECTORY, FINISHED_DIRECTORY,
    PUBLISHED_DATES, TITLES_FILE, UPLOAD_LINKS_FILE,
    
)

from __init__ import __version__

def banner():
    return f"""{COLOR_CYAN}
                   _                  _ 
         /\ /\__ _| |_ __ _ _____   _(_)
        / //_/ _` | __/ _` |_  / | | | |
       / __ \ (_| | || (_| |/ /| |_| | |
       \/  \/\__,_|\__\__,_/___|\__,_|_|
**************************************************
*       Welcome to the DJ CLI by Katazui.com     *
*  Control your entire DJ workflow in one place  *
*            Version: {__version__}                *      
**************************************************
{COLOR_RESET}"""

def add_project_root_to_path():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.append(root_dir)


def print_loaded_configurations():
    """
    Prints a summary of key loaded configuration values.
    This can be triggered with a flag (like --verbose-config) or always printed
    if DEBUG_MODE is True.
    """
    print(f"{MSG_STATUS}Loaded Settings:")
    print(f"{MSG_DEBUG}DEBUG_MODE: {COLOR_GREEN}{DEBUG_MODE}")
    print(f"  {MSG_NOTICE}API Keys:")
    print(f"    {MSG_DEBUG}MIXCLOUD_CLIENT_ID: {COLOR_GREEN}{MIXCLOUD_CLIENT_ID}")
    print(f"    {MSG_DEBUG}SPOTIFY_CLIENT_ID: {COLOR_GREEN}{SPOTIFY_CLIENT_ID}")
    print(f"    {MSG_DEBUG}LASTFM_API_KEY: {COLOR_GREEN}{LASTFM_API_KEY}")
    # print(f"    {MSG_DEBUG}DEEZER_API_KEY: {DEEZER_API_KEY}")
    # print(f"    {MSG_DEBUG}MUSICBRAINZ_API_TOKEN: {MUSICBRAINZ_API_TOKEN}")
    print(f"    {MSG_DEBUG}PEXEL_API_KEY: {COLOR_GREEN}{PEXEL_API_KEY}")
    print(f"  {MSG_NOTICE}Folder Paths:")
    print(f"    {MSG_DEBUG}DJ_POOL_BASE_PATH: {COLOR_GREEN}{DJ_POOL_BASE_PATH}")
    print(f"    {MSG_DEBUG}DOWNLOADS_FOLDER: {COLOR_GREEN}{DOWNLOAD_FOLDER_NAME}")
    print(f"    {MSG_DEBUG}COVER_IMAGE_DIRECTORY ({COLOR_YELLOW}up_mixes{COLOR_RESET}): {COLOR_GREEN}{COVER_IMAGE_DIRECTORY}")
    print(f"    {MSG_DEBUG}FINISHED_DIRECTORY ({COLOR_YELLOW}up_mixes{COLOR_RESET}): {COLOR_GREEN}{FINISHED_DIRECTORY}")
    if USE_EXTERNAL_TRACK_DIR:
        print(f"    {MSG_DEBUG}EXTERNAL_TRACK_DIR ({COLOR_YELLOW}up_mixes{COLOR_RESET}): {COLOR_GREEN}{EXTERNAL_TRACK_DIR}")
    else:
        print(f"    {MSG_DEBUG}LOCAL_TRACK_DIR ({COLOR_YELLOW}up_mixes{COLOR_RESET}): {COLOR_GREEN}{LOCAL_TRACK_DIR}")
    print(f"  {MSG_NOTICE}File Paths:")
    print(f"    {MSG_DEBUG}TITLES_FILE ({COLOR_YELLOW}up_mixes): {COLOR_GREEN}{TITLES_FILE}")
    print(f"    {MSG_DEBUG}PUBLISHED_DATES ({COLOR_YELLOW}up_mixes{COLOR_RESET}): {COLOR_GREEN}{PUBLISHED_DATES}")
    print(f"    {MSG_DEBUG}UPLOAD_LINKS_FILE ({COLOR_YELLOW}up_mixes{COLOR_RESET}): {COLOR_GREEN}{UPLOAD_LINKS_FILE}")
    print(f"    {MSG_DEBUG}LINKS_FILE ({COLOR_YELLOW}dl_audio{COLOR_RESET}): {COLOR_GREEN}{LINKS_FILE}")
    print(LINE_BREAK)


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
        organize_downloads(requested=False)

def handle_download_pexel_subcommand(args):
    one_folder_up = os.path.dirname(USER_CONFIG_FOLDER)
    folder_path = os.path.join(one_folder_up, 'content', 'albumCovers', 'pexel')
    log_path = os.path.join(one_folder_up, 'content', 'albumCovers', 'downloaded_pexel_photos.txt')
    search_and_download_photos(
        tags=TAGS,
        total_photos=args.num_photos,
        folder=folder_path,
        log_file=log_path
    )

def handle_organize_subcommand(args):
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        print(f"{MSG_WARNING}Download folder '{DOWNLOAD_FOLDER_NAME}' not found.")
        return

    if args.requested:
        print(f"{MSG_NOTICE}Organizing only requested songs...")
        # Add your specific logic for requested songs here.
    else:
        print(f"{MSG_NOTICE}Organizing all downloaded files...")
        organize_downloads()

def handle_create_album_covers_subcommand(args):
    if args.test:
        print(f"{MSG_NOTICE}Running test mode for album covers...")
        test_run_album_covers()
    else:
        create_album_covers_main()

def handle_config_subcommand(args):
    """
    Handles the configuration subcommand. Processes .env updates, and,
    if --init-settings is specified, creates user_settings.py in the
    user configuration folder.
    """
    dotenv_path = os.path.join(project_root, ".env")
    env_dict = parse_env_file(dotenv_path)

    changed_anything = False
    updated_keys = {}

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

    # NEW: If user passed --init-settings, create user_settings.py in user config folder.
    if args.init_settings:
        try:
            from config.settings import ensure_user_py_settings
            user_settings_path = ensure_user_py_settings()
            print(f"{MSG_SUCCESS}User settings file initialized at: {user_settings_path}")
        except Exception as e:
            print(f"{MSG_ERROR}Failed to initialize user settings: {e}")

    if args.print:
        print_loaded_configurations()

    api_keys = [
        ("MIXCLOUD_CLIENT_ID",     MIXCLOUD_CLIENT_ID),
        ("MIXCLOUD_CLIENT_SECRET", MIXCLOUD_CLIENT_SECRET),
        ("SPOTIFY_CLIENT_ID",      SPOTIFY_CLIENT_ID),
        ("SPOTIFY_CLIENT_SECRET",  SPOTIFY_CLIENT_SECRET),
        ("LASTFM_API_KEY",         LASTFM_API_KEY),
        # ("DEEZER_API_KEY",         DEEZER_API_KEY),
        # ("MUSICBRAINZ_API_TOKEN",  MUSICBRAINZ_API_TOKEN),
        ("PEXEL_API_KEY",          PEXEL_API_KEY),
    ]

    missing = []
    for key_name, val in api_keys:
        if not val:
            missing.append(key_name)

    if not missing:
        if changed_anything:
            print(f"{MSG_SUCCESS}All provided keys saved. No missing keys in settings.py.")
        else:
            print(f"{MSG_SUCCESS}All keys appear to be set. No action required.")
        return

    print(f"{MSG_WARNING}Missing in settings.py: {', '.join(missing)}")
    not_in_env = []
    blank_in_env = []
    for k in missing:
        if k not in env_dict:
            not_in_env.append(k)
        elif env_dict[k].strip() == "":
            blank_in_env.append(k)

    if not_in_env or blank_in_env:
        print(f"{MSG_WARNING}Keys missing or blank in .env: {', '.join(not_in_env + blank_in_env)}")
        choice = input("Add placeholders to .env? [y/N]: ").strip().lower()
        if choice == "y":
            for k in not_in_env:
                env_dict[k] = "PUT_YOUR_VALUE_HERE"
            for k in blank_in_env:
                if env_dict[k] == "":
                    env_dict[k] = "PUT_YOUR_VALUE_HERE"
            write_env_file(dotenv_path, env_dict)
            print(f"{MSG_SUCCESS}Placeholders added. Please edit .env to set real values.")
        else:
            print(f"{MSG_NOTICE}Skipping placeholder creation.")
    else:
        print(f"{MSG_WARNING}They might be in .env but not loaded into settings.py. Check your logic.")

# ----------------------------------------------------------------
#          Utility Functions
# ----------------------------------------------------------------

def parse_env_file(env_path):
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
    with open(env_path, "w", encoding="utf-8") as f:
        for key, val in env_dict.items():
            f.write(f"{key}={val}\n")

def setup_argparser():
    parser = argparse.ArgumentParser(
        prog="djcli",
        description="https://github.com/Katazui/DJAutomation",
        epilog=f"{COLOR_GREEN}Tip:{COLOR_RESET} Use 'djcli config --mc_id YOUR_ID --init-settings' to update .env and initialize user settings."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Download Music
    download_music_parser = subparsers.add_parser("dl_audio", help="Download audio from Youtube/SoundCloud links.")
    download_music_parser.add_argument("--mode",
        choices=["interactive", "file"],
        default="interactive",
        help="Download mode. Default=interactive"
    )
    download_music_parser.add_argument("--organize",
        action="store_true",
        help="Organize after download."
    )

    # Organize
    organize_parser = subparsers.add_parser("org_dl", help="Organize downloaded audio files.")
    organize_parser.add_argument("--requested",
        action="store_true",
        help="Only organize requested songs."
    )

    # Download Pexels
    download_pexel_parser = subparsers.add_parser("dl_pexel", help="Download photos from Pexels.")
    download_pexel_parser.add_argument("--num_photos",
        type=int,
        default=5,
        help="Number of photos per tag. Default=5."
    )

    # Covers
    covers_parser = subparsers.add_parser("create_ac", help="Create album covers from images.")
    covers_parser.add_argument("--test", action="store_true", help="Test mode for creating album covers.")

    # Mixcloud Upload
    mixcloud_parser = subparsers.add_parser("up_mixes", help="Upload multiple tracks to Mixcloud.")
    mixcloud_parser.add_argument("--init-settings", action="store_true", help="Initialize MixCloud Content.")
    mixcloud_parser.add_argument("--dry-run", action="store_true", help="Dry run mode for Mixcloud uploads.")

    # Testing
    test_parser = subparsers.add_parser("test", help="Run tests.")
    test_parser.add_argument("--mixcloud", action="store_true")
    test_parser.add_argument("--download", action="store_true")

    # Config
    config_parser = subparsers.add_parser("config", help="Check or set API keys in .env and manage user settings.")
    config_parser.add_argument("--print", action="store_true", help="Print loaded configurations.")
    config_parser.add_argument("--mc_id",       type=str, help="Set Mixcloud Client ID.")
    config_parser.add_argument("--mc_secret",   type=str, help="Set Mixcloud Client Secret.")
    config_parser.add_argument("--spotify_id",  type=str, help="Set Spotify Client ID.")
    config_parser.add_argument("--spotify_secret", type=str, help="Set Spotify Client Secret.")
    config_parser.add_argument("--lastfm",      type=str, help="Set Last.fm API key.")
    config_parser.add_argument("--deezer",      type=str, help="Set Deezer API key.")
    config_parser.add_argument("--musicbrainz", type=str, help="Set MusicBrainz token.")
    config_parser.add_argument("--pexel",       type=str, help="Set Pexel API key.")
    config_parser.add_argument("--init-settings", action="store_true", help="Initialize (create) user_settings.py in the configuration folder.")


    return parser

# ----------------------------------------------------------------
#          Main Function for CLI
# ----------------------------------------------------------------

def main():
    # Clear terminal screen
    # os.system("cls" if os.name == "nt" else "clear")

    add_project_root_to_path()

    # Load user settings so that if a user_settings.py exists in the user config folder,
    # its values override the defaults.
    try:
        from config.settings import ensure_user_py_settings, load_user_py_settings_as_dict, DEFAULT_PY_SETTINGS
        user_settings_path = ensure_user_py_settings()
        user_cfg = load_user_py_settings_as_dict()
        print(f"{MSG_STATUS}Loaded user settings from: {user_settings_path}")
        # Optionally override specific settings:
        global MIXCLOUD_CLIENT_ID, MIXCLOUD_CLIENT_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        global LASTFM_API_KEY, DEEZER_API_KEY, MUSICBRAINZ_API_TOKEN, PEXEL_API_KEY
        if "MIXCLOUD_CLIENT_ID" in user_cfg:
            MIXCLOUD_CLIENT_ID = user_cfg["MIXCLOUD_CLIENT_ID"]
        if "MIXCLOUD_CLIENT_SECRET" in user_cfg:
            MIXCLOUD_CLIENT_SECRET = user_cfg["MIXCLOUD_CLIENT_SECRET"]
        if "SPOTIFY_CLIENT_ID" in user_cfg:
            SPOTIFY_CLIENT_ID = user_cfg["SPOTIFY_CLIENT_ID"]
        if "SPOTIFY_CLIENT_SECRET" in user_cfg:
            SPOTIFY_CLIENT_SECRET = user_cfg["SPOTIFY_CLIENT_SECRET"]
        if "LASTFM_API_KEY" in user_cfg:
            LASTFM_API_KEY = user_cfg["LASTFM_API_KEY"]
        if "DEEZER_API_KEY" in user_cfg:
            DEEZER_API_KEY = user_cfg["DEEZER_API_KEY"]
        if "MUSICBRAINZ_API_TOKEN" in user_cfg:
            MUSICBRAINZ_API_TOKEN = user_cfg["MUSICBRAINZ_API_TOKEN"]
        if "PEXEL_API_KEY" in user_cfg:
            PEXEL_API_KEY = user_cfg["PEXEL_API_KEY"]
    except Exception as e:
        print(f"{MSG_ERROR}Error loading user settings: {e}")

    print(banner())

    parser = setup_argparser()
    args = parser.parse_args()

    if DEBUG_MODE or (hasattr(args, "verbose_config") and args.verbose_config):
        print_loaded_configurations()

    if not args.command:
        parser.print_help()
        return

    if args.command == "dl_audio":
        print(f"{MSG_STATUS}Starting 'download_music' subcommand...\n{LINE_BREAK}")
        handle_download_music_subcommand(args)

    elif args.command == "dl_pexel":
        print(f"{MSG_STATUS}Starting 'download_pexel' subcommand...\n{LINE_BREAK}")
        handle_download_pexel_subcommand(args)

    elif args.command == "create_ac":
        print(f"{MSG_STATUS}Starting 'create album covers' subcommand...\n{LINE_BREAK}")
        handle_create_album_covers_subcommand(args)

    elif args.command == "org_dl":
        print(f"{MSG_STATUS}Starting 'organize download' subcommand...\n{LINE_BREAK}")
        handle_organize_subcommand(args)

    elif args.command == "up_mixes":
        print(f"{MSG_STATUS}Starting 'upload mixcloud mixes' subcommand...\n{LINE_BREAK}")
        handle_mixcloud_subcommand(args)

    elif args.command == "test":
        print(f"{MSG_STATUS}Running custom tests or debug checks...\n{LINE_BREAK}")
        from cli.test_cli import handle_test_subcommand
        handle_test_subcommand(args)

    elif args.command == "config":
        print(f"{MSG_STATUS}Starting 'config' subcommand...\n{LINE_BREAK}")
        handle_config_subcommand(args)

    else:
        print(f"{MSG_ERROR}Unknown subcommand: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main()