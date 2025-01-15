# tests/test_mixcloud.py

"""
tests/test_mixcloud.py

Tests for the Mixcloud uploading module (modules/mixcloud/uploader.py).
Covers:
- Checking API key presence
- Sorting cover images/tracks
- Date parsing and last track number
- Finished directory usage
- OAuth flow mock
- Fake upload with mock requests
"""

import os
import sys
import pytest
import shutil
import tempfile
import requests
import datetime
import threading
import time
from unittest.mock import patch, MagicMock

# Ensure the project root is in sys.path (optional if you run from project root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from config.settings import APIS, COVER_IMAGE_DIRECTORY, FINISHED_DIRECTORY, MIXCLOUD_CLIENT_ID
from modules.mixcloud.uploader import (
    extract_number,
    extract_date_from_filename,
    parse_published_dates_from_file,
    get_last_uploaded_mix_number,
    get_last_uploaded_date,
    sort_cover_images_by_mix_number,
    sort_tracks_by_date,
    traverse_external_directory,
    move_to_finished,
    upload_track,
    start_oauth_server
)
from core.color_utils import MSG_ERROR, MSG_NOTICE, MSG_DEBUG, MSG_SUCCESS, MSG_STATUS, MSG_WARNING


# -----------------------------------------------------------------------------
# 1) TEST API KEY CONNECTION
# -----------------------------------------------------------------------------
# def test_api_key_presence():
#     """
#     Verifies that Mixcloud credentials exist in APIS dict and settings.
#     """
#     assert APIS["mixcloud"]["client_id"] != "", "Mixcloud client_id is missing."
#     assert APIS["mixcloud"]["client_secret"] != "", "Mixcloud client_secret is missing."
#     assert MIXCLOUD_CLIENT_ID != "", "MIXCLOUD_CLIENT_ID from settings.py is missing."


# -----------------------------------------------------------------------------
# 2) TEST IMAGE SORTING
# -----------------------------------------------------------------------------
def test_sort_cover_images_by_mix_number():
    """
    Ensures we correctly sort cover images by the first integer found in filename.
    """
    files = [
        "/path/to/cover_2.jpg",
        "/path/to/cover_10.png",
        "/path/to/cover_1.jpg",
        "/path/to/cover_3.jpg"
    ]
    result = sort_cover_images_by_mix_number(files)
    # Expect: cover_1, cover_2, cover_3, cover_10
    expected = [
        "/path/to/cover_1.jpg",
        "/path/to/cover_2.jpg",
        "/path/to/cover_3.jpg",
        "/path/to/cover_10.png"
    ]
    assert result == expected, f"Expected {expected}, got {result}"


# -----------------------------------------------------------------------------
# 3) TEST TRACK SORTING
# -----------------------------------------------------------------------------
def test_sort_tracks_by_date():
    """
    Ensures track files are sorted by date gleaned from filenames.
    """
    files = [
        "/music/2023-08-10_something.mp3",
        "/music/2023-01-05_other.m4a",
        "/music/2024-01-01_new.mp3",
        "/music/no-date.mp3"
    ]
    sorted_result = sort_tracks_by_date(files)
    # Chronological order, ignoring any no-date => goes last
    assert sorted_result[0].endswith("2023-01-05_other.m4a")
    assert sorted_result[1].endswith("2023-08-10_something.mp3")
    assert sorted_result[2].endswith("2024-01-01_new.mp3")
    assert sorted_result[3].endswith("no-date.mp3")


# -----------------------------------------------------------------------------
# 4) TEST DATE PARSING & LAST TRACK NUMBER
# -----------------------------------------------------------------------------
def test_extract_date_from_filename():
    """
    Basic check of date extraction from 'YYYY-MM-DD' in filename.
    """
    dt = extract_date_from_filename("2025-12-31_mix.mp3")
    assert dt is not None
    assert dt.year == 2025
    assert dt.month == 12
    assert dt.day == 31


def test_get_last_uploaded_mix_number(tmp_path):
    """
    Ensure we get the max integer from lines in a mock uploadLinks.txt.
    """
    fake_file = tmp_path / "uploadLinks.txt"
    fake_file.write_text(
        "https://www.mixcloud.com/.../mix1-2024-01-01\n"
        "https://www.mixcloud.com/.../mix3-2025-03-05\n"
        "https://www.mixcloud.com/.../mix2-2024-12-31\n"
    )
    num = get_last_uploaded_mix_number(str(fake_file))
    assert num == 3, f"Expected last mix number=3, got={num}"


