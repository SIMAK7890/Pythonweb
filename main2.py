import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape additional information from a product URL


def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract additional information
    asin_element = soup.find('th', string='ASIN')
    asin = asin_element.find_next_sibling(
        'td').text.strip() if asin_element else 'N/A'

    product_description_element = soup.find(
        'div', {'id': 'productDescription'})
    product_description = product_description_element.text.strip(
    ) if product_description_element else 'N/A'

    manufacturer_element = soup.find('a', {'id': 'bylineInfo'})
    manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

    return asin, product_description, manufacturer


# Read the CSV file containing the product listings
filename = 'product_listings.csv'
product_listings = []

with open(filename, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    product_listings = list(reader)

# Scrape additional information for each product URL
all_products_details = []

for product in product_listings:
    url = product[0]
    details = scrape_product_details(url)
    all_products_details.append(product + list(details))

# Export the updated data to a new CSV file
updated_filename = 'product_details.csv'

with open(updated_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating',
                    'Number of Reviews', 'ASIN', 'Product Description', 'Manufacturer'])
    writer.writerows(all_products_details)

print('Product details scraped and saved to', updated_filename)
