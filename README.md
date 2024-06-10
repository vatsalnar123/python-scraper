LinkedIn Job Scraper
This script (sor.py) automates the process of logging into LinkedIn, searching for job listings, and extracting job details using Selenium and BeautifulSoup. The extracted job details are saved into a CSV file.
Prerequisites

Python 3.x
Google Chrome browser
pip (Python package installer)

Installation

Clone the Repository:

bashCopy codegit clone https://github.com/vatsalnar123/python-scraper.git
cd python-scraper

Install Required Packages:

bashCopy codepip install -r requirements.txt
Ensure requirements.txt includes:
textCopy codeselenium
webdriver-manager
beautifulsoup4
pandas
Usage

Run the Script:

bashCopy codepython sor.py

Enter LinkedIn Credentials: The script will prompt you to enter your LinkedIn email and password.
Enter Job Search Details: You will be asked to enter the job title and location for the job search.
Job Details Extraction: The script will log into LinkedIn, perform the job search, and extract job details. The details are saved to job_details.csv.

Script Details
Functions

log_environment_info(): Logs versions of the installed libraries and Python.
initialize_driver(): Initializes the Selenium WebDriver for Chrome.
login_to_linkedin(driver, username_str, password_str): Logs into LinkedIn using the provided credentials.
search_and_extract_urls(driver, job_title, location): Searches for jobs on LinkedIn based on the provided job title and location and extracts job URLs.
extract_job_details(driver, job_urls): Extracts job details such as title, company, and description from the job URLs.

Workflow

Log Environment Information: Logs the versions of Selenium, WebDriver Manager, Pandas, and Python.
Initialize WebDriver: Initializes the Chrome WebDriver.
Login to LinkedIn: Logs into LinkedIn with the provided email and password.
Job Search: Searches for jobs based on the provided job title and location and extracts job URLs.
Extract Job Details: Extracts job details (title, company, description) from the job URLs and saves them to job_details.csv.

Output
The extracted job details are saved into job_details.csv in the current directory.
Notes

Headless Mode: Uncomment the line # options.add_argument("--headless") in the initialize_driver function to run the browser in headless mode.
Error Handling: The script includes basic error handling to manage issues like login failures, search initiation failures, and pagination errors.
