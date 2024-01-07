import json
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Chrome options to disable certificate errors and web security
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")

# Create a new Chrome browser object with the specified options
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

def element_exists(css_selector):
    try:
        driver.find_element(By.CSS_SELECTOR, css_selector)
        return True
    except NoSuchElementException:
        return False

def get_links_from_css_selector(base_url, css_selector):
    link_list = []
    try:
        driver.get(base_url)
        # Use WebDriverWait to wait for the elements to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        all_elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        links = [x.get_attribute('href') for x in all_elements if x.get_attribute('href')]
        link_list.extend(links)
    except (NoSuchElementException, WebDriverException) as e:
        print(f"Error while processing {base_url}: {e}")
    return link_list

sale = []
with open('menu_sale_href.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if row and len(row) > 0:
            sale.append(row[0])

link_lists = []

for url in sale[1000:]:
    try:
        selectors = 'div.propertyCard-details a'
        link_lists.extend(get_links_from_css_selector(url, selectors))
    except Exception as e:
        print(f"Error while processing {url}: {e}")
        continue  # Skip to the next URL if an error occurs

# Save the final list of links to a JSON file
with open('sale_links_1500.json', 'w') as json_file:
    json.dump(link_lists, json_file, indent=4, sort_keys=True)

# Close the browser properly
driver.quit()
print(len(link_lists))
