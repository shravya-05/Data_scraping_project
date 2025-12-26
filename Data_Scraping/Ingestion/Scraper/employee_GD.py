import requests
import pandas as pd
import os
import mimetypes
import random


# Google Drive file direct download link
DRIVE_URL = "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"
OUTPUT_CSV = "employee_data.csv"
DOWNLOAD_PATH = "downloaded_employee_file.csv"
hire_dates = ["2018-05-10", "2019-09-15", "2020-07-20", "2021-12-01", "2022-04-30"]


# Download file from Google Drive
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: Status code {response.status_code}")
    with open(filename, "wb") as f:
        f.write(response.content)
        
    print(f"File downloaded to {filename}")

# Determine the file type (CSV or Excel)
def detect_file_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type == "text/csv":
        return "csv"
    elif mime_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        return "excel"
    else:
        raise Exception("Unsupported file type")

# Parse the file and extract relevant employee data
def parse_employee_data(filename):
    try:
        df = pd.read_csv(filename)
        print("Parsed as CSV")
    except Exception as csv_error:
        try:
            df = pd.read_excel(filename, engine='openpyxl')  # or engine='xlrd' for .xls files
            print("Parsed as Excel")
        except Exception as excel_error:
            raise Exception(
                f"Unsupported or unreadable file format.\nCSV Error: {csv_error}\nExcel Error: {excel_error}"
            )

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    expected_columns = ["user_id", "first_name", "last_name", "email", "sex", "job_title", "phone", "date_of_birth"]
    missing = [col for col in expected_columns if col not in df.columns]
    print("Missing columns:", missing)
    if missing:
        raise Exception(f"Missing required columns: {missing}")

    return df

def run_employee_gd_scraper():
    try:
        # Step 1: Download
        download_file(DRIVE_URL, DOWNLOAD_PATH)

        # Step 2: Detect file type
        file_type = detect_file_type(DOWNLOAD_PATH)
        print(f"Detected file type: {file_type}")

        # Step 3: Parse and structure data
        employee_df = parse_employee_data(DOWNLOAD_PATH)

        # Step 4: Add random hire date column
        employee_df["hire_date"] = [random.choice(hire_dates) for _ in range(len(employee_df))]

        # Step 5: Save to CSV
        employee_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Employee data saved to {OUTPUT_CSV}")

        # Optional: Cleanup
        os.remove(DOWNLOAD_PATH)

    except Exception as e:
        print(f"Error occurred: {e}")


# Only runs if called directly
if __name__ == "__main__":
    run_employee_gd_scraper()
