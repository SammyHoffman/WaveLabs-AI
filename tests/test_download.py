"""
tests/test_download.py

Tests for your downloading logic. This example shows how to mock yt-dlp 
so you don't rely on an actual network connection during tests.
"""

import os
import sys
import pytest
from unittest.mock import patch

# Ensure the project root is in the path (optional if you run from project root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.download.downloader import download_track


# @pytest.mark.skip(reason="Integration test example - update or remove skip when ready")
def test_download_track_integration(tmp_path):
    """
    Example integration test for the download function, using a mock to avoid real network calls.
    Remove @pytest.mark.skip if you want to run it.
    """

    # 1) Example link to test (this won't be fetched because we'll mock the extraction)
    test_link = "https://www.youtube.com/watch?v=o-YBDTqX_ZU"

    # 2) Create a temporary download folder for the test
    download_folder = tmp_path / "audio_320"
    download_folder.mkdir(exist_ok=True)

    # 3) Define yt-dlp options you'd normally pass to download_track
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    }

    # 4) Mock yt_dlp.YoutubeDL.extract_info to simulate download without an actual network call
    with patch("yt_dlp.YoutubeDL.extract_info") as mock_extract_info:
        # Simulate a successful download with a known file path
        mock_extract_info.return_value = {
            "title": "Test Song",
            "requested_downloads": [
                {
                    "filepath": str(download_folder / "Test Song.mp3")
                }
            ]
        }

        # 5) Call your download_track function
        downloaded_file_path, info_dict = download_track(test_link, ydl_opts)

        # 6) Assertions
        assert downloaded_file_path == str(download_folder / "Test Song.mp3")
        assert info_dict.get("title") == "Test Song", "Expected 'Test Song' in mock info."
        assert (download_folder / "Test Song.mp3").name == "Test Song.mp3"

        # You can check if the file was 'created' in memory:
        # Because we mocked extract_info, there's no real file, 
        # but you could do:
        # assert (download_folder / "Test Song.mp3").exists()

    # Additional checks can be added after you expand the real logic
    # e.g., verifying ID3 tags, metadata updates, etc.