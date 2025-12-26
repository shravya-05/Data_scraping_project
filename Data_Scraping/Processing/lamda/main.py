import os
import sys
import json

# directories
current_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.abspath(os.path.join(current_dir, '..'))
processor_dir = os.path.join(processing_dir, 'Processor')
root_dir = os.path.abspath(os.path.join(processing_dir, '..'))

# add Processor folder to path
sys.path.append(processor_dir)

# imports
import book_process
import employee_process  
import employeeGD_process

unit_test_dir = os.path.join(processing_dir, 'Unit test')
sys.path.append(unit_test_dir)

import unit_test  # test.py



# File paths
config_path = os.path.join(processing_dir, 'run_scraper.json')
books_csv_path = os.path.join(root_dir, 'books_data.csv')
employee_json_path = os.path.join(root_dir, 'employee_data.json')
employee_gd_csv_path = os.path.join(root_dir, 'employee_data.csv')  # outside Processing/


# Load config
def load_config():
    with open(config_path, "r") as f:
        return json.load(f)

# Main
def main():
    scraper_id = input("Enter scraper ID: ").strip()
    config = load_config()

    if scraper_id not in config:
        print(f"[Error] Scraper ID '{scraper_id}' not found.")
        return

    scraper_type = config[scraper_id]["type"]

    if scraper_type == "book":
        print("[Main] Processing book...")
        book_process.validate_and_process_book_file(filepath=books_csv_path)
        unit_test.run_tests("book")         # after book processing



    elif scraper_type == "employee":
        print("[Main] Processing employee data...")
        df = employee_process.process_employee_json(filepath=employee_json_path)
        


        if df is not None:
            print("[Main] Normalized employee data preview:")
            print(df.head())  # Or use df.to_string(index=False) for full display
        else:
            print("[Main] Employee processing failed.")
        unit_test.run_tests("employee")     # after employee processing    


    elif scraper_type == "employee_GD":
        print("[Main] Processing employee GD file...")
        df = employeeGD_process.process_employee_gd_file(filepath=employee_gd_csv_path)

        if df is not None:
            print("[Main] Mapped employee GD data preview:")
            print(df.head())
        else:
            print("[Main] Employee GD processing failed.")

        unit_test.run_tests("employee_GD")  # after employeeGD processing
    else:
        print(f"[Error] Unknown type: {scraper_type}")

if __name__ == "__main__":
    main()
