# modules/mixcloud/scheduler.py

"""
modules/mixcloud/scheduler.py

Contains the scheduling, date parsing, track scanning, 
and main uploading logic integrated with Mixcloud.
"""

import os
import sys
import glob
import pytz
import re
import csv
import time
import json
import requests
import shutil
import datetime
import threading
import webbrowser
import socketserver
import http.server

from urllib.parse import urlparse, parse_qs
from config.mixcloud.settings import (
    MIXCLOUD_DEBUG, MIXCLOUD_PRO_USER, 
    USE_EXTERNAL_TRACK_DIR, LOCAL_TRACK_DIR, EXTERNAL_TRACK_DIR, COVER_IMAGE_DIRECTORY,
    FINISHED_DIRECTORY, PUBLISHED_DATES_FILE, TITLES_FILE, UPLOAD_LINKS_FILE,
    MAX_UPLOADS, PUBLISHED_HOUR, PUBLISHED_MINUTE, TRACK_TAGS,
    PORT, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET, AUTH_URL,
    MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING, LINE_BREAK
)


ACCESS_TOKEN = None  # Will be set after OAuth


##############################
# General Helpers
##############################

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')


def extract_date_from_filename(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        date_str = match.group(1)
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None
    return None


def get_last_uploaded_date(upload_links_file):
    dates = []
    try:
        with open(upload_links_file, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    date = extract_date_from_filename(url)  # could adapt if needed
                    if date:
                        dates.append(date)
        return max(dates) if dates else None
    except FileNotFoundError:
        print(f"{MSG_WARNING}Upload links file not found: {upload_links_file}")
        return None


def get_last_uploaded_mix_number(upload_links_file):
    mix_numbers = []
    try:
        with open(upload_links_file, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    match = re.search(r'(\d+)', url)
                    if match:
                        mix_numbers.append(int(match.group(1)))
        return max(mix_numbers) if mix_numbers else 0
    except FileNotFoundError:
        print(f"{MSG_WARNING}Upload links file not found: {upload_links_file}")
        return 0


##############################
# Directory / Track Discovery
##############################

def traverse_external_directory(start_date, max_uploads):
    track_files = []
    for root, dirs, files in os.walk(EXTERNAL_TRACK_DIR):
        for file in files:
            if file.startswith("._"):
                continue
            if file.lower().endswith(('.mp3', '.m4a')):
                date_obj = extract_date_from_filename(file)
                if date_obj and (start_date is None or date_obj > start_date):
                    track_files.append((os.path.join(root, file), date_obj))
    sorted_tracks = sorted(track_files, key=lambda x: x[1])
    return [file for file, dt in sorted_tracks][:max_uploads]


def sort_tracks_by_date(files):
    files_with_dates = []
    for f in files:
        date_obj = extract_date_from_filename(os.path.basename(f))
        if date_obj:
            files_with_dates.append((f, date_obj))
        else:
            files_with_dates.append((f, datetime.datetime.max))
    sorted_files = [fp for fp, dt in sorted(files_with_dates, key=lambda x: x[1])]
    return sorted_files


def sort_cover_images_by_mix_number(files):
    files_with_numbers = []
    for f in files:
        number = extract_number(os.path.basename(f))
        files_with_numbers.append((f, number))
    sorted_files = [fp for fp, num in sorted(files_with_numbers, key=lambda x: x[1])]
    return sorted_files


##############################
# OAuth Flow
##############################

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global ACCESS_TOKEN
        query_components = parse_qs(urlparse(self.path).query)
        auth_code = query_components.get("code", [""])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        response_content = """
        <html>
        <head><title>Authorization Successful</title></head>
        <body style="margin:0; background:linear-gradient(135deg,#6a11cb 0%,#2575fc 100%);">
        <div style="text-align:center;color:#fff;padding-top:20vh;font-family:sans-serif;">
        <h1>Authorization Successful</h1>
        <p>You can now close this window.</p>
        </div>
        </body>
        </html>
        """
        self.wfile.write(response_content.encode("utf-8"))

        if auth_code:
            print(f"{MSG_STATUS}Authorization code received.")
            ACCESS_TOKEN = get_access_token(auth_code)
            threading.Thread(target=shutdown_server, args=(self.server,)).start()


def get_access_token(auth_code):
    token_url = "https://www.mixcloud.com/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=payload)
    if response.ok:
        access_token = response.json().get("access_token")
        print(f"{MSG_SUCCESS}Access token obtained.")
        return access_token
    else:
        print(f"{MSG_ERROR}Error obtaining access token: {response.text}")
        return None


def shutdown_server(server):
    server.shutdown()


def start_oauth_server():
    with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
        print(f"{MSG_STATUS}Starting OAuth server at http://localhost:{PORT}/")
        webbrowser.open(AUTH_URL)
        httpd.serve_forever()


##############################
# Title Descriptions, Dates
##############################

def parse_published_dates(published_dates_file):
    results = []
    try:
        with open(published_dates_file, 'r') as f:
            for line in f:
                line = line.strip()
                try:
                    date_obj = datetime.datetime.strptime(line, '%Y-%m-%d')
                    date_obj = date_obj.replace(hour=PUBLISHED_HOUR, minute=PUBLISHED_MINUTE)
                    eastern = pytz.timezone('US/Eastern')
                    local_dt = eastern.localize(date_obj)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    results.append(utc_dt.strftime('%Y-%m-%dT%H:%M:%SZ'))
                except ValueError:
                    print(f"{MSG_WARNING}Invalid date in {published_dates_file}: {line}")
        return results
    except FileNotFoundError:
        print(f"{MSG_ERROR}Published dates file not found: {published_dates_file}")
        return []


def load_titles_descriptions(titles_file):
    titles = []
    try:
        with open(titles_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                titles.append({'title': row['title'], 'description': row['description']})
        return titles
    except Exception as e:
        print(f"{MSG_ERROR}Error reading titles file: {e}")
        return []


def display_upload_info(track_files, cover_image_files, published_dates, starting_mix_number, selected_title):
    print(f"{MSG_STATUS}Upload Information:")
    for i, track_path in enumerate(track_files):
        expected_mix_number = starting_mix_number + i
        cover_path = None
        for cimg in cover_image_files:
            cnum = extract_number(os.path.basename(cimg))
            if cnum == expected_mix_number:
                cover_path = cimg
                break
        if not cover_path:
            cover_path = "No cover image"

        publish_date = published_dates[i] if i < len(published_dates) else "No publish date"
        date_obj = extract_date_from_filename(os.path.basename(track_path))
        if date_obj:
            date_str = date_obj.strftime('%Y-%m-%d')
            track_name = f"{selected_title} #{expected_mix_number} | {date_str}"
        else:
            track_name = f"{selected_title} #{expected_mix_number}"

        print(f"{MSG_NOTICE}Track {i+1}:")
        print(f"{MSG_NOTICE}  File: {track_path}")
        print(f"{MSG_NOTICE}  Cover: {cover_path}")
        print(f"{MSG_NOTICE}  Name: {track_name}")
        print(f"{MSG_NOTICE}  Publish Date: {publish_date}")
        print("------")


##############################
# Actual Upload
##############################

def remove_first_line(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        if lines:
            with open(file_path, 'w') as f:
                f.writelines(lines[1:])
            if MIXCLOUD_DEBUG:
                print(f"{MSG_DEBUG}Removed first line from {file_path}.")
        else:
            print(f"{MSG_WARNING}{file_path} is empty, no lines to remove.")
    except Exception as e:
        print(f"{MSG_ERROR}Error removing first line from {file_path}: {e}")


def move_to_finished(track_path, cover_path, finished_dir):
    try:
        shutil.move(track_path, os.path.join(finished_dir, os.path.basename(track_path)))
        if cover_path and os.path.exists(cover_path):
            shutil.move(cover_path, os.path.join(finished_dir, os.path.basename(cover_path)))
    except Exception as e:
        print(f"{MSG_ERROR}Error moving files to finished directory: {e}")


def upload_track(
    file_path, cover_path, mix_number, title, description, 
    publish_date=None, remove_files=True
):
    # Build track name
    date_obj = extract_date_from_filename(os.path.basename(file_path))
    if date_obj:
        track_name = f"{title} #{mix_number} | {date_obj.strftime('%Y-%m-%d')}"
    else:
        track_name = f"{title} #{mix_number}"

    upload_url = "https://api.mixcloud.com/upload/"
    data = {
        "name": track_name,
        "description": description
    }
    for idx, tag in enumerate(TRACK_TAGS):
        data[f"tags-{idx}-tag"] = tag
        if idx >= 4:
            break

    if MIXCLOUD_PRO_USER and publish_date:
        data["publish_date"] = publish_date

    files = {"mp3": open(file_path, "rb")}
    if cover_path and os.path.exists(cover_path):
        files["picture"] = open(cover_path, "rb")

    if MIXCLOUD_DEBUG:
        print(f"{MSG_DEBUG}Track Name: {track_name}")
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
            if not MIXCLOUD_DEBUG and remove_files:
                move_to_finished(file_path, cover_path, FINISHED_DIRECTORY)

            remove_first_line(PUBLISHED_DATES_FILE)

            resp_data = resp.json()
            upload_key = resp_data.get("result", {}).get("key", "")
            if upload_key:
                up_link = f"https://www.mixcloud.com{upload_key}"
                with open(UPLOAD_LINKS_FILE, 'a') as f:
                    f.write(f"{up_link}\n")

            print(f"{MSG_SUCCESS}Response Code: {resp.status_code}")
            print(f"{MSG_SUCCESS}Response Text:\n{resp.text}")
            return True
        else:
            print(f"{MSG_ERROR}Error uploading {file_path}: {resp.status_code}\n{resp.text}")
            if resp.status_code == 403:
                err_info = resp.json()
                e_type = err_info.get("error", {}).get("type", "")
                if e_type == "RateLimitException":
                    retry_after = err_info.get("error", {}).get("retry_after", 0)
                    wait_mins = (retry_after // 60) + 1
                    print(f"{MSG_NOTICE}Rate limit reached. Waiting {wait_mins} minutes.")
                    return {"retry_after": wait_mins * 60}
            return False
    except Exception as e:
        print(f"{MSG_ERROR}Exception during upload: {e}")
        return False
    finally:
        files["mp3"].close()
        if "picture" in files:
            files["picture"].close()


##############################
# Main Execution
##############################

def run_mixcloud_upload():
    global ACCESS_TOKEN

    # 1) Start OAuth server in a thread
    server_thread = threading.Thread(target=start_oauth_server)
    server_thread.start()

    # 2) Wait for token
    while ACCESS_TOKEN is None:
        time.sleep(1)

    # 3) Load titles
    titles_list = load_titles_descriptions(TITLES_FILE)
    if not titles_list:
        print(f"{MSG_ERROR}No titles found. Exiting.")
        sys.exit(1)

    print(f"{MSG_STATUS}Available Titles:")
    for i, item in enumerate(titles_list):
        print(f"{i+1}. {item['title']}")

    while True:
        try:
            choice = int(input(f"{MSG_NOTICE}Select a title to use: "))
            if 1 <= choice <= len(titles_list):
                selected_title = titles_list[choice-1]['title']
                selected_description = titles_list[choice-1]['description']
                break
            else:
                print(f"{MSG_WARNING}Invalid selection.")
        except ValueError:
            print(f"{MSG_WARNING}Please enter a valid number.")

    # 4) Last uploaded info
    last_mix_number = get_last_uploaded_mix_number(UPLOAD_LINKS_FILE)
    next_mix_number = last_mix_number + 1
    print(f"{MSG_STATUS}Last uploaded mix #: {last_mix_number}")
    print(f"{MSG_STATUS}Expected next mix #: {next_mix_number}")

    last_date = get_last_uploaded_date(UPLOAD_LINKS_FILE)
    print(f"{MSG_STATUS}Last uploaded date: {last_date.strftime('%Y-%m-%d') if last_date else 'None'}")

    start_mix_number = next_mix_number

    # 5) Covers
    cover_images = sort_cover_images_by_mix_number(
        glob.glob(os.path.join(COVER_IMAGE_DIRECTORY, "*.png")) + 
        glob.glob(os.path.join(COVER_IMAGE_DIRECTORY, "*.jpg"))
    )

    # 6) Published dates
    published_dates = parse_published_dates(PUBLISHED_DATES_FILE)

    # 7) Track discovery
    if USE_EXTERNAL_TRACK_DIR:
        track_files = traverse_external_directory(last_date, 1000)
        remove_files_after_upload = False
    else:
        track_files = sort_tracks_by_date(
            glob.glob(os.path.join(LOCAL_TRACK_DIR, "*.mp3")) + 
            glob.glob(os.path.join(LOCAL_TRACK_DIR, "*.m4a"))
        )
        remove_files_after_upload = True

    if not track_files:
        print(f"{MSG_WARNING}No new tracks found.")
        sys.exit(0)

    print(f"{MSG_STATUS}{len(track_files)} tracks available.")
    default_limit = min(MAX_UPLOADS, len(track_files))
    try:
        user_inp = input(f"{MSG_NOTICE}How many to upload? (Default: {default_limit}): ")
        if not user_inp.strip():
            num_tracks = default_limit
        else:
            num_tracks = int(user_inp)
            if num_tracks > len(track_files):
                num_tracks = len(track_files)
    except ValueError:
        print(f"{MSG_WARNING}Invalid input. Using default {default_limit}.")
        num_tracks = default_limit

    track_files = track_files[:num_tracks]

    # 8) Display info
    display_upload_info(track_files, cover_images, published_dates, start_mix_number, selected_title)
    confirm = input(f"{MSG_WARNING}Confirm upload of {num_tracks} tracks? (y/n): ")
    if confirm.lower() != 'y':
        print(f"{MSG_NOTICE}Upload cancelled.")
        return

    # 9) Upload loop
    total = len(track_files)
    i = 0
    while i < total:
        track_file = track_files[i]
        mix_number = start_mix_number + i

        # Match cover
        cpath = None
        for cov in cover_images:
            cnum = extract_number(os.path.basename(cov))
            if cnum == mix_number:
                cpath = cov
                break

        pub_date = published_dates[i] if i < len(published_dates) else None

        print(f"{MSG_STATUS}Uploading track {i+1}/{total}")
        result = upload_track(
            track_file, cpath, mix_number,
            selected_title, selected_description,
            publish_date=pub_date,
            remove_files=remove_files_after_upload
        )
        if result is True:
            i += 1
        elif isinstance(result, dict) and "retry_after" in result:
            # Rate limit
            secs = result["retry_after"]
            print(f"{MSG_NOTICE}Waiting {secs//60} mins to retry.")
            for remaining in range(int(secs), 0, -60):
                time.sleep(60)
            print(f"{MSG_STATUS}Retrying upload.")
        else:
            i += 1

    print(f"{MSG_SUCCESS}All uploads completed.")