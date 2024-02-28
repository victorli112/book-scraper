from typing import List
from . third_party_prices import ThirdPartyPrices


class Book:
    def __init__(self):
        self.title = None
        self.author = None
        self.price = None
        self.publication_date = None
        self.imprint = None
        self.third_party_prices : List[ThirdPartyPrices] = []
        self.prh_details = None

    def populate_prh_basic_info(self, book_soup):
        self.title = book_soup.find('h1', class_="page-title").find('span').text.strip()
        self.author = book_soup.find('div', class_='autorYfav').find('a').text.strip()
        self.price = book_soup.find('span', class_='product-price').text.strip()
        self.publication_date = book_soup.find('div', class_='product-category-name-editorial').text.split(',')[1].strip()
        self.imprint = book_soup.find('div', class_='product-category-name-editorial').text.split(',')[0].strip()
        
    def __str__(self):
        return f'{self.title} by {self.author}, costs {self.price}, publication_date {self.publication_date}, imprint {self.imprint}, third party prices {self.third_party_prices}, prh details {self.prh_details}'

    def __repr__(self):
        return f'title={self.title}, author={self.author}, price={self.price}, publication_date={self.publication_date}, imprint={self.imprint}, third_party_prices={self.third_party_prices}, prh_details={self.prh_details}'