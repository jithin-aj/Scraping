# Scraping
Web scraping for jobs data extraction

## Required packages
* **Selenium**
* **Pandas**
* **Web browser driver - Chrome**
* **Web driver manager**

## Install selenium package
### Required version 3.x

If your version is >= 4, we suggest you to uninstall the package and install the required version

You can uninstall selenium package by runnning the below command
```
pip uninstall selenium
```


To install the selenium package with version 3.x, run the below command
```
pip3 install selenium==3.*
```

## Install pandas package
```
pip install pandas
```

## Setup web driver
The web drive version should be equivalent to the one you have in your system and make you downloaded the correct version
Run the below command to get the chrome version
```
$ google-chrome --version
```

### Link for chrome driver downloads
[Chrome driver downloads](https://chromedriver.chromium.org/downloads)

If you use different web browser, just search for respective browser driver in the google and download the correct version that matched with your system.

Once all the above packages are installed successfully open the python script and change the driver path with the one you have downloaded and extracted.

```webdriver.Chrome(executable_path="DRIVER-PATH")```

### WebDriver Manager
This package automatically install the driver and setup the path for executing web browser

Install the package by runnning below command
```
pip install webdriver-manager
```

## Run the script
```
python3 scrapy.py
```

The script will create an excel file with all the URLs extracted from the jobs list we got
