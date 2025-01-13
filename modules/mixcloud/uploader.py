# modules/mixcloud/uploader.py

"""
A single file integrating Mixcloud uploading, scheduling, and OAuth logic.
References:
- config.settings for environment variables (paths, Mixcloud creds, etc.)
- core.color_utils for colored logs.

Usage:
    python modules/mixcloud/uploader.py
    (Prompts for OAuth and uploads tracks to Mixcloud)
"""

import os
import sys
import csv
import re
import glob
import time
import json
import pytz
import shutil
import requests
import threading
import datetime
import webbrowser
import socketserver
import http.server
from urllib.parse import urlparse, parse_qs

# Ensure project root is in sys.path if needed
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

# Imports from config.settings
from config.settings import (
    # Logging toggles
    DEBUG_MODE as DEBUG,

    # Mixcloud Credentials / Config
    MIXCLOUD_CLIENT_ID as CLIENT_ID,
    MIXCLOUD_CLIENT_SECRET as CLIENT_SECRET,
    MIXCLOUD_PRO_USER as PRO_USER,
    MIXCLOUD_PORT,
    MIXCLOUD_REDIRECT_URI,
    MIXCLOUD_AUTH_URL,
    MIXCLOUD_ENABLED,
    # Track/Cover Paths + Upload Lists
    USE_EXTERNAL_TRACK_DIR,
    LOCAL_TRACK_DIR,
    EXTERNAL_TRACK_DIR,
    COVER_IMAGE_DIRECTORY,
    FINISHED_DIRECTORY,
    TITLES_FILE,
    UPLOAD_LINKS_FILE,
    PUBLISHED_DATES,
    MAX_UPLOADS,
    PUBLISHED_HOUR,
    PUBLISHED_MINUTE,
    TRACK_TAGS
)

# Additional optional references (if you want them):
# from config.settings import DJ_POOL_BASE_PATH, DOWNLOAD_FOLDER_NAME, LINKS_FILE

# Colored logs
from core.color_utils import (
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS,
    MSG_STATUS, MSG_WARNING, LINE_BREAK,
    COLOR_RED, COLOR_GREEN, COLOR_YELLOW,
    COLOR_BLUE, COLOR_CYAN, COLOR_RESET
)

# Global Access Token (set after OAuth)
ACCESS_TOKEN = None

#########################################################
#                 CREATE CONFIGURATION
#########################################################

# Boolean to check if configuration files & path exist
def check_mixcloud_config():
    return all(
        os.path.exists(p) for p in [    
            PUBLISHED_DATES, TITLES_FILE, UPLOAD_LINKS_FILE,
            COVER_IMAGE_DIRECTORY, FINISHED_DIRECTORY
        ]
    )

def create_mixcloud_files():
    # If PUBLISHED_DATES, TITLES_FILE, UPLOAD_LINKS_FILE don't exist, create them.
    if not os.path.exists(PUBLISHED_DATES):
        with open(PUBLISHED_DATES, 'w') as f:
            f.write("")
        print(f"{MSG_NOTICE}Created {PUBLISHED_DATES}")

    if not os.path.exists(TITLES_FILE):
        with open(TITLES_FILE, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "description"])
            writer.writeheader()
        print(f"{MSG_NOTICE}Created {TITLES_FILE}")

    if not os.path.exists(UPLOAD_LINKS_FILE):
        with open(UPLOAD_LINKS_FILE, 'w') as f:
            f.write("")
        print(f"{MSG_NOTICE}Created {UPLOAD_LINKS_FILE}")

    # Create cover image directory if it doesn't exist
    if not os.path.exists(COVER_IMAGE_DIRECTORY):
        os.makedirs(COVER_IMAGE_DIRECTORY)
        print(f"{MSG_NOTICE}Created {COVER_IMAGE_DIRECTORY}")

    # Create finished directory if it doesn't exist
    if not os.path.exists(FINISHED_DIRECTORY):
        os.makedirs(FINISHED_DIRECTORY)
        print(f"{MSG_NOTICE}Created {FINISHED_DIRECTORY}")

    print(f"{MSG_SUCCESS}Configuration files created.")

