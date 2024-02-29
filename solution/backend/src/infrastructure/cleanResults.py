import os
import glob
from typing import NoReturn


def clean() -> NoReturn:
    """
    Removes all JSON files from the results directory.

    This function is designed to clean up the results directory by deleting
    all JSON files it contains. It iterates through all JSON files in the
    specified
    directory and attempts to remove each. If an error occurs during file
    deletion,
    it catches the exception and prints an error message.

    Returns:
        NoReturn: This function does not return anything.
    """
    # Define the path to the results directory
    results_dir = './results'

    # Construct the pattern to match all JSON files in the directory
    pattern = os.path.join(results_dir, '*.json')

    # Use glob to find all files matching the pattern
    json_files = glob.glob(pattern)

    # Iterate over the list of file paths & remove each file
    for file_path in json_files:
        try:
            os.remove(file_path)
            print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
