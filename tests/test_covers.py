# tests/test_covers.py

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from io import BytesIO

from mutagen.id3 import ID3
from mutagen.mp3 import MP3

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from core.cover_utils import (
    has_embedded_cover,
    download_crop_and_attach_cover,
    attach_cover_to_mp3,
    crop_image_to_square,
    image_to_jpeg_bytes,
    fetch_album_cover
)

################################################
# 1) Test has_embedded_cover
################################################

@patch("core.cover_utils.MP3")
def test_has_embedded_cover_no_apic(mock_mp3, tmp_path):
    """
    Ensure has_embedded_cover returns False if there's no APIC tag.
    """
    # Mock MP3 object without APIC
    mock_audio = MagicMock()
    mock_audio.tags.getall.return_value = []
    mock_mp3.return_value = mock_audio

    # Path doesn't matter due to mocking
    mp3_path = tmp_path / "test_no_cover.mp3"

    # Confirm there's no embedded cover
    assert not has_embedded_cover(str(mp3_path))

################################################
# 2) Test attach_cover_to_mp3
################################################

@patch("core.cover_utils.MP3")
def test_attach_cover_to_mp3(mock_mp3, tmp_path):
    """
    Test embedding a simple JPEG byte string in an MP3 file.
    """
    # Mock MP3 object with ID3 tags
    mock_audio = MagicMock()
    mock_audio.tags = MagicMock()
    mock_mp3.return_value = mock_audio

    # Create a small JPEG in memory
    img = Image.new("RGB", (100, 100), color="red")
    cover_bytes = image_to_jpeg_bytes(img)

    # Path doesn't matter due to mocking
    mp3_path = tmp_path / "test_embed_cover.mp3"

    # Attach the cover
    attach_cover_to_mp3(str(mp3_path), cover_bytes)

    # Verify the cover was embedded
    mock_audio.tags.delall.assert_called_with('APIC')
    mock_audio.tags.add.assert_called_once()
    mock_audio.save.assert_called_once()

################################################
# 3) Test crop_image_to_square
################################################

def test_crop_image_to_square():
    """
    Ensure crop_image_to_square outputs a square image in JPEG bytes.
    """
    # Create a rectangular PIL image
    img = Image.new("RGB", (300, 150), color="green")

    # Crop & convert to JPEG bytes
    out_bytes = crop_image_to_square(img)
    assert isinstance(out_bytes, bytes), "Should return raw bytes."

    # Ensure the final is square
    out_img = Image.open(BytesIO(out_bytes))
    assert out_img.width == out_img.height, "Cropped output must be square."

################################################
# 4) Test download_crop_and_attach_cover
################################################

@patch("core.cover_utils.requests.get")
@patch("core.cover_utils.MP3")
def test_download_crop_and_attach_cover(mock_mp3, mock_get, tmp_path):
    """
    Tests the pipeline:
      1) Download an image
      2) Crop it
      3) Embed in MP3
    """
    # Mock MP3 object with ID3 tags
    mock_audio = MagicMock()
    mock_audio.tags = MagicMock()
    mock_mp3.return_value = mock_audio

    # Create a rectangular mock image
    original_img = Image.new("RGB", (200, 100), color="blue")
    buffer = image_to_jpeg_bytes(original_img)

    # Mock the requests.get call
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = buffer
    mock_get.return_value = mock_resp

    # Path doesn't matter due to mocking
    mp3_path = tmp_path / "test_cover_embed.mp3"

    # Call download_crop_and_attach_cover
    cover_url = "http://example.com/fake_cover.jpg"
    download_crop_and_attach_cover(str(mp3_path), cover_url)

    # Validate that the MP3 now has a cover
    mock_audio.tags.add.assert_called_once()
    mock_audio.save.assert_called_once()

################################################
# 5) Test fetch_album_cover (Stub/Mock Example)
################################################

def test_fetch_album_cover_unknown_artist():
    """
    If the artist/title are 'unknown artist'/'unknown title',
    fetch_album_cover should return None.
    """
    result = fetch_album_cover("Unknown Title", "Unknown Artist")
    assert result is None, "Should return None for completely unknown track data."

@patch("core.cover_utils.lastfm_cover")
@patch("core.cover_utils.musicbrainz_cover")
@patch("core.cover_utils.spotify_cover")
@patch("core.cover_utils.deezer_cover")
def test_fetch_album_cover_order_of_calls(
    mock_deezer_cover, mock_spotify_cover, mock_mb_cover, mock_lastfm_cover
):
    """
    If lastfm_cover returns a valid URL, fetch_album_cover should return that
    without calling the others.
    """
    mock_lastfm_cover.return_value = "http://cover.example.com/lastfm.jpg"
    mock_mb_cover.return_value = None
    mock_spotify_cover.return_value = None
    mock_deezer_cover.return_value = None

    result = fetch_album_cover("Some Title", "Some Artist")
    assert result == "http://cover.example.com/lastfm.jpg"
    mock_lastfm_cover.assert_called_once()
    mock_mb_cover.assert_not_called()
    mock_spotify_cover.assert_not_called()
    mock_deezer_cover.assert_not_called()

@patch("core.cover_utils.lastfm_cover", return_value=None)
@patch("core.cover_utils.musicbrainz_cover", return_value=None)
@patch("core.cover_utils.spotify_cover", return_value=None)
@patch("core.cover_utils.deezer_cover", return_value="http://cover.example.com/deezer.jpg")
def test_fetch_album_cover_deezer(
    mock_deezer_cover, mock_spotify_cover, mock_mb_cover, mock_lastfm_cover
):
    """
    If lastfm, musicbrainz, spotify all return None, but deezer gives a URL,
    fetch_album_cover should return the Deezer URL.
    """
    result = fetch_album_cover("Another Title", "Another Artist")
    assert result == "http://cover.example.com/deezer.jpg"
    mock_deezer_cover.assert_called_once()