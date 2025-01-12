"""
cli/test_cli.py

Provides a subcommand for "test" logic. 
Here you can run internal debug checks, or script certain tests. 
"""

import subprocess
from core.color_utils import (
    MSG_STATUS, MSG_NOTICE, MSG_WARNING, MSG_ERROR, MSG_SUCCESS
)


def handle_test_subcommand(args):
    """
    Called when the user runs:
        python cli/main.py test
    or:
        python cli/main.py test --mixcloud
    """
    print(f"{MSG_STATUS}Starting tests...")

    if args.mixcloud:
        # Run only Mixcloud-specific tests
        handle_mixcloud_tests()
    elif args.download:
        # Run only download-specific tests
        handle_download_tests()
    else:
        # Run all tests
        print(f"{MSG_NOTICE}No specific flag provided. Running all available tests...")
        run_all_tests()

    print(f"{MSG_SUCCESS}Test subcommand completed.")


def handle_mixcloud_tests():
    """
    Runs Mixcloud-specific tests.
    """
    print(f"{MSG_STATUS}Running Mixcloud tests: tests/test_mixcloud.py")
    try:
        result = subprocess.run(["pytest", "tests/test_mixcloud.py"], check=False)
        if result.returncode == 0:
            print(f"{MSG_SUCCESS}Mixcloud tests passed.")
        else:
            print(f"{MSG_ERROR}Mixcloud tests encountered failures. Return code: {result.returncode}")
    except FileNotFoundError:
        print(f"{MSG_ERROR}Pytest not found. Please install it or adjust the command.")
    print(f"{MSG_SUCCESS}Mixcloud tests completed.")

def handle_download_tests():
    """
    Runs download-specific tests.
    """
    print(f"{MSG_STATUS}Running download tests: tests/test_download.py")
    try:
        result = subprocess.run(["pytest", "tests/test_download.py"], check=False)
        if result.returncode == 0:
            print(f"{MSG_SUCCESS}Download tests passed.")
        else:
            print(f"{MSG_ERROR}Download tests encountered failures. Return code: {result.returncode}")
    except FileNotFoundError:
        print(f"{MSG_ERROR}Pytest not found. Please install it or adjust the command.")
    print(f"{MSG_SUCCESS}Download tests completed.")


import subprocess
import os
from core.color_utils import (
    MSG_ERROR, MSG_SUCCESS, MSG_STATUS
)

def run_all_tests():
    """
    Runs all available tests in the `tests/` folder using Pytest.
    Uses an absolute path to avoid 'file or directory not found' issues.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    tests_path = os.path.join(project_root, "tests")

    print(f"{MSG_STATUS}Running all tests from: {tests_path}")

    if not os.path.isdir(tests_path):
        print(f"{MSG_ERROR}Tests directory not found at '{tests_path}'. Aborting.")
        return

    try:
        result = subprocess.run(["pytest", tests_path], check=False)
        if result.returncode == 0:
            print(f"{MSG_SUCCESS}All tests passed.")
        else:
            print(f"{MSG_ERROR}Some tests encountered failures. Return code: {result.returncode}")
    except FileNotFoundError:
        # Pytest might not be installed or not on PATH
        print(f"{MSG_ERROR}Pytest not found. Please install it or adjust the command.")
    except Exception as e:
        print(f"{MSG_ERROR}Unexpected error running tests: {str(e)}")

    print(f"{MSG_SUCCESS}All tests completed.")