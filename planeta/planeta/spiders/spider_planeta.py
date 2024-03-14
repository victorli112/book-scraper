from bs4 import BeautifulSoup
import scrapy

from planeta.items import SBook, SThirdPartyPrices
from planeta.spiders.planeta_helper import PlanetaHelper
from planeta.spiders.third_party_helper import ThirdPartyHelper

# do the same as scrape_prh.py but with scrapy
class spiders(scrapy.Spider):
    name = "planeta-scraper"
    handle_httpstatus_list = [404, 500]
    start_urls = [#"https://www.planetadelibros.com.ar/libros/novelas/00038/p/1?q=30"
                  #"https://www.planetadelibros.com.ar/libros/novela-historica/00013/p/1?q=30",
                  #"https://www.planetadelibros.com.ar/libros/novela-literaria/00012/p/1?q=30",
                  #"https://www.planetadelibros.com.ar/libros/novela-negra/00015/p/1?q=30",
                  #"https://www.planetadelibros.com.ar/libros/novelas-romanticas/00014/p/1?q=30",
                  #"https://www.planetadelibros.com.ar/libros/poesia/00051/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/teatro/00052/p/1?q=30"]
    
    AJAX_URL = "https://www.planetadelibros.com.ar/includes/ajax_canales_venda.php?soporte="
    
    RETRY_HTTP_CODES = [502, 503, 504, 522, 524, 408, 429, 400]
    custom_settings = {
        "RETRY_HTTP_CODES": [502, 503, 504, 522, 524, 408, 429, 400],
        "handle_httpstatus_list": [404, 500],
    }
    dont_parse_third_party = ["bajalibros", "play", "goto", "amazon", "audible", "casassaylorenzo", "books", "itunes", "casadellibro", "storytel", "es", "tienda"]
    links = set()
    tracking_third_party_links = set()
    num_duplicates = 0
    
    def parse(self, response):
        # we might still be getting a response from 500 errors
        if response.status == 500 or response.status == 404:
            print("//////////////////// 500 ERROR PARSE ///////////////////////////////", response.url)
           
        # Category of request separated by _
        category = '_'.join(response.request.url.split("/libros/")[1].split("/")[0].split("-"))
        if category == "novelas":
            category = "novela_contemporanea"
        
        soup = BeautifulSoup(response.body, 'lxml')
        
        # Get all book ids on the page
        book_info = soup.find('div', class_='resultat-cercador')
        if not book_info:
            print("No results", response.request.url)
            return 
        
        # find all <li> elements in book info
        books = book_info.find_all('li')
        
        for book in books:
            # link to main site for the book
            basic_information_link = book.find('a')['href']
            planeta_helper = PlanetaHelper()
            try:
                planeta_helper.populate_planeta_basic_info(basic_information_link)
            except Exception as e:
                # No book found
                print("Failed to populate", response.request.url, basic_information_link, e)
                continue
            
            # Create empty scrapy item to hold information
            item = SBook(
                category=category,
                title=planeta_helper.title,
                author=planeta_helper.author,
                price=planeta_helper.price,
                fecha_publicacion=planeta_helper.fecha_publicacion,
                idoma=planeta_helper.idoma,
                ISBN=planeta_helper.ISBN,
                formato=planeta_helper.formato,
                presentacion=planeta_helper.presentacion,
                third_party_prices=[]
            )
                        
            # the numerical id component
            book_id = book.find('div', class_='comprar')
            if book_id and book_id.find('span')['data-book-id']:
                
                # get the numerical id
                book_id = book_id.find('span')['data-book-id']
                book_site = self.AJAX_URL + book_id
                print("Added book", item['title'], "Thirdparty Site:", book_site)


                # Keep track of duplicate books
                if (book_site, book_id, category) in self.links:
                    self.num_duplicates += 1
                    if self.num_duplicates % 10 == 0:
                        print(f"[COUNT] Processed {self.num_duplicates} duplicates.")
                        continue
                else:
                    self.links.add((book_site, book_id, category))
                    yield scrapy.Request(book_site, callback=self.parse_third_party_page, meta={'category': category, 'item': item}, dont_filter=True)

        # Go to next page if it exists and there are books on this page
        next_page = response.css('div.paginacio-seguent a::attr(href)').get()
        if next_page:
            print(f"Next page: {next_page}")
            yield scrapy.Request(next_page, callback=self.parse)
            
    def parse_third_party_page(self, response):
        if response.status == 500 or response.status == 404:
            print(f"//////////////////// {response.status} ERROR PARSE BOOK /////////////////////////////// {response.url}")
            
        book_soup = BeautifulSoup(response.body, 'lxml')

        # Dictionary of third-party sites mapped to their links
        third_party_links = {}
        
        # Get all third-party links
        for link in book_soup.find_all('a', class_='boto-comprar'):
            third_party_links[link['data-botiga']] = link['href']
        
        item = response.meta['item']
        
        # Iterate through all third party links
        for site_name, link in third_party_links.items():
            if any(x in link for x in self.dont_parse_third_party):
                continue
            elif (link, response.meta['category'], item['title'], item['author']) in self.tracking_third_party_links:
                continue
            else:
                self.tracking_third_party_links.add((link, response.meta['category'], item['title'], item['author']))
                yield scrapy.Request(link, callback=self.parse_third_party, dont_filter=True, meta={'item': item, 'url': link, 'siteName': site_name, 'parent_link': response.request.url, 'bookTitle':item['title']})

    def parse_third_party(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        book_item = response.meta['item']
        price = ThirdPartyHelper()
        price.populate_price(soup, response.meta['url'], response.meta['bookTitle'])
        item = SThirdPartyPrices(name=price.name, price=price.price, discount=price.discount)
        book_item['third_party_prices'].append(item)
            
        return book_item
        
