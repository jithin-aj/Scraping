# Import packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import time
import re

# URL to open from the browser for jobs scraping
url = "https://www.linkedin.com/jobs/search/?currentJobId=3478021945&geoId=102713980&keywords=software%20engineer%20mysore&location=India&refresh=true"

# Set up webdriver (chrome), automatically manage driver versions and install if required
# create Chrome options object
chrome_options = Options()

# set headless option to run Chrome in the background
chrome_options.add_argument('--headless')
print("Chrome is configured to run in background")

# create Chrome webdriver object with options
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
print("Chrome is running in background...\n")

# Open the URL from the browser
driver.get(url)

# Wait for few seconds to load all the information (just in case)
driver.implicitly_wait(5)

# Get the jobs count for scraping
jobs = driver.find_elements_by_class_name("results-context-header__job-count")[0].text

# As the previous result is in string, convert it to the numeric value
# The search result count be in the format: 1,000+
job_count = int(re.sub("[,+]", "", jobs))
print("Jobs search result count: " + str(job_count) + "\n")

# Scroll through jobs
# NOTE: There will be around 20 - 25 jobs list per window, scroll number of times according to the
# number of jobs resulted in the search
max_window = (int)(job_count / 20) + 1
driver.execute_script("window.scrollTo(0, 0);")
print("Loading all jobs info...")
for window in range(1, max_window):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(2)

    # Click on "See more jobs" button if encountered
    try:
        more_jobs = driver.find_element_by_xpath("//button[@aria-label='See more jobs']")
        driver.execute_script("arguments[0].click();", more_jobs)

        time.sleep(1)
    except:
        # No button encounter, continue scroll
        pass

    time.sleep(1)
    print("Page " + str(window) + " loaded.")
print("All jobs are loaded\n")

# Extracted jobs link form all the "href" with ".../jobs/view" context.
# create a new workbook in append mode and append links one after other
print("Scraping links STARTED...")
wb = openpyxl.Workbook()
ws = wb.active
links = driver.find_elements_by_tag_name("a")
links_list = []
for link in links:
    href_link = link.get_attribute("href")
    link_filter = 'https://in.linkedin.com/jobs/view/'
    if link_filter in href_link:
        links_list.append(href_link)
        ws.append([href_link])

# Save the file
wb.save('linkedin_job_links.xlsx')
wb.close()
print("Links saved as linkedin_job_links.xlsx")

# Close the current browser window
driver.close()
print("Scraping links COMPLETE.\n")

# Scrap top card layout details which contains below information
# Job title
# Company Name
# Company location
# Post dates
#
# The 2nd part of the window contains below information
# About the job
# Primary skills (optional)
# Seniority level
# Employment type
# Job function
# Industries

# create a new workbook and open in append mode with above information as column names
wb = openpyxl.Workbook()
ws = wb.active
ws.append([
    "Job titles",
    "Company names",
    "Locations",
    "Seniority levels",
    "Employment types",
    "Job functions",
    "Industries"
])
wb.save('linkedin_jobs.xlsx')

# Now we have the links for all the jobs listed open one after the other and scrap all the
# necessary information about the job
print("Scraping jobs information STARTED...")
count = 0
# Iterate over rows
for url in links_list:
    print(url)
    # Open new instance
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(0.5) # time to load the page

    try:
        # Element job title
        job_title_element = driver.find_element_by_css_selector("h1.top-card-layout__title")
        job_title = job_title_element.text.strip()

        # Element company name
        company_name_element = driver.find_element_by_css_selector("a.topcard__org-name-link")
        company_name = company_name_element.text.strip()

        # Element company location
        location_element = driver.find_element_by_css_selector("span.topcard__flavor--bullet")
        location = location_element.text.strip()

        # Locate job criteria section
        criteria_section = driver.find_element_by_class_name("description__job-criteria-list")

        # Extract all job criteria items
        criteria_items = criteria_section.find_elements_by_class_name("description__job-criteria-item")

        # Loop through criteria items and extract criteria data
        for item in criteria_items:
            # extract criteria subheader and text
            subheader = item.find_element_by_class_name("description__job-criteria-subheader").text

            # Filter item to specific list
            if "Seniority level" in subheader:
                seniority_level = item.find_element_by_class_name("description__job-criteria-text").text
            elif "Employment type" in subheader:
                employment_type = item.find_element_by_class_name("description__job-criteria-text").text
            elif "Job function" in subheader:
                job_function = item.find_element_by_class_name("description__job-criteria-text").text
            elif "Industries" in subheader:
                industry = item.find_element_by_class_name("description__job-criteria-text").text

    except NoSuchElementException:
        # Some times we get login page when we try to open the URL, ignore and proceed to next
        print("Job info page NOT FOUND")
        driver.close()
        continue

    driver.close()

    ws.append([
        job_title,
        company_name,
        location,
        seniority_level,
        employment_type,
        job_function,
        industry
    ])

    # save changes to output file
    wb.save('linkedin_jobs.xlsx')

    count += 1
    print("Job " + str(count) + " COMPLETE")

print("Jobs data scrap COMPLETE\n")
print("Jobs information are saved as linkedin_jobs.xlsx")

