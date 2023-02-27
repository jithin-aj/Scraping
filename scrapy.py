# Import packages
from selenium import webdriver
import time
import pandas as pd
import os

# URL to open from the browser for jobs scraping
url = "https://www.linkedin.com/jobs/search/?currentJobId=3436059284&geoId=101207163&keywords=software%20engineer"

# Set up webdriver (chrome)
driver = webdriver.Chrome(executable_path="/home/aj/Work/Software/chrome_driver/chromedriver")

# Open the URL from the browser
driver.get(url)

# Wait for few seconds just to load all information (just in case)
driver.implicitly_wait(10)

# Get the jobs count for scraping
jobs = driver.find_elements_by_class_name("results-context-header__job-count")[0].text

# As the previous result is in string, convert it to the numeric value
job_count = pd.to_numeric(jobs)

# Scroll through jobs
# NOTE: There will be around 20 - 25 jobs list per window, scroll number of times according to the
# number of jobs resulted in the search
max_window = (int)(job_count / 20) + 1
driver.execute_script("window.scrollTo(0, 0);")
#time.sleep(10)
for window in range(1, max_window):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Click on "See more jobs" button if encountered
    try:
        more_jobs = driver.find_element_by_xpath("//button[@aria-label='See more jobs']")
        driver.execute_script("arguments[0].click();", more_jobs)

        time.sleep(3)
    except:
        # No button encounter, continue scroll
        pass

        time.sleep(3)

# Extract company name
company_list=[]
for job in range(job_count):
    try:
        company = driver.find_elements_by_class_name('base-search-card__subtitle')[job].text
        company_list.append(company)

    except IndexError:
        print("Complete")

print(company_list)

# Extract job title
job_title=[]
for job in range(job_count):
    try:
        title = driver.find_elements_by_class_name('base-search-card__title')[job].text
        job_title.append(title)

    except IndexError:
        print("Complete")

print(job_title)

# Close the driver
driver.quit()
