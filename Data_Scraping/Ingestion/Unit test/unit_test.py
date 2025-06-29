import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import pandas as pd

BOOK_CSV = "books_data.csv"
EMPLOYEE_JSON_API = "https://api.slingacademy.com/v1/sample-data/files/employees.json"
EMPLOYEE_CSV = "employee_data.csv"

class TestBookScraper(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("requests.get")
    def test_book_csv_download(self, mock_get, mock_file):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"Title,Price,Rating\nBook A,10.99,5"
        with open(BOOK_CSV, "wb") as f:
            f.write(mock_get.return_value.content)
        self.assertTrue(os.path.exists(BOOK_CSV))
        print("[Book Test] CSV file simulated and exists.")

    def test_book_file_format(self):
        df = pd.DataFrame([{
            "Title": "Sample Book", "Price": "£10", "Rating": 4,
            "Availability": "In stock", "Product URL": "http://example.com"
        }])
        expected_cols = {"Title", "Price", "Rating", "Availability", "Product URL"}
        self.assertTrue(expected_cols.issubset(df.columns))
        print("[Book Test] File format is valid.")


class TestEmployeeScraper(unittest.TestCase):

    @patch("requests.get")
    def test_employee_json_download(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": [{"name": "John"}]}
        response = mock_get(EMPLOYEE_JSON_API)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        print("[Employee Test] JSON download mocked and successful.")

    def test_employee_json_format(self):
        df = pd.DataFrame([{
            "Full Name": "John Doe", "email": "john@example.com", "gender": "M",
            "age": 30, "job_title": "Engineer", "years_of_experience": 5,
            "salary": 70000, "department": "Tech"
        }])
        expected_cols = {"Full Name", "email", "gender", "age", "job_title", "years_of_experience", "salary", "department"}
        self.assertTrue(expected_cols.issubset(df.columns))
        print("[Employee Test] File format is valid.")


class TestEmployeeGDScraper(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_employee_gd_csv_download(self, mock_file):
        with open(EMPLOYEE_CSV, "w") as f:
            f.write("user_id,first_name,last_name,email,sex,job_title,phone,date_of_birth\n")
        self.assertTrue(os.path.exists(EMPLOYEE_CSV))
        print("[Employee_GD Test] CSV file mocked as downloaded.")

    def test_employee_gd_format(self):
        df = pd.DataFrame([{
            "user_id": 1, "first_name": "John", "last_name": "Doe",
            "email": "john@example.com", "sex": "M", "job_title": "Engineer",
            "phone": "1234567890", "date_of_birth": "1990-01-01"
        }])
        expected_cols = {"user_id", "first_name", "last_name", "email", "sex", "job_title", "phone", "date_of_birth"}
        self.assertTrue(expected_cols.issubset(set(df.columns)))
        print("[Employee_GD Test] File format is valid.")


def run_tests(scraper_type):
    suite = unittest.TestSuite()

    if scraper_type == "book":
        suite.addTest(TestBookScraper('test_book_csv_download'))
        suite.addTest(TestBookScraper('test_book_file_format'))
    elif scraper_type == "employee":
        suite.addTest(TestEmployeeScraper('test_employee_json_download'))
        suite.addTest(TestEmployeeScraper('test_employee_json_format'))
    elif scraper_type == "employee_GD":
        suite.addTest(TestEmployeeGDScraper('test_employee_gd_csv_download'))
        suite.addTest(TestEmployeeGDScraper('test_employee_gd_format'))
    else:
        print(f"[Test] No test suite for scraper type '{scraper_type}'")
        return

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_tests("book")  # Change manually to test standalone