def test_get_last_uploaded_date(tmp_path):
    """
    Ensure we find the latest date from lines in uploadLinks.txt.
    """
    fake_file = tmp_path / "uploadLinks.txt"
    fake_file.write_text(
        "https://www.mixcloud.com/.../my-set-2023-06-10\n"
        "https://www.mixcloud.com/.../my-set-2024-01-01\n"
        "https://www.mixcloud.com/.../my-set-2022-12-31\n"
    )
    dt = get_last_uploaded_date(str(fake_file))
    assert dt.year == 2024 and dt.month == 1 and dt.day == 1, f"Wrong date => {dt}"


# -----------------------------------------------------------------------------
# 5) TEST FINISHED DIRECTORY
# -----------------------------------------------------------------------------
# def test_move_to_finished(tmp_path):
#     """
#     Checks that move_to_finished properly relocates files to a 'finished' dir.
#     """
#     # Create a fake file & cover
#     audio_file = tmp_path / "test_track.mp3"
#     cover_file = tmp_path / "cover.jpg"
#     audio_file.write_text("audio data")
#     cover_file.write_text("cover data")

#     # Make a mock 'finished' folder
#     finished_dir = tmp_path / "finished"
#     finished_dir.mkdir()

#     move_to_finished(str(audio_file), str(cover_file), str(finished_dir))

#     assert not audio_file.exists(), "Audio file wasn't moved."
#     assert not cover_file.exists(), "Cover file wasn't moved."

#     assert (finished_dir / "test_track.mp3").exists(), "Audio not in finished dir."
#     assert (finished_dir / "cover.jpg").exists(), "Cover not in finished dir."


# -----------------------------------------------------------------------------
# 6) TEST PUBLISHED DATES
# -----------------------------------------------------------------------------
def test_parse_published_dates_from_file(tmp_path):
    """
    Validate we parse and convert local times to UTC strings.
    """
    sample_file = tmp_path / "dates.txt"
    sample_file.write_text("2024-01-01\n2023-12-31\nInvalidDate\n")
    dates = parse_published_dates_from_file(str(sample_file))
    # We expect 2 valid, 1 invalid
    assert len(dates) == 2, f"Expected 2 valid dates, got={len(dates)}"


# -----------------------------------------------------------------------------
# 7) TEST OAUTH WORKS (Mocking)
# -----------------------------------------------------------------------------
@patch("modules.mixcloud.uploader.webbrowser.open")
@patch("modules.mixcloud.uploader.socketserver.TCPServer")
def test_start_oauth_server(mock_server, mock_webopen):
    """
    Mocks start_oauth_server to confirm we attempt to open the correct URL
    and serve forever in a separate thread.
    """
    mock_instance = MagicMock()
    mock_server.return_value = mock_instance

    srv_thread = threading.Thread(target=start_oauth_server)
    srv_thread.start()
    time.sleep(0.5)  # Let it run briefly

    mock_webopen.assert_called_once()
    assert "mixcloud.com/oauth/authorize?" in mock_webopen.call_args[0][0]
    mock_instance.__enter__.return_value.serve_forever.assert_called()


# -----------------------------------------------------------------------------
# 8) TEST FAKE UPLOAD
# -----------------------------------------------------------------------------
@patch("modules.mixcloud.uploader.requests.post")
def test_fake_upload_track(mock_post, tmp_path):
    from unittest.mock import patch as patch2, MagicMock
    import modules.mixcloud.uploader as mc_upload  # Import the module, not just the name

    with patch2("modules.mixcloud.uploader.ACCESS_TOKEN", new="FAKE_TOKEN"):
        # Prepare track & cover
        track_path = tmp_path / "MyMix_2025-02-02.mp3"
        cover_path = tmp_path / "cover_1.jpg"
        track_path.write_text("fake audio data")
        cover_path.write_text("fake cover data")

        # Confirm the module’s ACCESS_TOKEN is patched
        assert mc_upload.ACCESS_TOKEN == "FAKE_TOKEN", "ACCESS_TOKEN patch failed."

        # Mock requests.post
        mock_resp = MagicMock(ok=True, status_code=200, text="Success", json=lambda: {"result": {"key": "/fakekey"}})
        mock_post.return_value = mock_resp

        result = mc_upload.upload_track(
            file_path=str(track_path),
            cover_path=str(cover_path),
            mix_number=1,
            title="Test Title",
            description="Test Desc",
            publish_date="2025-02-02T12:00:00Z",
            remove_files=False
        )
        assert result is True, "Expected upload success"

        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert kwargs["params"].get("access_token") == "FAKE_TOKEN"

        data_sent = kwargs["data"]
        assert data_sent["name"].startswith("Test Title #1 | 2025-02-02")
        assert data_sent["description"] == "Test Desc"
        assert data_sent["publish_date"] == "2025-02-02T12:00:00Z"