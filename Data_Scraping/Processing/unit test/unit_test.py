import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import json
import os

MOCK_BOOK_DATA = pd.DataFrame({
    "Title": ["Book A"],
    "Price": ["$10"],
    "Rating": [4],
    "Availability": ["In stock"],
    "Product URL": ["http://example.com/book"]
})

MOCK_EMPLOYEE_JSON = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone": "1234567890",
        "job_title": "Engineer"
    }
]

MOCK_EMPLOYEE_GD_DATA = pd.DataFrame({
    "user_id": [1],
    "first_name": ["Alice"],
    "last_name": ["Smith"],
    "email": ["alice@example.com"],
    "job_title": ["Engineer"],
    "phone": ["1234567890"],
    "date_of_birth": ["1990-01-01"]
})


class TestBookProcessing(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_csv", return_value=MOCK_BOOK_DATA)
    def test_03_csv_file_extraction(self, mock_read_csv, mock_exists):
        self.assertTrue(os.path.exists("books_data.csv"))

    @patch("pandas.read_csv", return_value=MOCK_BOOK_DATA)
    def test_04_data_structure(self, mock_read_csv):
        df = pd.read_csv("books_data.csv")
        required_cols = {"Title", "Price", "Rating", "Availability", "Product URL"}
        self.assertTrue(required_cols.issubset(set(df.columns)))

    @patch("pandas.read_csv", return_value=MOCK_BOOK_DATA)
    def test_05_handle_missing_or_invalid_data(self, mock_read_csv):
        df = pd.read_csv("books_data.csv")
        self.assertFalse(df.isnull().all().any())


class TestEmployeeProcessing(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(MOCK_EMPLOYEE_JSON))
    @patch("os.path.exists", return_value=True)
    def test_03_json_file_extraction(self, mock_exists, mock_file):
        self.assertTrue(os.path.exists("employee_data.json"))
        data = json.load(mock_file())
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(MOCK_EMPLOYEE_JSON))
    def test_04_data_structure(self, mock_file):
        data = json.load(mock_file())
        df = pd.DataFrame(data)
        expected_cols = {"first_name", "last_name", "email", "phone", "job_title"}
        self.assertTrue(expected_cols.issubset(set(df.columns)))

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(MOCK_EMPLOYEE_JSON))
    def test_05_handle_missing_or_invalid_data(self, mock_file):
        data = json.load(mock_file())
        df = pd.DataFrame(data)
        self.assertFalse(df.isnull().all().any())


class TestEmployeeGDProcessing(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_csv", return_value=MOCK_EMPLOYEE_GD_DATA)
    def test_03_csv_file_extraction(self, mock_read_csv, mock_exists):
        self.assertTrue(os.path.exists("employee_data.csv"))

    @patch("pandas.read_csv", return_value=MOCK_EMPLOYEE_GD_DATA)
    def test_04_data_structure(self, mock_read_csv):
        df = pd.read_csv("employee_data.csv")
        required_cols = {"user_id", "first_name", "last_name", "email", "job_title", "phone", "date_of_birth"}
        self.assertTrue(required_cols.issubset(set(df.columns)))

    @patch("pandas.read_csv", return_value=MOCK_EMPLOYEE_GD_DATA)
    def test_05_handle_missing_or_invalid_data(self, mock_read_csv):
        df = pd.read_csv("employee_data.csv")
        self.assertFalse(df.isnull().all().any())


# Run selective tests based on scraper type
def run_tests(scraper_type):
    suite = unittest.TestSuite()

    if scraper_type == "book":
        suite.addTests([
            TestBookProcessing('test_03_csv_file_extraction'),
            TestBookProcessing('test_04_data_structure'),
            TestBookProcessing('test_05_handle_missing_or_invalid_data')
        ])
    elif scraper_type == "employee":
        suite.addTests([
            TestEmployeeProcessing('test_03_json_file_extraction'),
            TestEmployeeProcessing('test_04_data_structure'),
            TestEmployeeProcessing('test_05_handle_missing_or_invalid_data')
        ])
    elif scraper_type == "employee_GD":
        suite.addTests([
            TestEmployeeGDProcessing('test_03_csv_file_extraction'),
            TestEmployeeGDProcessing('test_04_data_structure'),
            TestEmployeeGDProcessing('test_05_handle_missing_or_invalid_data')
        ])
    else:
        print(f"[Test] No test suite for '{scraper_type}'")
        return

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    run_tests("book")
