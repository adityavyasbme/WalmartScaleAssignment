import unittest
from src.infrastructure.dataLoader import load_csv_data
import pandas as pd
import os


class TestDataLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a temporary CSV file for testing."""
        cls.test_file = "test_data.csv"
        test_data = pd.DataFrame({
            'column1': [1, 2, 3],
            'column2': ['a', 'b', 'c']
        })
        test_data.to_csv(cls.test_file, index=False)

    @classmethod
    def tearDownClass(cls):
        """Clean up the temporary file after tests."""
        os.remove(cls.test_file)

    def test_load_csv_data_success(self):
        """Test that data is successfully loaded from a valid CSV file."""
        data = load_csv_data(self.test_file)
        self.assertIsInstance(data, pd.DataFrame)
        # Expecting 3 rows of data
        self.assertEqual(len(data), 3)  # type: ignore

    def test_load_csv_data_file_not_found(self):
        """Test the response when the CSV file does not exist."""
        data = load_csv_data("non_existent_file.csv")
        self.assertIsNone(data)
