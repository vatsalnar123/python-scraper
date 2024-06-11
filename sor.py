# Import dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_job_search_url(title, location, start=0):
    """Constructs the LinkedIn job search URL."""
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    params = {
        "keywords": title,
        "location": location,
        "start": start
    }
    return base_url, params

def fetch_job_urls(title, location):
    """Fetch job URLs based on job title and location."""
    job_urls = []
    start = 0

    while True:
        url, params = get_job_search_url(title, location, start)
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("li")
        
        if not jobs:
            break
        
        for job in jobs:
            job_link = job.find("a", {"class": "base-card__full-link"})
            if job_link:
                job_urls.append(job_link.get('href'))
        
        start += len(jobs)
    
    return job_urls

def fetch_job_details(job_urls):
    """Fetch job details from a list of job URLs."""
    job_details = []
    
    for job_url in job_urls:
        try:
            response = requests.get(job_url)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            job_post = {"url": job_url}
            
            try:
                job_post["job_title"] = soup.find("h1", {"class": "top-card-layout__title"}).text.strip()
            except:
                job_post["job_title"] = None
            
            try:
                job_post["company_name"] = soup.find("a", {"class": "topcard__org-name-link"}).text.strip()
            except:
                job_post["company_name"] = None
            
            try:
                description = soup.find("div", {"class": "show-more-less-html__markup"}).get_text(separator="\n").strip()
                job_post["job_description"] = description
            except:
                job_post["job_description"] = None
            
            try:
                employee_size = soup.find("span", {"class": "org-top-card-summary__company-size-definition-text"}).text.strip()
                job_post["employee_size"] = employee_size
            except:
                job_post["employee_size"] = None
            
            job_details.append(job_post)
        
        except Exception as e:
            continue
    
    return job_details

def save_to_csv(job_details, filename='jobarea.csv'):
    """Save job details to a CSV file."""
    try:
        existing_df = pd.read_csv(filename)
        existing_urls = existing_df['url'].tolist()
    except FileNotFoundError:
        existing_df = pd.DataFrame()
        existing_urls = []

    new_job_details = [job for job in job_details if job['url'] not in existing_urls]

    if new_job_details:
        df = pd.DataFrame(new_job_details)
        df.to_csv(filename, index=False, mode='a', header=not existing_df.empty)
    else:
        print("No new jobs to add.")

def main():
   
    title = input("Enter the job title: ")
    location = input("Enter the job location: ")
    
   
    job_urls = fetch_job_urls(title, location)
    print(f"Found {len(job_urls)} job URLs.")
    
   
    job_details = fetch_job_details(job_urls)
    print(f"Fetched details for {len(job_details)} jobs.")
    
   
    save_to_csv(job_details, 'jo.csv')
    print("Job details saved to jo.csv.")

if __name__ == "__main__":
    main()
