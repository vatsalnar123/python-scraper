from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import sys
import selenium
import webdriver_manager

def log_environment_info():
    print(f"Selenium version: {selenium.__version__}")
    print(f"Webdriver Manager version: {webdriver_manager.__version__}")
    print(f"Pandas version: {pd.__version__}")
    print(f"Python version: {sys.version}")

def initialize_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment the next line to run in headless mode
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_to_linkedin(driver, username_str, password_str):
    driver.get("https://linkedin.com/uas/login")
    time.sleep(5)
    
    username = driver.find_element(By.ID, "username")
    username.send_keys(username_str)  
    
    pword = driver.find_element(By.ID, "password")
    pword.send_keys(password_str)
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

def search_and_extract_urls(driver, job_title, location):
    driver.get("https://www.linkedin.com/jobs")
    
    try:
        search_job = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']"))
        )
        search_location = driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
        
        search_job.send_keys(job_title)
        search_location.send_keys(location)
        search_location.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Failed to initiate search: {str(e)}")
        driver.quit()
        return []

    time.sleep(10)  # Allow time for search results to load
    job_urls = []
    page_number = 1
    
    while True:
        try:
            links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jobs/view/"]')
            if not links:
                print(f"No job links found on page {page_number}")
                break

            for link in links:
                job_url = link.get_attribute('href')
                if job_url and job_url.startswith('/'):
                    job_url = "https://www.linkedin.com" + job_url
                job_urls.append(job_url)

            print(f"Found {len(links)} job links on page {page_number}")

            # Check if the "Next" button exists before clicking it
            next_button = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Next']")
            if next_button:
                driver.execute_script("arguments[0].click();", next_button[0])
                page_number += 1
                print(f"Moving to page {page_number}")
                time.sleep(10)  # Wait for next page of results to load
            else:
                print("No 'Next' button found or it is not enabled")
                break
        except Exception as e:
            print(f"Error during pagination: {str(e)}")
            break
    
    print(f"Total job URLs found: {len(job_urls)}")
    return job_urls

def extract_job_details(driver, job_urls):
    job_details = []
    for index, url in enumerate(job_urls):
        if not url:
            continue
        driver.get(url)
        time.sleep(5)
        try:
            title = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
            ).text
            
            try:
                company = driver.find_element(By.CSS_SELECTOR, 'a[href*="/company/"]').text
            except:
                try:
                    company = driver.find_element(By.CSS_SELECTOR, 'div.topcard__org-name-link').text
                except:
                    company = "Company not found"
            
            description = None
            description_selectors = [
                'div.show-more-less-html__markup',
                'div.description__text',
                'div[class*="description__content"]',
                'div[class*="job-description"]',
                'div[class*="description"]',
                'section[class*="description"]'
            ]
            for selector in description_selectors:
                try:
                    description = driver.find_element(By.CSS_SELECTOR, selector).text
                    break
                except:
                    continue
            
            if not description:
                description = "Description not found"
            
            employee_size = 'Not Available'

            job_details.append({
                'URL': url,
                'Title': title,
                'Company': company,
                'Description': description,
                'Employee Size': employee_size
            })
            print(f"Extracted details for job {index + 1}/{len(job_urls)}")
        except Exception as e:
            print(f"Failed to extract data for {url}: {str(e)}")

    return job_details

def main():
    log_environment_info()
    driver = initialize_driver()
    
    username_str = input("Enter LinkedIn email: ")
    password_str = input("Enter LinkedIn password: ")
    
    login_to_linkedin(driver, username_str, password_str)
    
    job_title = input("Enter the job title: ")
    location = input("Enter the location: ")
    
    job_urls = search_and_extract_urls(driver, job_title, location)
    
    job_details = extract_job_details(driver, job_urls)
    driver.quit()

    if job_details:
        df = pd.DataFrame(job_details)
        df.to_csv('job_details.csv', index=False)
        print("Job details extracted and saved to job_details.csv")
    else:
        print("No job details extracted")

if __name__ == "__main__":
    main()
