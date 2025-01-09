"""
tests/test_download.py

Tests for your downloading logic. This example shows how to mock yt-dlp 
so you don't rely on an actual network connection during tests.
"""

import os
import sys
import pytest
from unittest.mock import patch

# Ensure the project root is in the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.download.downloader import download_track


def test_download_track_integration(tmp_path):
    """
    Integration test for the download function using mocks.
    """
    test_link = "https://www.youtube.com/watch?v=o-YBDTqX_ZU"
    download_folder = tmp_path / "audio_320"
    download_folder.mkdir(exist_ok=True)

    with patch("yt_dlp.YoutubeDL.extract_info") as mock_extract_info:
        mock_extract_info.return_value = {
            "title": "Test Song",
            "requested_downloads": [
                {
                    "filepath": str(download_folder / "Test Song.mp3")
                }
            ]
        }

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True

            downloaded_file_path, info_dict = download_track(test_link, str(download_folder), "320")

            assert downloaded_file_path == str(download_folder / "Test Song.mp3")
            assert info_dict.get("title") == "Test Song"
            assert (download_folder / "Test Song.mp3").name == "Test Song.mp3"