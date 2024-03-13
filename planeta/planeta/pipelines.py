# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from xlsxwriter import Workbook

from planeta.items import SBook

THIRD_PARTY_PRH = ['Librenta', 'Buscalibre', 'Tematika', 'SBS_Liberia', 'Libreria_Hernandez', 'Cuspide', 'Tras_los_Pasos']
class ExcelWriterPipeline:
    def open_spider(self, spider):
        self.row = 1
        self.results = {
            'aventuras': {},
            'fantasia': {},
            'literatura_contemporanea': {},
            'novela_misterio_y_thriller': {},
            'poesia': {},
            'ciencia_ficcion': {},
            'grandes_clasicos': {},
            'novela_historica': {},
            'novela_romantica': {}
        }
        self.num_books = 0
        
    def close_spider(self, spider):
        # Clean the data
        # {title : {Title: x, Author: y}, title2: {Title: x, Author: y}}
        # for title, info in self.results.items():
        #     for key, value in info.items():
        #         if not value and key.startswith('discount'):
        #             self.results[title][key] = '0%'
        #         elif not value and key.startswith('price'):
        #             self.results[title][key] = '-1'
        
        # TO EXCEL 
        print(f"FINAL Processed {self.num_books} books, counts of each category: {[(k, len(v)) for k, v in self.results.items()]}")
        
        ordered_columns = ['Title', 'Author', 'Price', 'Fecha de Publicacion', 'Idoma', 'ISBN', 'Formato', 'Presentacion']
        wb = Workbook("penguin_random_house_books.xlsx")

        for category, books in self.results.items():
            ws = wb.add_worksheet(category)
            first_row = 0
            for header in ordered_columns:
                col = ordered_columns.index(header) # We are keeping order.
                ws.write(first_row, col, header) # We have written first row which is the header of worksheet also.

            row = 1
            for book in books.values():
                for _key,_value in book.items():
                    col = ordered_columns.index(_key)
                    ws.write(row, col, _value)
                row += 1 # enter the next row

        wb.close()
        
    def process_item(self, item, spider):
        if isinstance(item, SBook):
            self.handle_book(item, spider)
        return item
    
    def handle_book(self, item, spider):
        category_dict = self.results[item["category"]]
        primary_key = (item["title"], item["author"], item["category"], item["price"])
                
        book_data = self.create_book_dict(item)
        if primary_key in category_dict:
            category_dict[primary_key] = {**category_dict[primary_key], **book_data}
        else:
            category_dict[primary_key] = book_data
            self.num_books += 1
            #print("Book added to category", item["category"])
            if self.num_books % 200 == 0:
                print(f"Processed {self.num_books} books, counts of each category: {[(k, len(v)) for k, v in self.results.items()]}")
        
    def create_book_dict(self, book_item):
        book_dict = {
            'Title': book_item['title'], 
            'Author': book_item['author'], 
            'Price': book_item['price'], 
            'Fecha de Publicacion': book_item['fecha_de_publicacion'],
            'Idoma': book_item['idoma'],
            'ISBN': book_item['ISBN'],
            'Formato': book_item['formato'],
            'Presentacion': book_item['presentacion']
        }
        list_of_third_party_prices = book_item['third_party_prices']
        if list_of_third_party_prices:
            all_collected_names = []
            for price_item in list_of_third_party_prices:
                book_dict[f'price_in_{price_item["name"].replace(" ", "_")}'] = price_item['price']
                book_dict[f'discount_{price_item["name"].replace(" ", "_")}'] = price_item['discount']
                all_collected_names.append(price_item['name']) 
            not_collected = list(set(THIRD_PARTY_PRH) - set(all_collected_names))
            for name in not_collected:
                book_dict[f'price_in_{name.replace(" ", "_")}'] = None
                book_dict[f'discount_{name.replace(" ", "_")}'] = None
                
        return book_dict
