import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product listings from a given URL


def scrape_product_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    # Find all product listings
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})

    for listing in listings:
        # Extract product information
        product_url = 'https://www.amazon.in' + \
            listing.find('a', {'class': 'a-link-normal'})['href']
        product_name = listing.find(
            'span', {'class': 'a-size-medium'}).text.strip()
        product_price = listing.find(
            'span', {'class': 'a-price-whole'}).text.strip()

        rating_element = listing.find('span', {'class': 'a-icon-alt'})
        if rating_element:
            rating = rating_element.text.split()[0]
        else:
            rating = 'N/A'

        reviews_count_element = listing.find('span', {'class': 'a-size-base'})
        if reviews_count_element:
            reviews_count = reviews_count_element.text.strip()
        else:
            reviews_count = '0'

        # Append product information to the list
        products.append([product_url, product_name,
                        product_price, rating, reviews_count])

    return products


# Scrape multiple pages of product listings
num_pages = 20
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'

all_products = []

for page in range(1, num_pages+1):
    url = base_url + str(page)
    products = scrape_product_listings(url)
    all_products.extend(products)

# Export data to a CSV file
filename = 'product_listings.csv'

with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name',
                    'Product Price', 'Rating', 'Number of Reviews'])
    writer.writerows(all_products)

print('Product listings scraped and saved to', filename)
