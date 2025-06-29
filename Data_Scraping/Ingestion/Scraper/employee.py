import requests
import json

API_URL = "https://api.slingacademy.com/v1/sample-data/files/employees.json"
OUTPUT_JSON = "employee_data.json"

def scrape_employee_data():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            print("[Employee] Failed to fetch data. Status:", response.status_code)
            return False

        json_data = response.json()

        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        print(f"[Employee] JSON data saved to {OUTPUT_JSON}")
        return True

    except Exception as e:
        print("[Employee] Error occurred:", e)
        return False
