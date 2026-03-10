import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import re

BASE_URL = "https://books.toscrape.com/"

def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, "html.parser")

# function to get all book URLs from the main page
def get_book_urls(page_url=BASE_URL):

    soup = get_soup(BASE_URL)

    book_urls = []
    # each book is in an <article class="product_pod"> tag
    for book in soup.find_all("article", class_="product_pod"):
        relative_url = book.h3.a["href"]  # relative URL like "catalogue/a-light-in-the-attic_1000/index.html"
        absolute_url = urljoin(BASE_URL, relative_url)  # convert to complete URL
        book_urls.append(absolute_url)

    return book_urls



# function to scrape book details from the book detail page
def get_book_details(book_url):
    soup = get_soup(book_url)

    # get description from meta tag
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"].strip() if description_tag else ""

    # get availability text
    availability_text = soup.find("p", class_="instock availability").text.strip()

    # get table data (UPC, Tax, etc.)
    table = soup.find("table", class_="table table-striped")
    table_data = {}
    if table:
        for row in table.find_all("tr"):
            key = row.find("th").text
            value = row.find("td").text
            table_data[key] = value

    # return a dictionary with the scraped details
    return {
        "description": description,
        "availability": availability_text,
        "table_data": table_data
    }



# function to scrape book data from the website and return a list of dictionaries
def get_book_list():
    soup = get_soup(BASE_URL)
    books_urls = get_book_urls()  # get list of book URLs to ensure we have the correct order and count
    books_html = soup.find_all("article", class_="product_pod")

    book_list = []
    for i, book in enumerate(books_html):
        title = book.h3.a["title"]
        
        price_text = book.find("p", class_="price_color").text
        price = float(re.search(r'\d+\.\d+', price_text).group())
        
        rating_class = book.find("p", class_="star-rating")["class"]
        rating_dict = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
        rating = rating_dict[rating_class[1]]
        
        image_url = urljoin(BASE_URL, book.img["src"])
        
        book_list.append({
            "title": title,
            "price": price,
            "rating": rating,
            "image_url": image_url,
            "book_url": books_urls[i]  # Add the corresponding book URL from the list

        })
    return book_list

# This function combines the basic book list with the details from each book's page
def get_book_list_with_details():
    books = get_book_list()  # get basic book info from the main page
    for book in books:
        details = get_book_details(book["book_url"])  # get details from the book's detail page
        book.update(details)  # add the details to the existing dictionary
    return books


if __name__ == "__main__":
    books = get_book_list()
    
    # create books.json 
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"{len(books)} books saved to data/books.json")

    #create books_with_details.json
    books_with_details = get_book_list_with_details()
    with open("data/books_with_details.json", "w", encoding="utf-8") as f:
        json.dump(books_with_details, f, ensure_ascii=False, indent=4)
    print(f"{len(books_with_details)} books with details saved to data/books_with_details.json")