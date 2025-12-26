import os
import json
import pandas as pd

def process_employee_json(filepath="employee_data.json"):
    print("[Employee Process] Starting processing...")

    # Step 1: Check file exists
    if not os.path.exists(filepath):
        print(f"[Error] File not found: {filepath}")
        return None

    # Step 2: Load JSON with error handling
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Error] Failed to read JSON: {e}")
        return None

    try:
        df = pd.DataFrame(data)

        # Step 3: Designation assignment
        def assign_designation(years):
            if years < 3:
                return "System Engineer"
            elif 3 <= years <= 5:
                return "Data Engineer"
            elif 5 < years <= 10:
                return "Senior Data Engineer"
            else:
                return "Lead"

        df["designation"] = df["years_of_experience"].apply(assign_designation)

        # Step 4: Combine first and last name
        df["Full Name"] = df["first_name"] + " " + df["last_name"]

        # Step 5: Normalize phone numbers
        df["phone"] = df["phone"].apply(lambda x: "Invalid Number" if "x" in str(x) else x)

        # Step 6: Convert data types
        dtype_map = {
            "Full Name": str,
            "email": str,
            "phone": str,
            "gender": str,
            "age": int,
            "job_title": str,
            "years_of_experience": int,
            "salary": int,
            "department": str,
        }

        for col, dtype in dtype_map.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        print("[Employee Process] Data normalization complete.")
        return df

    except Exception as e:
        print(f"[Error] Processing failed: {e}")
        return None
