from bs4 import BeautifulSoup
import requests
import unidecode
class PlanetaHelper:
    def __init__(self):
        self.title = None
        self.author = None
        self.price = None
        self.fecha_publicacion = None
        self.idoma = None
        self.ISBN = None
        self.formato = None
        self.presentacion = None
        
    def populate_planeta_basic_info(self, link):
        response = requests.get(link, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'Referer': 'https://www.penguinlibros.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'identity'})
        
        book_soup = BeautifulSoup(response.content, 'lxml')
        
        title_block = book_soup.find('div', class_="titol")
        if title_block:
            self.title = book_soup.find('h1').text.strip()
        else:
            raise Exception("No title for book", link)
        
        price_block = book_soup.find('div', class_="dades-generals")
        if price_block and price_block.find('div', class_='preu_format'):
            self.price = unidecode.unidecode(book_soup.find('div', class_='preu_format').text.strip()).replace(' ','')
        
        author_tag = book_soup.find('div', class_='autors')
        if author_tag and author_tag.find('h2'):
            self.author = author_tag.find('h2').text.strip()
        
        details_block = book_soup.find('div', class_='fitxa-tecnica-caixa')
        if details_block:
            publicacion = details_block.find('span')
            # first two spans are date and isbn
            if publicacion:
                self.fecha_publicacion = publicacion.text.strip()
            
            isbn = details_block.find('span', itemprop="isbn")
            if isbn:
                self.ISBN = isbn.text.replace("-","").strip()
                self.idoma = "Español"
                # rest of the information is after isbn span
                information = isbn.next_sibling.text.split("|")
                print(information)
                for info in information:
                    if "Formato" in info:
                        self.idoma = info.split(":")[1].strip()
                    elif "Presentación" in info:
                        self.presentacion = info.split(":")[1].strip()