#########################################################
#                 GENERIC HELPERS
#########################################################

def extract_number(filename: str):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')


def extract_date_from_filename(filename: str):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        try:
            return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            return None
    return None


def extract_date_from_url(url: str):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', url)
    if match:
        try:
            return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            return None
    return None


def remove_first_line(file_path):
    """
    Removes the first line from a file.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        if lines:
            with open(file_path, 'w') as f:
                f.writelines(lines[1:])
            if DEBUG:
                print(f"{MSG_DEBUG}Removed first line from {file_path}.")
        else:
            print(f"{MSG_WARNING}{file_path} is empty. No lines to remove.")
    except Exception as e:
        print(f"{MSG_ERROR}Error removing first line from {file_path}: {e}")


def move_to_finished(track_path, cover_path, finished_dir):
    """
    Moves the track and cover image to the finished directory.
    """
    try:
        shutil.move(track_path, os.path.join(finished_dir, os.path.basename(track_path)))
        if cover_path and os.path.exists(cover_path):
            shutil.move(cover_path, os.path.join(finished_dir, os.path.basename(cover_path)))
    except Exception as e:
        print(f"{MSG_ERROR}Error moving files to finished directory: {e}")


#########################################################
#                OAUTH FLOW
#########################################################

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP request handler for Mixcloud OAuth.
    """
    def do_GET(self):
        global ACCESS_TOKEN
        query_components = parse_qs(urlparse(self.path).query)
        auth_code = query_components.get("code", [""])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        response_html = """
        <html>
        <head><title>Mixcloud OAuth</title></head>
        <body style="text-align:center;font-family:sans-serif;padding-top:20vh;">
            <h1 style="color:#00ff00;">Authorization Successful</h1>
            <p>You can close this window now.</p>
        </body>
        </html>
        """
        self.wfile.write(response_html.encode("utf-8"))

        if auth_code:
            print(f"{MSG_STATUS}Authorization code received.")
            ACCESS_TOKEN = get_access_token(auth_code)
            threading.Thread(target=shutdown_server, args=(self.server,)).start()


def shutdown_server(server):
    server.shutdown()


def get_access_token(auth_code: str):
    """
    Exchanges code for an access token. 
    """
    if not MIXCLOUD_ENABLED or not CLIENT_ID or not CLIENT_SECRET:
        print(f"{MSG_ERROR}Mixcloud not fully configured. Check your .env or settings.")
        return None

    token_url = "https://www.mixcloud.com/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "redirect_uri": MIXCLOUD_REDIRECT_URI,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    resp = requests.post(token_url, data=payload)
    if resp.ok:
        token = resp.json().get("access_token")
        print(f"{MSG_SUCCESS}Access token obtained.")
        return token
    else:
        print(f"{MSG_ERROR}Could not obtain Mixcloud token. {resp.text}")
        return None


def start_oauth_server():
    if not MIXCLOUD_ENABLED:
        print(f"{MSG_WARNING}Mixcloud is disabled. OAuth server will not start.")
        return
    with socketserver.TCPServer(("", MIXCLOUD_PORT), OAuthHandler) as httpd:
        print(f"{MSG_STATUS}Starting OAuth server at {MIXCLOUD_REDIRECT_URI}")
        webbrowser.open(MIXCLOUD_AUTH_URL)
        httpd.serve_forever()


#########################################################
#            TRACK & COVER DISCOVERY
#########################################################

def traverse_external_directory(start_date, max_uploads):
    track_files = []
    for root, dirs, files in os.walk(EXTERNAL_TRACK_DIR):
        for f in files:
            if f.lower().endswith((".mp3", ".m4a")) and not f.startswith("._"):
                dt = extract_date_from_filename(f)
                if dt and (start_date is None or dt > start_date):
                    track_files.append((os.path.join(root, f), dt))
    sorted_tracks = sorted(track_files, key=lambda x: x[1])
    return [fp for fp, dt in sorted_tracks][:max_uploads]


def sort_tracks_by_date(files):
    with_dates = []
    for f in files:
        dt = extract_date_from_filename(os.path.basename(f)) or datetime.datetime.max
        with_dates.append((f, dt))
    return [fp for fp, dt in sorted(with_dates, key=lambda x: x[1])]


