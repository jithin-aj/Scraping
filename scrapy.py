# Import packages
from selenium import webdriver
import time
import pandas as pd
import os
import re

# URL to open from the browser for jobs scraping
url = "https://www.linkedin.com/jobs/search/?currentJobId=3478021945&geoId=102713980&keywords=software%20engineer%20mysore&location=India&refresh=true"

# Set up webdriver (chrome)
driver = webdriver.Chrome(executable_path="/home/aj/Work/Software/chrome_driver/chromedriver")

# Open the URL from the browser
driver.get(url)

# Wait for few seconds to load all the information (just in case)
driver.implicitly_wait(5)

# Get the jobs count for scraping
jobs = driver.find_elements_by_class_name("results-context-header__job-count")[0].text

# As the previous result is in string, convert it to the numeric value
# The search result count be in the format: 1,000+
job_count = int(re.sub("[,+]", "", jobs))
print(job_count)

# Scroll through jobs
# NOTE: There will be around 20 - 25 jobs list per window, scroll number of times according to the
# number of jobs resulted in the search
max_window = (int)(job_count / 20) + 1
driver.execute_script("window.scrollTo(0, 0);")

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

        time.sleep(2)

'''
We are now extracting only the job links for getting more information about the job, so ignore below
scraping

# Extract company name
# Array of objects for the below param
company_list=[]
job_title=[]
location=[]
for job in range(job_count):
    try:
        # Company list
        company = driver.find_elements_by_class_name('base-search-card__subtitle')[job].text
        company_list.append(company)

        # Job title
        title = driver.find_elements_by_class_name('base-search-card__title')[job].text
        job_title.append(title)

        # Location (Location, posted on, salary (optional))
        loc = driver.find_elements_by_class_name('base-search-card__metadata')[job].text
        # loc = loc.split('\n')[0]
        location.append(loc)

    except IndexError:
        print("Complete")
'''

# Extracted jobs link form all the "href" with ".../jobs/view" context
job_link=[]
links = driver.find_elements_by_tag_name("a")
for link in links:
    href_link = link.get_attribute("href")
    link_filter = 'https://in.linkedin.com/jobs/view/'
    if link_filter in href_link:
        job_link.append(href_link)

# Create a pandas dataframe from the extracted data
df = pd.DataFrame({'Job link': job_link})

# Write the dataframe to an Excel file
df.to_excel('linkedin_job_links.xlsx', index=False)

# Close the driver
driver.quit()
