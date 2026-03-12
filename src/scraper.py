import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import re
import time
from .parser import BookParser

BASE_URL = "https://books.toscrape.com/"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds between retries


# get BeautifulSoup object from a URL
def get_soup(url):
    """Return BeautifulSoup object for the URL, retrying on timeout."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            res = requests.get(url, timeout=30)
            res.raise_for_status()  # garante que status != 200 levanta exceção
            return BeautifulSoup(res.text, "html.parser")
        except (requests.Timeout, requests.ConnectionError) as e:
            print(f"Attempt {attempt}/{MAX_RETRIES} failed for {url}: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed to fetch {url} after {MAX_RETRIES} attempts.")
                return None  # maybe raise? if we want to handle this at a higher level
        except requests.HTTPError as e:
            print(f"HTTP error for {url}: {e}")
            return None


# function to scrape book details from the book detail page
def get_book_details(book_url):
    soup = get_soup(book_url)
    if soup is None:
        print(f"Skipping {book_url}")
        return {}

    # get description using BookParser
    description = BookParser.parse_description(soup)

    # get availability using BookParser
    availability_text = BookParser.parse_availability(soup)

    # get table data using BookParser
    table = soup.find("table", class_="table table-striped")
    table_data = BookParser.parse_table(table)

    # return a dictionary with the scraped details
    return {
        "description": description,
        "availability": availability_text,
        "table_data": table_data
    }



# function to scrape book data from the website and return a list of dictionaries
def get_all_books():
    all_books = []
    page_num = 1
    while True:
        if page_num == 1:
            url = BASE_URL
        elif page_num == 51:
            break  # we know there are only 50 pages, so we can stop after page 50
        else:
            url = urljoin(BASE_URL, f"catalogue/page-{page_num}.html")
        soup = get_soup(url)
        if soup is None:
            break
        books_html = soup.find_all("article", class_="product_pod")
        if not books_html:
            break
        for book_html in books_html:
            all_books.append(BookParser.parse_book(book_html))
        page_num += 1
    return all_books

# This function combines the basic book list with the details from each book's page
def get_book_list_with_details():
    books = get_all_books()  # get basic book info from the main page

    for book in books:
        details = get_book_details(book["book_url"])  # get details from the book's detail page
        book.update(details)  # add the details to the existing dictionary

    return books


if __name__ == "__main__":
    books = get_all_books()
    
    # create books.json 
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"{len(books)} books saved to data/books.json")

    #create books_with_details.json
    if False:  # set to True to run this part
        books_with_details = get_book_list_with_details()
        with open("data/books_with_details.json", "w", encoding="utf-8") as f:
            json.dump(books_with_details, f, ensure_ascii=False, indent=4)
        print(f"{len(books_with_details)} books with details saved to data/books_with_details.json")