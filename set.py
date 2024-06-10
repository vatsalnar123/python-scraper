from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def initialize_driver():
    
    "Initializes the Selenium ChromeDriver specifying a version."
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def get_user_input():
    
    "prompts the user to enter his details"
    job_title = input("Enter the job title: ")
    location = input("Enter the location: ")
    return job_title, location

def search_and_extract_urls(driver, job_title, location):
    
    driver.get("https://www.linkedin.com/jobs")
    
    try:
        search_job = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
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

            job_urls.extend([link.get_attribute('href') for link in links])
            print(f"Found {len(links)} job links on page {page_number}")

            next_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Next']")
            if not next_buttons:
                print("No 'Next' button found")
                break
            next_button = next_buttons[0]
            if not next_button.is_enabled():
                print("'Next' button is not enabled")
                break
            next_button.click()
            page_number += 1
            print(f"Moving to page {page_number}")
            time.sleep(10)  # Wait for next page of results to load
        except Exception as e:
            print(f"Error during pagination: {str(e)}")
            break
    
    print(f"Total job URLs found: {len(job_urls)}")
    return job_urls

def extract_job_details(driver, job_urls):
    """
    Visits each job URL and extracts detailed job information.
    """
    job_details = []
    for index, url in enumerate(job_urls):
        driver.get(url)
        time.sleep(5)
        try:
            title = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
            
            try:
                company = driver.find_element(By.CSS_SELECTOR, 'a[href*="/company/"]').text
            except:
                try:
                    company = driver.find_element(By.CSS_SELECTOR, 'div.topcard__org-name-link').text
                except:
                    company = "Company not found"
            
            # Try multiple selectors for the job description
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
            
            # Placeholder if detailed company size is not directly available
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
    """
    The main function to run the job scraper.
    """
    driver = initialize_driver()
    job_title, location = get_user_input()
    urls = search_and_extract_urls(driver, job_title, location)
    details = extract_job_details(driver, urls)
    driver.quit()

    if details:
        # Output and save job details
        df = pd.DataFrame(details)
        df.to_csv('job_details.csv', index=False)
        print("Job details extracted and saved to job_details.csv")
    else:
        print("No job details extracted")

if __name__ == "__main__":
    main()
