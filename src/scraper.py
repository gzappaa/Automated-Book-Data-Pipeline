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

def get_book_urls(page_url=BASE_URL):
    """
    returns a list of absolute URLs for each book on the page
    """
    soup = get_soup(BASE_URL)

    book_urls = []
    # each book is in an <article class="product_pod"> tag
    for book in soup.find_all("article", class_="product_pod"):
        relative_url = book.h3.a["href"]  # relative URL like "catalogue/a-light-in-the-attic_1000/index.html"
        absolute_url = urljoin(BASE_URL + "catalogue/", relative_url)  # convert to complete URL
        book_urls.append(absolute_url)

    return book_urls


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






if __name__ == "__main__":
    books = get_book_list()
    
    # create books.json 
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"{len(books)} books saved to data/books.json")