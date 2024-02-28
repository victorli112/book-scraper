import requests
from bs4 import BeautifulSoup

# Define the URLs of the publishers
urls = ["https://www.penguinlibros.com/ar/40915-aventuras"]

# Define the data fields to scrape
fields = ["title", "author", "price", "publication_date", "imprint", "collection", "number_of_pages", "size", "language", "ISBN"]

# Initialize a list to store the data
data = []

# Loop through each URL
for url in urls:
    # Send a GET request to the URL
    response = requests.get(url)
    f = open("response.html", "w")
    f.write(response.text)
    f.close()
    break 

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the 'Literatura' category
    literatura = soup.find('div', {'class': 'Literatura'})

    # Loop through each subcategory
    for subcategory in literatura.find_all('div', {'class': 'subcategory'}):
        # Loop through each book
        for book in subcategory.find_all('div', {'class': 'book'}):
            # Initialize a dictionary to store the book data
            book_data = {}

            # Loop through each field
            for field in fields:
                # Find the field in the book HTML and store it in the dictionary
                book_data[field] = book.find('div', {'class': field}).text

            # Add the book data to the list
            data.append(book_data)

# Print the data
for book in data:
    print(book)