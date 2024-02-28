from src.infrastructure.dataLoader import load_csv_data
import pandas as pd


def test_load_csv_data_success(tmpdir):
    """Test that data is successfully loaded from a valid CSV file."""
    # Create a temporary CSV file
    file_path = tmpdir.join("test_data.csv")
    test_data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })
    test_data.to_csv(file_path, index=False)

    # Test loading the data
    data = load_csv_data(str(file_path))
    assert isinstance(data, pd.DataFrame), "Data should be a pandas DataFrame"
    assert len(data) == 3, "DataFrame should contain 3 rows"


def test_load_csv_data_file_not_found():
    """Test the response when the CSV file does not exist."""
    data = load_csv_data("non_existent_file.csv")
    assert data is None, "Function should return None for non-existent files"