def sort_cover_images_by_mix_number(files):
    with_nums = []
    for f in files:
        num = extract_number(os.path.basename(f))
        with_nums.append((f, num))
    return [fp for fp, n in sorted(with_nums, key=lambda x: x[1])]


#########################################################
#           TITLES & PUBLISHED DATES
#########################################################

def parse_published_dates_from_file(file_path: str):
    results = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                ds = line.strip()
                try:
                    date_obj = datetime.datetime.strptime(ds, "%Y-%m-%d")
                    date_obj = date_obj.replace(hour=PUBLISHED_HOUR, minute=PUBLISHED_MINUTE)
                    eastern = pytz.timezone("US/Eastern")
                    local_dt = eastern.localize(date_obj)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    results.append(utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ"))
                except ValueError:
                    print(f"{MSG_WARNING}Invalid date in {file_path}: {ds}")
        return results
    except FileNotFoundError:
        print(f"{MSG_ERROR}Published dates file not found: {file_path}")
        return []


def load_titles_descriptions(titles_file: str):
    items = []
    try:
        with open(titles_file, 'r', encoding='utf-8') as cf:
            reader = csv.DictReader(cf)
            for row in reader:
                items.append({"title": row["title"], "description": row["description"]})
        return items
    except Exception as e:
        print(f"{MSG_ERROR}Error reading {titles_file}: {e}")
        return []


def get_last_uploaded_date(links_file: str):
    dates = []
    try:
        with open(links_file, 'r') as f:
            for line in f:
                url = line.strip()
                d = extract_date_from_url(url)
                if d:
                    dates.append(d)
        if dates:
            return max(dates)
        return None
    except FileNotFoundError:
        print(f"{MSG_WARNING}File not found => {links_file}")
        return None


def get_last_uploaded_mix_number(links_file: str):
    nums = []
    try:
        with open(links_file, 'r') as f:
            for line in f:
                url = line.strip()
                num = extract_number(url)
                if num != float("inf"):
                    nums.append(num)
        return int(max(nums)) if nums else 0
    except FileNotFoundError:
        print(f"{MSG_WARNING}File not found => {links_file}")
        return 0


#########################################################
#              MIXCLOUD UPLOAD LOGIC
#########################################################

def display_upload_info(track_files, cover_images, published_dates, start_mix, title):
    print(f"{MSG_STATUS}Upload Information:")
    for i, track_fp in enumerate(track_files):
        mix_num = start_mix + i
        cimg = None
        for cov in cover_images:
            cnum = extract_number(os.path.basename(cov))
            if cnum == mix_num:
                cimg = cov
                break

        pub_d = published_dates[i] if i < len(published_dates) else "No publish date"
        dt = extract_date_from_filename(os.path.basename(track_fp))
        date_str = dt.strftime("%Y-%m-%d") if dt else None
        if date_str:
            track_name = f"{title} #{mix_num} | {date_str}"
        else:
            track_name = f"{title} #{mix_num}"

        print(f"{MSG_NOTICE}Track {i+1}:")
        print(f"{MSG_NOTICE}  File:        {track_fp}")
        print(f"{MSG_NOTICE}  Cover Image: {cimg if cimg else 'No cover'}")
        print(f"{MSG_NOTICE}  Name:        {track_name}")
        print(f"{MSG_NOTICE}  Publish Date:{pub_d}")
        print("------")


def upload_track(
    file_path, cover_path, mix_number, title, description, publish_date=None, remove_files=True
):
    """
    Actually uploads the track to Mixcloud, referencing global ACCESS_TOKEN.
    """
    global ACCESS_TOKEN

    dt = extract_date_from_filename(os.path.basename(file_path))
    date_str = dt.strftime("%Y-%m-%d") if dt else None
    if date_str:
        track_name = f"{title} #{mix_number} | {date_str}"
    else:
        track_name = f"{title} #{mix_number}"

    upload_url = "https://api.mixcloud.com/upload/"
    data = {
        "name": track_name,
        "description": description
    }
    # Add up to 5 tags from TRACK_TAGS
    for idx, tg in enumerate(TRACK_TAGS):
        data[f"tags-{idx}-tag"] = tg
        if idx >= 4:
            break

    if PRO_USER and publish_date:
        data["publish_date"] = publish_date

    if not ACCESS_TOKEN:
        print(f"{MSG_ERROR}No Mixcloud Access Token. OAuth may have failed.")
        return False

    files = {"mp3": open(file_path, "rb")}
    if cover_path and os.path.exists(cover_path):
        files["picture"] = open(cover_path, "rb")

    if DEBUG:
        print(f"{MSG_DEBUG}Track: {track_name}")
        print(f"{MSG_DEBUG}Data: {data}")
        print(f"{MSG_DEBUG}Files: {list(files.keys())}")

    try:
        resp = requests.post(
            upload_url,
            params={"access_token": ACCESS_TOKEN},
            data=data,
            files=files
        )
        if resp.ok:
            print(f"{MSG_SUCCESS}Successfully uploaded: {track_name}")

            if not DEBUG and remove_files:
                move_to_finished(file_path, cover_path, FINISHED_DIRECTORY)

            remove_first_line(PUBLISHED_DATES)
            result_data = resp.json()
            up_key = result_data.get("result", {}).get("key", "")
            if up_key:
                link_url = f"https://www.mixcloud.com{up_key}"
                with open(UPLOAD_LINKS_FILE, 'a') as f:
                    f.write(f"{link_url}\n")

            print(f"{MSG_SUCCESS}Response Code: {resp.status_code}")
            print(f"{MSG_SUCCESS}Response Text:\n{resp.text}")
            return True
        else:
            print(f"{MSG_ERROR}Error uploading {file_path}: {resp.status_code}\n{resp.text}")
            if resp.status_code == 403:
                err = resp.json()
                err_type = err.get("error", {}).get("type", "")
                if err_type == "RateLimitException":
                    ra = err.get("error", {}).get("retry_after", 0)
                    wait_minutes = (ra // 60) + 1
                    print(f"{MSG_NOTICE}Rate limit reached. Wait {wait_minutes} minutes.")
                    return {"retry_after": wait_minutes * 60}
            return False

    except Exception as e:
        print(f"{MSG_ERROR}Exception: {e}")
        return False

    finally:
        files["mp3"].close()
        if "picture" in files:
            files["picture"].close()

#########################################################
#              MAIN EXECUTION
#########################################################

def main():
    """
    Main function handling Mixcloud OAuth, scanning tracks, user selection,
    and uploading in a single run.
    """
    global ACCESS_TOKEN

    # If Mixcloud is disabled, skip
    if not MIXCLOUD_ENABLED:
        print(f"{MSG_WARNING}Mixcloud is disabled in config. Exiting.")
        sys.exit(0)

    # # Check for configuration files
    # if not check_mixcloud_config():
    #     print(f"{MSG_WARNING}Configuration files not found. Creating...")
    #     create_mixcloud_files()
    #     print(f"{MSG_WARNING}Please fill in the necessary details and run again.")
    #     sys.exit(0)

    # Start OAuth in a thread
    t = threading.Thread(target=start_oauth_server)
    t.start()

    # Wait for token
    while ACCESS_TOKEN is None:
        time.sleep(1)

    # Load titles
    titles_data = load_titles_descriptions(TITLES_FILE)
    if not titles_data:
        print(f"{MSG_ERROR}No titles found in CSV: {TITLES_FILE}. Exiting.")
        sys.exit(1)

    print(f"{MSG_STATUS}Available Titles:")
    for idx, item in enumerate(titles_data):
        print(f"{idx+1}. {item['title']}")

    selected_title = ""
    selected_description = ""
    while True:
        try:
            pick = int(input(f"{MSG_NOTICE}Select a title to use: "))
            if 1 <= pick <= len(titles_data):
                selected_title = titles_data[pick-1]["title"]
                selected_description = titles_data[pick-1]["description"]
                break
            else:
                print(f"{MSG_WARNING}Invalid selection. Try again.")
        except ValueError:
            print(f"{MSG_WARNING}Please enter a valid number.")

    last_mixnum = get_last_uploaded_mix_number(UPLOAD_LINKS_FILE)
    next_mixnum = last_mixnum + 1
    print(f"{MSG_STATUS}Last uploaded mix # => {last_mixnum}")
    print(f"{MSG_STATUS}Next expected mix # => {next_mixnum}")

    last_date = get_last_uploaded_date(UPLOAD_LINKS_FILE)
    if last_date:
        print(f"{MSG_STATUS}Last uploaded date => {last_date.strftime('%Y-%m-%d')}")
    else:
        print(f"{MSG_STATUS}No last uploaded date found.")

    start_mix = next_mixnum

    # Ask user if the next mix number is correct
    inp = input(f"{MSG_NOTICE}Start from Mix #{start_mix}? (y/n): ").lower()
    if inp != "y":
        try:
            start_mix = int(input(f"{MSG_NOTICE}Enter a new starting mix number: "))
        except ValueError:
            print(f"{MSG_WARNING}Invalid input. Using default => {next_mixnum}")
            start_mix = next_mixnum
    if inp == "y" and start_mix != next_mixnum:
        print(f"{MSG_WARNING}Starting from mix #{start_mix} instead of {next_mixnum}")

    # Covers
    cover_imgs = sort_cover_images_by_mix_number(
        glob.glob(os.path.join(COVER_IMAGE_DIRECTORY, "*.png")) +
        glob.glob(os.path.join(COVER_IMAGE_DIRECTORY, "*.jpg"))
    )

    # Published dates
    published_dates = parse_published_dates_from_file(PUBLISHED_DATES)

    # Determine track list
    if USE_EXTERNAL_TRACK_DIR:
        t_files = traverse_external_directory(last_date, 1000)
        remove_after = False
    else:
        all_files = glob.glob(os.path.join(LOCAL_TRACK_DIR, "*.mp3")) + glob.glob(os.path.join(LOCAL_TRACK_DIR, "*.m4a"))
        t_files = sort_tracks_by_date(all_files)
        remove_after = True

    if not t_files:
        print(f"{MSG_WARNING}No new tracks found.")
        sys.exit(0)

    print(f"{MSG_STATUS}{len(t_files)} tracks found.")
    default_up = min(MAX_UPLOADS, len(t_files))
    try:
        inp = input(f"{MSG_NOTICE}How many to upload? (Default: {default_up}): ").strip()
        if not inp:
            num_up = default_up
        else:
            num_up = int(inp)
            if num_up > len(t_files):
                num_up = len(t_files)
    except ValueError:
        print(f"{MSG_WARNING}Invalid input. Using default => {default_up}")
        num_up = default_up

    t_files = t_files[:num_up]

    # Show info
    display_upload_info(t_files, cover_imgs, published_dates, start_mix, selected_title)

    confirm = input(f"{MSG_WARNING}Confirm upload of {num_up} tracks? (y/n): ").lower()
    if confirm != "y":
        print(f"{MSG_NOTICE}Upload cancelled. Exiting.")
        return

    total = len(t_files)
    i = 0
    while i < total:
        track_fp = t_files[i]
        mix_num = start_mix + i

        cpath = None
        for cimg in cover_imgs:
            cnum = extract_number(os.path.basename(cimg))
            if cnum == mix_num:
                cpath = cimg
                break

        pub_date = published_dates[i] if i < len(published_dates) else None
        print(f"{MSG_STATUS}Uploading Track {i+1}/{total} => {track_fp}")
        result = upload_track(
            track_fp, cpath, mix_num, 
            selected_title, selected_description,
            publish_date=pub_date, remove_files=remove_after
        )

        if result is True:
            i += 1
        elif isinstance(result, dict) and "retry_after" in result:
            secs = result["retry_after"]
            print(f"{MSG_NOTICE}Rate limit => Wait {secs//60} minutes.")
            for remain in range(int(secs), 0, -60):
                time.sleep(60)
            print(f"{MSG_STATUS}Retrying upload.")
        else:
            i += 1

    print(f"{MSG_SUCCESS}All uploads completed.")