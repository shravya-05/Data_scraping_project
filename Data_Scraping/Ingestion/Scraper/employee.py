import requests
import json
import random  # For random hire date selection

API_URL = "https://api.slingacademy.com/v1/sample-data/files/employees.json"
OUTPUT_JSON = "employee_data.json"

hire_dates = ["2018-05-10", "2019-09-15", "2020-07-20", "2021-12-01", "2022-04-30"]

def scrape_employee_data():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            print("[Employee] Failed to fetch data. Status:", response.status_code)
            return False

        json_data = response.json()

        # If the JSON itself is a dict and employee list is nested
        if isinstance(json_data, dict) and "employees" in json_data:
            employees = json_data["employees"]
        elif isinstance(json_data, list):
            employees = json_data
        else:
            print("[Employee] Unexpected JSON format")
            return False

        # Assign a random hire date to each employee
        for emp in employees:
            emp["hire_date"] = random.choice(hire_dates)

        # Save updated data
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(employees, f, indent=2)

        print(f"[Employee] JSON data saved to {OUTPUT_JSON}")
        return True

    except Exception as e:
        print("[Employee] Error occurred:", e)
        return False
