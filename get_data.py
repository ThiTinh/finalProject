import csv
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_website(website, driver):
    try:
        driver.get(website)
        # Assuming you might need to wait for some dynamic content to load here
        # Add necessary WebDriverWait or time.sleep if needed

        # Get the page source after dynamic content loads
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        title_element = soup.find('h1', class_='_2uQQ3SV0eMHL1P6t5ZDo2q')
        title = title_element.get_text(strip=True) if title_element else 'N/A'

        price_span = soup.find('span', class_='Kn64CpaGkZuigLbd4_JAe')
        price = price_span.find_previous('span').text.strip() if price_span else 'N/A'

        reduced_element = soup.find('div', class_='_2nk2x6QhNB1UrxdI5KpvaF')
        reduced = reduced_element.get_text(strip=True) if reduced_element else 'N/A'

        deposit_input = soup.find('input', {'name': 'property-deposit'})
        deposit_value = deposit_input.get('value') if deposit_input else 'N/A'

        interest_input = soup.find('input', {'name': 'property-interest'})
        annual_interest = interest_input.get('value') if interest_input else 'N/A'

        repayment_input = soup.find('input', {'name': 'property-term'})
        repayment_period = repayment_input.get('value') if repayment_input else 'N/A'

        property_type_element = soup.find('dt', text='PROPERTY TYPE')
        property_type = property_type_element.find_next('dd').get_text(strip=True) if property_type_element else 'N/A'

        bedrooms_element = soup.find('dt', text='BEDROOMS')
        bedrooms = bedrooms_element.find_next('dd').get_text(strip=True) if bedrooms_element else 'N/A'

        bathrooms_element = soup.find('dt', text='BATHROOMS')
        bathrooms = bathrooms_element.find_next('dd').get_text(strip=True) if bathrooms_element else 'N/A'

        tenure_element = soup.find('dt', text='TENURE')
        tenure = tenure_element.find_next('dd').get_text(strip=True) if tenure_element else 'N/A'

        key_feature_items = soup.find_all('li', class_='lIhZ24u1NHMa5Y6gDH90A')
        key_features = [item.get_text(strip=True) for item in key_feature_items] if key_feature_items else 'N/A'

        description_div = soup.find('div', class_='STw8udCxUaBUMfOOZu0iL')
        description_text = description_div.get_text(separator='\n', strip=True) if description_div else 'N/A'

        council_tax_element = soup.find('p', class_='_1VOsciKYew6xj3RWxMv_6J')
        council_tax = council_tax_element.text.strip() if council_tax_element else 'N/A'

        address_element = soup.find('h2', id='mapTitleScrollAnchor')
        address = address_element.text.strip() if address_element else 'N/A'

        agent_div = soup.find('div', class_='_14g3Gg072iB2RZfaVWqhL3')
        agent_name = agent_div.find('h3').text.strip() if agent_div else 'N/A'
        agent_address = agent_div.find('p').text.strip() if agent_div else 'N/A'


    except Exception as e:
        print(f"An error occurred while scraping {website}: {e}")
        title = 'N/A'
        price = 'N/A'
        reduced = 'N/A'
        property_type = 'N/A'
        bedrooms = 'N/A'
        bathrooms = 'N/A'
        tenure = 'N/A'
        key_features = 'N/A'
        description_text = 'N/A'
        council_tax = 'N/A'
        address = 'N/A'
        agent_name = 'N/A'
        agent_address = 'N/A'
        

    property_data = {
        'title': title,
        'price': price,
        'reduced': reduced,
        'property_type': property_type,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'tenure': tenure,
        'key_features': key_features,
        'description_text': description_text,
        'council_tax': council_tax,
        'address': address,
        'agent_name': agent_name,
        'agent_address': agent_address,
        'url': website
    }
    return property_data

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode to avoid opening a browser window
    driver = webdriver.Chrome(options=chrome_options)

    with open('combined_sale_links_end.json', 'r') as json_file:
        website_links = json.load(json_file)

    csv_file = 'sale_data_2.csv'
    fieldnames = ['title', 'price', 'reduced', 'property_type', 'bedrooms', 'bathrooms', 'tenure', 'key_features', 'description_text', 'council_tax', 'address', 'agent_name', 'agent_address', 'url']

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for website in website_links[34210:]:
            property_data = scrape_website(website, driver)
            writer.writerow(property_data)
            print(f'Scraped data for {website} is saved successfully.')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
