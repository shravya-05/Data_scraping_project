import os
import pandas as pd
import mimetypes

def process_employee_gd_file(filepath="employee_data.csv"):
    print("[Employee GD Process] Starting file validation...")

    # Step 1: File existence check
    if not os.path.exists(filepath):
        print(f"[Error] File not found: {filepath}")
        return None

    # Step 2: Detect file type by extension (more reliable than MIME)
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(filepath)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath, engine="openpyxl")
        else:
            print(f"[Error] Unsupported file extension: {ext}")
            return None

        if df.empty:
            print("[Error] File is empty.")
            return None

        # Step 3: Validate required columns (field mapping)
        required_fields = {
            "user_id": "Employee ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "job_title": "Job Title",
            "phone": "Phone Number",
            "date_of_birth": "Hire Date"  # Assuming date_of_birth is used as hire date
        }

        missing_fields = [col for col in required_fields if col not in df.columns]
        if missing_fields:
            print(f"[Error] Missing columns in file: {missing_fields}")
            return None

        # Step 4: Rename columns
        df_renamed = df[list(required_fields.keys())].rename(columns=required_fields)

        print("[Employee GD Process] File successfully parsed and mapped.")
        return df_renamed

    except Exception as e:
        print(f"[Error] Failed to process file: {e}")
        return None
