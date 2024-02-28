from bs4 import BeautifulSoup
import scrapy

from prh.items import SBook, SPRHDetails, SThirdPartyPrices
from prh.spiders.getdata.prh_helper import PRHHelper
from prh.spiders.getdata.third_party_helper import ThirdPartyHelper

# do the same as scrape_prh.py but with scrapy
class spiders(scrapy.Spider):
    name = "prh-scraper"
    start_urls = ["https://www.penguinlibros.com/ar/40915-aventuras"]
    
    def parse(self, response):
        # Get all books on the page
        for book in response.css('p.productTitle a::attr(href)').getall():
            yield scrapy.Request(book, callback=self.parse_book)
            break
    
    def parse_book(self, response):
        book_soup = BeautifulSoup(response.body, 'lxml')
         
        # Initialize helper class to store data
        helper = PRHHelper()
    
        # Get basic information
        helper.populate_prh_basic_info(book_soup)
        
        # Get detailed info
        helper.populate_prh_detailed_info(book_soup)
        
        # Populate scrapy item
        item = SBook(title=helper.title, author=helper.author, price=helper.price, publication_date=helper.publication_date, imprint=helper.imprint, third_party_prices=[], prh_details=SPRHDetails(colleccion=helper.colleccion, paginas=helper.paginas, target_de_edad=helper.target_de_edad, tipo_de_encuadernacion=helper.tipo_de_encuadernacion, idioma=helper.idioma, fecha_de_publicacion=helper.fecha_de_publicacion, autor=helper.autor, editorial=helper.editorial, referencia=helper.referencia))
        
        # Iterate through all third party links
        for link in response.css('div.bloque_external_link a::attr(href)').getall():
            yield scrapy.Request(link, callback=self.parse_third_party, meta={'item': item, 'url': link, 'bookTitle':helper.title})
        
    def parse_third_party(self, response):
        price = ThirdPartyHelper()
        soup = BeautifulSoup(response.body, 'lxml')
        price.populate_price(soup, response.meta['url'], response.meta['bookTitle'])
        item = SThirdPartyPrices(name=price.name, price=price.price, discount=price.discount)
        
        book_item = response.meta['item']
        book_item['third_party_prices'].append(item)
        return book_item
        