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
        colleccion_tag = book_soup.find('dt', text='Colección')
        self.colleccion = colleccion_tag.find_next_sibling('dd').text.strip()
        
        paginas_tag = book_soup.find('dt', text='Páginas')
        self.paginas = paginas_tag.find_next_sibling('dd').text.strip()
        
        target_de_edad_tag = book_soup.find('dt', text='Target de Edad')
        self.target_de_edad = target_de_edad_tag.find_next_sibling('dd').text.strip()
        
        tipo_de_encuadernacion_tag = book_soup.find('dt', text='Tipo de encuadernación')
        self.tipo_de_encuadernacion = tipo_de_encuadernacion_tag.find_next_sibling('dd').text.strip()
        
        idoma_tag = book_soup.find('dt', text='Idioma')
        self.idioma = idoma_tag.find_next_sibling('dd').text.strip()
        
        fecha_de_publicacion_tag = book_soup.find('dt', text='Fecha de publicación')
        self.fecha_de_publicacion = fecha_de_publicacion_tag.find_next_sibling('dd').text.strip()
        
        self.autor = self.author
        
        editorial_tag = book_soup.find('dt', text='Editorial')
        self.editorial = editorial_tag.find_next_sibling('dd').text.strip()
        
        # Get reference number 
        self.referencia = book_soup.find('div', class_='product-reference').find('span').text.strip()