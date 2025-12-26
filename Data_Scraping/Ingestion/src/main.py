import json
import sys
import os

# Dynamically add ../Scraper to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
scraper_dir = os.path.abspath(os.path.join(current_dir, '..', 'Scraper'))
sys.path.append(scraper_dir)

import employee # Now correctly importing employee.py from Scraper/
import book
import employee_GD
unit_test_dir = os.path.abspath(os.path.join(current_dir, '..', 'Unit Test'))
sys.path.append(unit_test_dir)
import unit_test
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the processor folder path (Processing/Processor)
processor_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'Processing', 'Processor'))
sys.path.append(processor_dir)

import datamapping
import datamapping_process



def load_config(file_name="run_scraper.json"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, "r") as file:
        return json.load(file)


def main():
    scraper_id = input("Enter scraper ID: ").strip()
    config = load_config()

    if scraper_id not in config:
        print(f"[Error] Scraper ID '{scraper_id}' not found in config.")
        return

    scraper_info = config[scraper_id]
    scraper_type = scraper_info["type"]
    url = scraper_info["url"]

    if scraper_type == "book":
        book_data = book.scrape()
        if book_data:
            import pandas as pd
            df = pd.DataFrame(book_data)
            df.to_csv("books_data.csv", index=False)
            print(f"[Main] Saved {len(df)} book records to books_data.csv")
            unit_test.run_tests("book")
        else:
            print("[Main] No book data scraped.")
        # Call book scraper logic here if needed
    elif scraper_type == "employee":
        print("[Main] Running employee scraper...")
        success = employee.scrape_employee_data()
        if success:
            unit_test.run_tests("employee")
        else:
            print("[Main] No employee data fetched.")
    elif scraper_type == "employee_GD":
        print("[Main] Running employee_GD scraper...")
        employee_GD.run_employee_gd_scraper()
        unit_test.run_tests("employee_GD")
    elif scraper_type == "data_mapping":
    
        raw_df, ref_df = datamapping.read_raw_and_reference()
        success = datamapping_process.filter_and_map_data(raw_df, ref_df)
        if not success:
            print("[Main] Data mapping failed.")

    else:
        print(f"[Error] Unknown scraper type: {scraper_type}")

if __name__ == "__main__":
    main()
