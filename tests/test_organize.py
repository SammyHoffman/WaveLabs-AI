# tests/test_organize_cli.py

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Adjust path so Python can import `cli.organize_cli`
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the CLI entry point
from cli.organize_cli import main as organize_main

################################################
# 1) Test when --requested is specified
################################################

@patch("cli.organize_cli.os.path.exists", return_value=True)
@patch("cli.organize_cli.os.listdir", return_value=["song1.mp3", "song2.mp3"])
@patch("cli.organize_cli.move_to_date_based_folder_requested_songs")
@patch("cli.organize_cli.print")
def test_organize_cli_requested(
    mock_print,
    mock_move_func,
    mock_listdir,
    mock_exists
):
    """
    If '--requested' is passed, it should call
    move_to_date_based_folder_requested_songs for each file.
    """
    test_argv = ["organize_cli.py", "--requested"]
    with patch.object(sys, "argv", test_argv):
        organize_main()

    # The script should print a notice about organizing requested songs
    assert any("Organizing only requested songs" in call_args[0][0] for call_args in mock_print.call_args_list)
    # Each file in the download folder should be moved with the 'requested_songs' function
    mock_move_func.assert_any_call(os.path.join("downloads", "song1.mp3"))
    mock_move_func.assert_any_call(os.path.join("downloads", "song2.mp3"))
    assert mock_move_func.call_count == 2

################################################
# 2) Test default mode (no --requested)
################################################

@patch("cli.organize_cli.os.path.exists", return_value=True)
@patch("cli.organize_cli.organize_downloads")
@patch("cli.organize_cli.print")
def test_organize_cli_default_mode(
    mock_print,
    mock_organize_downloads,
    mock_exists
):
    """
    If '--requested' is not provided, it should call `organize_downloads()`.
    """
    test_argv = ["organize_cli.py"]
    with patch.object(sys, "argv", test_argv):
        organize_main()

    # The script should print a notice about organizing all downloaded files
    assert any("Organizing all downloaded files" in call_args[0][0] for call_args in mock_print.call_args_list)
    # Should call the standard organize_downloads function
    mock_organize_downloads.assert_called_once()

################################################
# 3) Test when download folder doesn't exist
################################################

@patch("cli.organize_cli.os.path.exists", return_value=False)
@patch("cli.organize_cli.print")
def test_organize_cli_no_download_folder(
    mock_print,
    mock_exists
):
    """
    If the download folder doesn't exist, it should warn and exit.
    """
    test_argv = ["organize_cli.py"]
    with patch.object(sys, "argv", test_argv):
        organize_main()

    # Check for a warning about missing download folder
    assert any("not found" in call_args[0][0] for call_args in mock_print.call_args_list)