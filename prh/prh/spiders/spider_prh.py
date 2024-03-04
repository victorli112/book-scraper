from bs4 import BeautifulSoup
import scrapy

from prh.items import SBook, SPRHDetails, SThirdPartyPrices
from prh.spiders.prh_helper import PRHHelper
from prh.spiders.third_party_helper import ThirdPartyHelper

# do the same as scrape_prh.py but with scrapy
class spiders(scrapy.Spider):
    name = "prh-scraper"
    handle_httpstatus_list = [404, 500]
    start_urls = ["https://www.penguinlibros.com/ar/40915-aventuras",
                  "https://www.penguinlibros.com/ar/40919-fantasia",
                  "https://www.penguinlibros.com/ar/40925-literatura-contemporanea",
                  "https://www.penguinlibros.com/ar/40929-novela-negra-misterio-y-thriller",
                  "https://www.penguinlibros.com/ar/40933-poesia",
                  "https://www.penguinlibros.com/ar/40917-ciencia-ficcion",
                  "https://www.penguinlibros.com/ar/40923-grandes-clasicos",
                  "https://www.penguinlibros.com/ar/40927-novela-historica",
                  "https://www.penguinlibros.com/ar/40931-novela-romantica"]
    
    RETRY_HTTP_CODES = [502, 503, 504, 522, 524, 408, 429, 400]
    custom_settings = {
        "RETRY_HTTP_CODES": [502, 503, 504, 522, 524, 408, 429, 400],
        "handle_httpstatus_list": [404, 500],
    }
    dont_parse_third_party = ["bajalibros", "play", "goto", "amazon", "audible"]
    links = []
    
    def parse(self, response):
        # we might still be getting a response from 500 errors
        if response.status == 500 or response.status == 404:
            print("//////////////////// 500 ERROR ///////////////////////////////", response.url)
           
        # Category of request separated by _
        category = '_'.join(response.request.url.split("/")[-1].split("-")[1:]).split('?')[0]
        if category == 'novela_negra_misterio_y_thriller':
            category = 'novela_misterio_y_thriller'
        
        # Get all books on the page
        all_books = response.css('p.productTitle a::attr(href)').getall()
        for book in all_books:
            if book in self.links:
                print("+++++++ Duplicate book", book)
            else:
                self.links.append(book)
            yield scrapy.Request(book, callback=self.parse_book, meta={'category': category})
        
        # Go to next page if it exists
        next_page = response.selector.xpath('//*[@id="paginacionProductos"]/div/ul/li/a[contains(@class, "next")]/@href').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
            
    def parse_book(self, response):
        if response.status == 500 or response.status == 404:
            print("//////////////////// 500 ERROR PARSE BOOK ///////////////////////////////", response.url)
            
        book_soup = BeautifulSoup(response.body, 'lxml')
    
        # Initialize helper class to store data
        helper = PRHHelper()
    
        # Get basic information
        try:
            helper.populate_prh_basic_info(book_soup)
        except:
            print("Can't parse basic info", response.url, response.status)
            
        # Get detailed info
        try:
            helper.populate_prh_detailed_info(book_soup)
        except:
            print("Can't parse detailed info", response.url, response.status)
            
        # Populate scrapy item
        item = SBook(category=response.meta['category'],
                     title=helper.title, 
                     author=helper.author, 
                     price=helper.price, 
                     publication_date=helper.publication_date, 
                     imprint=helper.imprint, 
                     third_party_prices=[], 
                     prh_details=SPRHDetails(colleccion=helper.colleccion, 
                                             paginas=helper.paginas, 
                                             target_de_edad=helper.target_de_edad, 
                                             tipo_de_encuadernacion=helper.tipo_de_encuadernacion, 
                                             idioma=helper.idioma, 
                                             fecha_de_publicacion=helper.fecha_de_publicacion, 
                                             autor=helper.autor, 
                                             editorial=helper.editorial, 
                                             referencia=helper.referencia
                                             )
                     )
        
        # Iterate through all third party links
        for link in response.css('div.bloque_external_link a::attr(href)').getall():
            if any(x in link for x in self.dont_parse_third_party):
                continue
            yield scrapy.Request(link, callback=self.parse_third_party, meta={'item': item, 'url': link, 'bookTitle':helper.title})
        
    def parse_third_party(self, response):
        price = ThirdPartyHelper()
        soup = BeautifulSoup(response.body, 'lxml')
        price.populate_price(soup, response.meta['url'], response.meta['bookTitle'])
        
        item = SThirdPartyPrices(name=price.name, price=price.price, discount=price.discount)
        book_item = response.meta['item']
        book_item['third_party_prices'].append(item)
        return book_item
        
