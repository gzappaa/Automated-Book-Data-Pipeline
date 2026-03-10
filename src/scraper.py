import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import re


def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, "html.parser")

# function to scrape book data from the website and return a list of dictionaries
def get_book_list():
    BASE_URL = "https://books.toscrape.com/"
    soup = get_soup(BASE_URL)
    books_html = soup.find_all("article", class_="product_pod")

    book_list = []
    for book in books_html:
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
            "image_url": image_url
        })
    return book_list


if __name__ == "__main__":
    books = get_book_list()
    
    # create books.json 
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"{len(books)} books saved to data/books.json")