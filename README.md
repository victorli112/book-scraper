# book-scraper

Implemented with Scrapy
Research data scraper for Argentinian books prices and discounts

## How to run

### Prerequesites:

1. Install Python and Pip
2. Install packages from `requirements.txt` using `pip install -r requirements.txt`
3. Ensure Scrapy is downloaded by running `scrapy -v`

### Running the Spiders

I have noticed that the spiders will skip URLs if there are too many links for some reason, thus scraping is done in batches. `planeta/` and `prh/` directories indicate individual separate scrapers.

1. Modify `batches.py` file in the directory, **only `CURRENT_BATCH` at the bottom needs to be changed**
2. Make sure you are at the root directory (`/book-scraper/planeta/`), then run the spider using `scrapy crawl planeta-scraper` or `scrapy crawl prh-scraper`
3. When it is finished, the .xlxs file will be in the root directory
4. When scraping is done for all batches, you will need to run `python3 combine_planeta.py` or `python3 combine_prh.py` in the utility directory
5. The final xlsx file will be `planeta_books.xlsx` or `prh_books.xlsx`

### Penguin Random House https://www.penguinlibros.com/ar/

- Scrape category: Literatura -> Aventura … Peosia
- From main page, save title, author, price, imprint, publication date
- From details, save Collection … Referencia
- Click on all third-party sites, save price/discount as price_in_StoreX and discount_storeX

### Grupo Planeta https://www.planetadelibros.com.ar/

- Scrape category: Tematicas -> Literatura -> Novela contemporanea … Teatro
- Save basic book information
- Click on all third-party sites, save price/discount as price_in_StoreX and discount_storeX
