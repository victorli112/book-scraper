import requests
from bs4 import BeautifulSoup

from . headers import HEADERS

class ThirdPartyPrices:
    def __init__ (self):
        self.name = None
        self.price = None
        self.discount = None
    
    def populate_price(self, url):
        if "www" in url:
            site_name = url.split('.')[1]
        else: 
            site_name = url.split('.')[0].split('//')[1]
        match site_name:
            case "librenta":
                self.name = "Librenta"
                self.get_librenta_price(url)
            case "buscalibre":
                self.name = "Buscalibre"
                self.get_buscalibre_price(url)
            case "tematika":
                self.name = "Tematika"
                self.get_tematika_price(url)
            case "sbs":
                self.name = "SBS Liberia"
                self.get_sbs_price(url)
            case "libreriahernandez":
                self.name = "Liberia Hernandez"
                self.get_libreria_hernandez_price(url)
            case "cuspide":
                self.name = "Cuspide"
                self.get_cuspide_price(url)
            case "traslospasos":
                self.name = "Tras los Pasos"
                self.get_traslospasos_price(url)
            case _:
                raise Exception("Third party site not handled", site_name, url) 
        
        # if there is no price, something is wrong (parsing error, etc)
        # if price is -1, it is out of stock
        if not self.price:
            raise Exception("Price not found", url)
            
    def get_librenta_price(self, url): 
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Get price 
        price = soup.find('span', class_='andes-money-amount__fraction')
        if price:
            price = price.text
            self.price = "$" + price.strip()
        else:
            self.price = -1
        
        # No discount available
        
    def get_buscalibre_price(self, url):
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Get price 
        price = soup.find('p', class_='precioAhora')
        if price:
            self.price = price.find('span').text.strip()
        else: 
            self.price = -1
            
        # Get discount if possible
        discount = soup.find('div', class_='box-descuento')
        if discount:
            self.discount = discount.find('strong').text.strip()
        
    def get_tematika_price(self, url):
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Get discount if possible
        old_price = soup.find('p', class_='old-price')
        if old_price: 
            old_price = old_price.find('span', class_='price').text.strip()
            old_price_float = float(old_price.replace('$', '').replace('.', '').split(',')[0])
            curr_price = soup.find('p', class_='special-price').find('span', class_='price')
            if curr_price:
                curr_price = curr_price.text.strip()
                curr_price_float = float(curr_price.replace('$', '').replace('.', '').split(',')[0])
                discount = 1 - (curr_price_float / old_price_float)
                self.discount = str(round(discount * 100)).strip() + "%"
            else:
                raise Exception("Discount but no price")
            
        # No discount
        else:        
            price = soup.find('span', class_='regular-price')
            if price: 
                price = price.find('span', class_='price').text.strip()
                self.price = price
            else:
                self.price = -1
        
    def get_sbs_price(self, url):
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Get price 
        price = soup.find('span', class_='best-price')
        if price:
            price = price.text.strip()
            self.price = price
        else:
            self.price = -1
            return
        
        # If there is a discount
        old_price = soup.find('span', class_='old-price')
        if old_price: 
            old_price = old_price.text
            old_price_float = float(old_price.replace('$', '').replace('.', '').split(',')[0])
            price_float = float(price.replace('$', '').replace('.', '').split(',')[0])
            discount = 1 - (price_float / old_price_float)
            self.discount = str(round(discount * 100)).strip() + "%"
    
    def get_libreria_hernandez_price(self, url):
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Get price 
        price = soup.find('td', class_='searchPrice')
        if price:
            self.price = price.text.strip()
        else:
            self.price = -1
                
    def get_cuspide_price(self, url):
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        price = soup.find('p', class_='product-page-price')
        if price:
            price = price.find('bdi').text.strip()
            self.price = price
        else: # no price
            self.price = -1
            return
        
        # If there is a discount, find it and update price
        if soup.find('p', class_='price-on-sale'):
            discounted_price = soup.find('p', class_='price-on-sale').find_all('bdi')[1].text
            formatted_disc_price = float(discounted_price.replace('$', '').replace('.', '').split(',')[0])
            formatted_price = float(price.replace('$', '').replace('.', '').split(',')[0])
            discount = 1 - (formatted_disc_price / formatted_price)
            self.discount = str(round(discount * 100)).strip() + "%"
            self.price = discounted_price
                
    def get_traslospasos_price(self, url):
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Get price 
        price = soup.find('div', class_='item-description')
        if price:
            self.price = price.find('span', class_='item-price').text.strip()
        else:
            self.price = -1
        
    def __str__(self):
        return f'name={self.name}, price={self.price}, discount={self.discount}'
    
    def __repr__(self):
        return f'name={self.name}, price={self.price}, discount={self.discount}'
    