import unidecode


class PRHHelper:
    def __init__(self):
        self.title = None
        self.author = None
        self.price = None
        self.publication_date = None
        self.imprint = None
        self.prh_details = None
        
        # PRH details
        self.colleccion = None
        self.paginas = None
        self.target_de_edad = None
        self.tipo_de_encuadernacion = None
        self.idioma = None
        self.fecha_de_publicacion = None
        self.autor = None
        self.editorial = None
        self.referencia = None
        
    def populate_prh_basic_info(self, book_soup):
        self.title = book_soup.find('h1', class_="page-title").find('span').text.strip()
        self.author = book_soup.find('div', class_='autorYfav').find('a').text.strip()
        self.price = unidecode.unidecode(book_soup.find('span', class_='product-price').text.strip()).replace(' ','')
        self.publication_date = book_soup.find('div', class_='product-category-name-editorial').text.split(',')[1].strip()
        self.imprint = book_soup.find('div', class_='product-category-name-editorial').text.split(',')[0].strip()
    
    def populate_prh_detailed_info(self, book_soup):
        # Gather PRH details except reference number
        prh_details_list = book_soup.find('dl', class_='caracteristicas-prod').find_all('dd', class_='value')
        self.colleccion = prh_details_list[0].text.strip()
        self.paginas = prh_details_list[1].text.strip()
        self.target_de_edad = prh_details_list[2].text.strip()
        self.tipo_de_encuadernacion = prh_details_list[3].text.strip()
        self.idioma = prh_details_list[4].text.strip()
        self.fecha_de_publicacion = prh_details_list[5].text.strip()
        self.autor = self.author
        self.editorial = prh_details_list[7].text.strip()
        
        # Get reference number 
        self.referencia = book_soup.find('div', class_='product-reference').find('span').text.strip()