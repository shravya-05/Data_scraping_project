import os
import pandas as pd

def validate_and_process_book_file(filepath="books_data.csv"):
    print("[Book Process] Starting book file validation...")

    # Step 1: Check if file exists
    if not os.path.exists(filepath):
        print(f"[Error] File not found: {filepath}")
        return False

    # Step 2: Check file extension
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(filepath)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath, engine="openpyxl")  # Excel file
        else:
            print(f"[Error] Unsupported file extension: {ext}")
            return False

        if df.empty:
            print("[Error] File is empty.")
            return False

        # Step 3: Validate required columns
        expected_cols = {"Title", "Price", "Rating", "Availability", "Product URL"}
        missing = expected_cols - set(df.columns)
        if missing:
            print(f"[Error] Missing columns: {missing}")
            return False

        print(f"[Book Process] Successfully validated {len(df)} records.")
        return True

    except Exception as e:
        print(f"[Error] Failed to read file: {e}")
        return False
