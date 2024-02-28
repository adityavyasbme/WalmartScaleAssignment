import pandas as pd
from typing import Optional
import os


def load_csv_data(file_path: str) -> Optional[pd.DataFrame]:
    """Loads CSV data from a given file path.

    Args:
        file_path (str): The path to the CSV file to be loaded.

    Returns:
        Optional[pd.DataFrame]: The loaded data as a pandas DataFrame or None.
    """
    try:
        data = pd.read_csv(file_path)  # type: ignore
        print(f"Data loaded successfully from {file_path}")
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"""An error occurred while loading the data (CWD {os.getcwd()} 
              File Path {file_path}): {e}""")
        return None
