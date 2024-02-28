from typing import List
import requests
from bs4 import BeautifulSoup
import time
import lxml
import cchardet

from data.book_data import Book
from data.prh_details import PRHDetails
from data.third_party_prices import ThirdPartyPrices

def main():
    start = time.time()
    # Define the categories of the publishers
    urls = ["https://www.penguinlibros.com/ar/40915-aventuras"]

    # Initialize a list to store the data
    books : List[Book] = []

    # Loop through each category
    for url in urls:
        # Send a GET request to the URL
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'lxml')

        """
        
        """
        page = 0
        num_book = 0
        all_book_links_on_page = [book.a['href'] for book in soup.find_all('p', class_="productTitle")]
            
        while all_book_links_on_page:
            print(f'[PAGE] {page}')
            # Loop through each book URL
            for link in all_book_links_on_page:
                print(f'    [BOOK] {num_book}')
                book_response = requests.get(link)
                book_soup = BeautifulSoup(book_response.content, 'lxml')
                
                # Initialize to store the book data
                book = Book()
                
                # Get basic information
                book.populate_prh_basic_info(book_soup)
                
                # Gather PRH detailed info
                prh_details = PRHDetails()
                prh_details.populate_prh_info(book_soup, book.author)
                book.prh_details = prh_details
                
                # Get all third party links
                third_party_links = [anchor['href'] for anchor in book_soup.find('div', class_='bloque_external_link').find_all('a')]
                
                # Get third party prices
                third_party_prices = []
                for third_party_link in third_party_links:
                    price = ThirdPartyPrices()
                    try:
                        price.populate_price(third_party_link)
                    except:
                        raise Exception({"Third party error":  third_party_link, "Book title": book.title, "PRH link": link})
                    third_party_prices.append(price)
                book.third_party_prices = third_party_prices
                
                books.append(book)
                num_book += 1
            break
            
            # Get the next page
            page += 1
            response = requests.get(url + f"?page={page}")
            all_book_links_on_page = [book.a['href'] for book in soup.find_all('p', class_="productTitle")]     
        print(books)
        print(f"Time taken: {time.time() - start}")
        break 

main()

# # testing third party
# price = ThirdPartyPrices()
# price.populate_price("https://www.sbs.com.ar/9789875667198?utm_source=Referral&utm_medium=Penguinlibros")
# print(price)