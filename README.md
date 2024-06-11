LinkedIn Job Scraper
This Python script scrapes job listings from LinkedIn based on a job title and location provided by the user. It utilizes the requests and BeautifulSoup libraries to fetch and parse HTML content from LinkedIn's job search API.

Features
Search for job listings by job title and location: Provides a way to fetch relevant job postings based on user input.
Fetch job URLs from the search results: Handles pagination to collect all job URLs.
Extract job details: Collects information such as job title, company name, job description, and employee size.
Save the extracted job details to a CSV file: Stores the job information in a structured format.
Append new job details to an existing CSV file: Ensures no duplicate entries by appending only new job details to the existing CSV file.
Installation
Clone the Repository

git clone https://github.com/vatsalnar123/python-scraper.git
cd python-scraper
Install Required Dependencies
Use pip to install the required dependencies:

pip install requests beautifulsoup4 pandas
Usage
Run the Script
Execute the script using Python:


python scraper.py
User Input
When prompted, enter the job title and location:

Enter the job title: Data Scientist
Enter the job location: San Francisco
The script will fetch the job URLs, extract job details, and save them to a CSV file named jo.csv.

Script Structure
get_job_search_url(title, location, start=0)
This function constructs the LinkedIn job search URL based on the provided job title, location, and start index.

fetch_job_urls(title, location)
This function fetches job URLs from the LinkedIn job search API based on the job title and location. It handles pagination and returns a list of job URLs.

fetch_job_details(job_urls)
This function takes a list of job URLs and fetches the job details for each URL. It extracts information such as job title, company name, job description, and employee size. The job details are returned as a list of dictionaries.

save_to_csv(job_details, filename='jobarea.csv')
This function saves the job details to a CSV file. If the file already exists, it appends the new job details to the existing file, avoiding duplicates.

main()
This is the main function that gets executed when the script is run. It prompts the user for job title and location, fetches job URLs, extracts job details, and saves them to a CSV file.

Example Output
When the script runs successfully, it will output messages similar to the following:

Enter the job title: Data Scientist
Enter the job location: San Francisco
Found 25 job URLs.
Fetched details for 25 jobs.
Job details saved to jo.csv.
