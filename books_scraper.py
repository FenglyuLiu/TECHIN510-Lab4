import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from db import Database


load_dotenv()
BASE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'

class BookScraper:
    def __init__(self, database_url):
        self.database = Database(database_url)
    
    def scrape_books(self):
        self.database.create_table()

        page = 1
        while True:
            url = BASE_URL.format(page)
            print(f"Scraping {url}")
            response = requests.get(url)
            
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            if not soup.find('li', class_='next'):
                break  # No next page

            books = soup.select('.product_pod')
            for book in books:
                data = self.parse_book(book)
                self.database.insert_book(data)
            page += 1

    def parse_book(self, book):
        title = book.select_one('h3 > a')['title']
        price = book.select_one('.price_color').text[2:]  # Remove the pound symbol
        rating = book.select_one('p')['class'][1]  # e.g., 'Three'
        in_stock = 'In stock' in book.select_one('.availability').text
        
        return {
            'title': title,
            'price': float(price.replace('£', '')),  # Ensure price is a float
            'rating': rating,
            'in_stock': in_stock
        }

if __name__ == '__main__':
    database_url = os.getenv('DATABASE_URL')
    scraper = BookScraper(database_url)
    scraper.scrape_books()
