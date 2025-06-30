# Data_scraping_project
Multi-source data scraping and processing pipeline using Python  
Team: Shreenidhi, Auryn, Shravya 

## Overview
This project scrapes and processes data from multiple sources:

1. Books to Scrape – for book details  
2. Employee API – JSON-based employee data  
3. Employee Google Drive – CSV-based employee data  

All datasets are processed, validated, and tested using a modular pipeline with file detection, normalization, and mocking-based unit tests.

## Objective

- Extract and transform structured data (books and employees)  
- Normalize, validate, and log data integrity issues  
- Verify file types, structure, and content  
- Perform unit tests dynamically based on scraper type  

## Technologies Used

| Category         | Libraries                              |
|------------------|----------------------------------------|
| Scraping         | requests, BeautifulSoup                |
| File Handling    | json, csv, pandas, mimetypes           |
| Processing       | pandas                                 |
| Testing          | unittest, unittest.mock (MagicMock)    |
| Logging & Flow   | print statements with control logic    |

## Business Flow

1. Select Scraper  
   Input is taken via Scraper ID (e.g., 100, 200, 300)

2. Load Data File  
   File is expected to exist locally (CSV or JSON)

3. Processor Execution  
   Calls appropriate processor module:
   - book_process.py
   - employee_process.py
   - employeeGD_process.py

4. Data Validation  
   Each processor performs:
   - Schema validation
   - Data normalization
   - Type checking
   - Optional transformation (e.g., phone, currency)

5. Unit Testing  
   Runs MagicMock-based tests tailored to the scraper

---

## Code Structure

Directory Tree:
DATA_SCRAPING/
├── Ingestion/
│ └── Scraper/
│ ├── book.py
│ ├── employee.py
│ └── employee_GD.py
├── Processing/
│ ├── lamda/
│ │ └── main.py
│ ├── Processor/
│ │ ├── book_process.py
│ │ ├── employee_process.py
│ │ └── employeeGD_process.py
│ ├── Unit test/
│ │ └── unit_test.py
│ └── run_scraper.json
├── books_data.csv
├── employee_data.json
├── employee_data.csv

## Processor Details

Book
- Validates .csv structure and required fields
- Handles rating conversion and missing tags

Employee (API JSON)
- Combines name fields
- Derives designation from experience
- Flags invalid phone numbers
- Validates and casts types

Employee GD (CSV)
- Validates file format
- Ensures required fields exist
- Logs unreadable or broken rows

## Error Handling

- File not found → logged and ignored  
- Unsupported file type → displayed to user  
- Missing columns → triggers test case failure  
- Invalid phone, salary, or dates → normalized and logged  

## Testing (MagicMock)

All test cases use MagicMock to simulate data without accessing actual files.  

Tests are executed via unit_test.py and invoked from main.py automatically based on scraper type.

| Test Suite          | Test ID | Test Description                              |
|---------------------|---------|-----------------------------------------------|
| Book                | TC01    | Verify CSV File Download                      |
|                     | TC02    | Validate File Type and Format (.csv)          |
|                     | TC03    | Verify CSV File Extraction                    |
|                     | TC04    | Validate Data Structure                       |
|                     | TC05    | Handle Missing or Invalid Data                |
| Employee            | TC06    | Verify JSON File Download                     |
|                     | TC07    | Validate File Type and Format (.json)         |
|                     | TC08    | Verify JSON File Extraction                   |
|                     | TC09    | Validate Data Structure                       |
|                     | TC10    | Handle Missing or Invalid Data                |
| EmployeeGD          | TC11    | Verify CSV File Download                      |
|                     | TC12    | Validate File Type and Format (.csv)          |
|                     | TC13    | Verify CSV File Extraction                    |
|                     | TC14    | Validate Data Structure                       |
|                     | TC15    | Handle Missing or Invalid Data                |


## Sample Data Formats

books_data.csv
| Title               | Price | Rating | Availability | Product URL                                             |
|---------------------|-------|--------|--------------|---------------------------------------------------      |
| A Light in the Attic| 51.77 | 3      | In stock     |https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html|

employee_data.json

```json
[
  {
    "id": 1,
    "first_name": "Jose",
    "last_name": "Lopez",
    "email": "joselopez0944@slingacademy.com",
    "phone": "+1-971-533-4552x1542",
    "gender": "male",
    "age": 25,
    "job_title": "Project Manager",
    "years_of_experience": 1,
    "salary": 8500,
    "department": "Product",
    "hire_date": "2020-07-20"
  }
]
```

| user\_id       | first\_name | last\_name | email                 | job\_title         | phone        | hire\_date |
| ---------------| ----------- | ---------- | --------------------- | ------------------ | -------------| ---------- |
| 8717bbf45cCDbEe| Shelia      | Mahoney    | pwarner@example.org   | Probapion Officer  | 857-139-8239 | 2021-12-01 |


## Contributors
Shreenidhi Kamath
Auryn 
Shravya Rai


