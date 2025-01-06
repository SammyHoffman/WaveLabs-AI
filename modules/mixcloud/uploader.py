# modules/mixcloud/uploader.py

"""
modules/mixcloud/uploader.py

Handles Mixcloud OAuth and track uploads.
Make sure your .env or config/settings.py has:
- MIXCLOUD_CLIENT_ID
- MIXCLOUD_CLIENT_SECRET

If you store them in APIS["mixcloud"], reference those keys here.
"""

import os
import requests
from config.settings import APIS
from core.color_utils import (
    MSG_STATUS, MSG_NOTICE, MSG_WARNING, MSG_ERROR, MSG_SUCCESS
)


def get_mixcloud_token():
    """
    If needed, exchange code for a token or retrieve a stored token.
    For a simpler flow, you might have the user log in once, 
    store the token, and reuse it. Placeholder logic here.
    """
    client_id = APIS["mixcloud"].get("client_id", "")
    client_secret = APIS["mixcloud"].get("client_secret", "")

    if not client_id or not client_secret:
        print(f"{MSG_WARNING}Mixcloud credentials missing. Check .env or APIS dictionary.")
        return None

    # Your real OAuth flow might be more complex, but here's a placeholder:
    # This function returns None unless you build a proper flow for Mixcloud OAuth.
    return None


def upload_to_mixcloud(file_path: str) -> bool:
    """
    Uploads the specified file_path to Mixcloud.
    Returns True if successful, False otherwise.
    """
    if not os.path.isfile(file_path):
        print(f"{MSG_ERROR}File not found => {file_path}")
        return False

    # Retrieve client info from APIS
    client_id = APIS["mixcloud"].get("client_id", "")
    client_secret = APIS["mixcloud"].get("client_secret", "")
    enabled = APIS["mixcloud"].get("enabled", False)

    if not enabled:
        print(f"{MSG_WARNING}Mixcloud is disabled in config. Cannot upload.")
        return False
    if not client_id or not client_secret:
        print(f"{MSG_ERROR}Mixcloud credentials not set. Update .env or settings.")
        return False

    print(f"{MSG_STATUS}Preparing to upload => {file_path}")

    # Placeholder upload logic. See Mixcloud API docs for real implementation:
    # https://www.mixcloud.com/developers/
    # Typically you'd do a multi-part form POST to "https://api.mixcloud.com/upload/"

    # Example stub code:
    try:
        # Suppose we have an 'ACCESS_TOKEN' from a prior OAuth flow:
        token = get_mixcloud_token()
        if not token:
            # If you need a token, handle it properly here (OAuth flow).
            # For now, pretend we have one (stub).
            token = "FAKE_ACCESS_TOKEN"

        # This is a pretend endpoint or example logic:
        upload_url = "https://api.mixcloud.com/upload/"
        # Construct form data
        data = {
            "name": "My DJ Mix",
            "description": "Automatically uploaded mix",
        }
        files = {"mp3": open(file_path, "rb")}

        # Potentially add tags, track listing, etc. per Mixcloud docs:
        # data["tags-0-tag"] = "DJ"
        # data["tags-1-tag"] = "Live Mix"

        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(upload_url, data=data, files=files, headers=headers)

        if resp.status_code == 200:
            print(f"{MSG_SUCCESS}Successfully uploaded to Mixcloud!")
            return True
        else:
            print(f"{MSG_ERROR}Mixcloud upload error => {resp.status_code} {resp.text}")
            return False

    except Exception as e:
        print(f"{MSG_ERROR}Upload exception => {str(e)}")
        return False
    finally:
        if 'files' in locals():
            files["mp3"].close()