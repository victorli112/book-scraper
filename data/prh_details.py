class PRHDetails:
    def __init__(self):
        self.colleccion = None
        self.paginas = None
        self.target_de_edad = None
        self.tipo_de_encuadernacion = None
        self.idioma = None
        self.fecha_de_publicacion = None
        self.autor = None
        self.editorial = None
        self.referencia = None
        
    def populate_prh_info(self, book_soup, author):
        # Gather PRH details except reference number
        prh_details_list = book_soup.find('dl', class_='caracteristicas-prod').find_all('dd', class_='value')
        self.colleccion = prh_details_list[0].text.strip()
        self.paginas = prh_details_list[1].text.strip()
        self.target_de_edad = prh_details_list[2].text.strip()
        self.tipo_de_encuadernacion = prh_details_list[3].text.strip()
        self.idioma = prh_details_list[4].text.strip()
        self.fecha_de_publicacion = prh_details_list[5].text.strip()
        self.autor = author
        self.editorial = prh_details_list[7].text.strip()
        
        # Get reference number 
        self.referencia = book_soup.find('div', class_='product-reference').find('span').text.strip()

    def __str__(self):
        return f'coleccion= {self.colleccion}, paginas= {self.paginas}, target_de_edad= {self.target_de_edad}, tipo_de_encuadernacion= {self.tipo_de_encuadernacion}, idioma= {self.idioma}, fecha_de_publicacion= {self.fecha_de_publicacion}, autor= {self.autor}, editorial= {self.editorial}, referencia= {self.referencia}'
    
    def __repr__(self):
        return f'coleccion= {self.colleccion}, paginas= {self.paginas}, target_de_edad= {self.target_de_edad}, tipo_de_encuadernacion= {self.tipo_de_encuadernacion}, idioma= {self.idioma}, fecha_de_publicacion= {self.fecha_de_publicacion}, autor= {self.autor}, editorial= {self.editorial}, referencia= {self.referencia}'