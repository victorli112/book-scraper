from bs4 import BeautifulSoup
import scrapy

from planeta.items import SBook, SThirdPartyPrices
from planeta.spiders.planeta_helper import PlanetaHelper
from planeta.spiders.third_party_helper import ThirdPartyHelper

# do the same as scrape_prh.py but with scrapy
class spiders(scrapy.Spider):
    name = "planeta-scraper"
    handle_httpstatus_list = [404, 500]
    start_urls = ["https://www.planetadelibros.com.ar/libros/novelas/00038/p/1?q=30"
                  "https://www.planetadelibros.com.ar/libros/novela-historica/00013/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/novela-literaria/00012/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/novela-negra/00015/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/novelas-romanticas/00014/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/poesia/00051/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/teatro/00052/p/1?q=30"]
    
    AJAX_URL = "https://www.planetadelibros.com.ar/includes/ajax_canales_venda.php?soporte="
    
    RETRY_HTTP_CODES = [502, 503, 504, 522, 524, 408, 429, 400]
    custom_settings = {
        "RETRY_HTTP_CODES": [502, 503, 504, 522, 524, 408, 429, 400],
        "handle_httpstatus_list": [404, 500],
    }
    dont_parse_third_party = ["bajalibros", "play", "goto", "amazon", "audible", "casassaylorenzo"]
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
        
        # Get all book ids on the page
        all_book_ids = response.css('div.comprar span::attr(data-book-id)').getall()
        all_books_data_sites = [self.AJAX_URL + book_id for book_id in all_book_ids]

        for book_site in all_books_data_sites:
            print(book_site, category)
            # Keep track of duplicate books
            if (book_site, category) in self.links:
               self.num_duplicates += 1
               if self.num_duplicates % 100 == 0:
                   print(f"[COUNT] Processed {self.num_duplicates} duplicates.")
               continue
            else:
               self.links.add((book_site, category))
               
            yield scrapy.Request(book_site, callback=self.parse_book_links, meta={'category': category}, dont_filter=True)
            break
        return
        # TODO VVV
        # Go to next page if it exists and there are books on this page
        if "pageno" in response.request.url:
            next_page = response.request.url.split("pageno=")[0] + "pageno=" + str(int(response.request.url.split("pageno=")[1]) + 1)
            #page = int(response.request.url.split("pageno=")[1]) + 1
        else:
            next_page = response.request.url + "?pageno=2"
            #page = 2
        if next_page and len(all_books) > 0:
            #batching
            #if page > 49:
            #    print(f'On page {page}')
            yield scrapy.Request(next_page, callback=self.parse)
            
    def parse_book_links(self, response):
        if response.status == 500 or response.status == 404:
            print(f"//////////////////// {response.status} ERROR PARSE BOOK /////////////////////////////// {response.url}")
            
        book_soup = BeautifulSoup(response.body, 'lxml')

        # Dictionary of third-party sites mapped to their links
        third_party_links = {}
        
        # Get all third-party links
        for link in book_soup.find_all('a', class_='boto-comprar'):
            third_party_links[link['data-botiga']] = link['href']
        
        try:
            title = book_soup.find("div", class_="titol").text.strip()
            author = book_soup.find("div", class_="autor").text.strip()
            price = book_soup.find("div", class_="preu").text.strip().replace(" ", "")
        except:
            print("++[ERROR]++ Cant get author or title", response.url)
            return 
        
        # Create empty scrapy item to hold information
        item = SBook(
            category=response.meta["category"],
            title=title,
            author=author,
            price=None,
            fecha_publicacion=None,
            idoma=None,
            ISBN=None,
            formato=None,
            presentacion=None,
            third_party_prices=[]
        )
        
        # Iterate through all third party links
        for site_name, link in third_party_links.items():
            if any(x in link for x in self.dont_parse_third_party):
                continue
            elif (link, response.meta['category'], title, author) in self.tracking_third_party_links:
                continue
            else:
                self.tracking_third_party_links.add((link, response.meta['category'], title, author))
                yield scrapy.Request(link, callback=self.parse_third_party, dont_filter=True, meta={'item': item, 'url': link, 'siteName': site_name, 'bookTitle':item['title']})
        
    def parse_third_party(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        book_item = response.meta['item']
        
        if response.meta["siteName"] == "Mercadolibre": # Main site with book details
            planeta_helper = PlanetaHelper()
            planeta_helper.populate_planeta_basic_info(soup, response.meta['bookTitle'])
            book_item['price'] = planeta_helper.price
            book_item['fecha_publicacion'] = planeta_helper.fecha_publicacion
            book_item['idoma'] = planeta_helper.idoma
            book_item['ISBN'] = planeta_helper.ISBM
            book_item['formato'] = planeta_helper.formato
            book_item['presentacion'] = planeta_helper.presentacion
        else: # Third party site
            price = ThirdPartyHelper()
            price.populate_price(soup, response.meta['url'], response.meta['bookTitle'])
            item = SThirdPartyPrices(name=price.name, price=price.price, discount=price.discount)
            book_item['third_party_prices'].append(item)
            
        return book_item
        