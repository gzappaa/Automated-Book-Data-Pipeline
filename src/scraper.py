import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from urllib.parse import urljoin
import time
import concurrent.futures
from .parser import BookParser

BASE_URL = "https://books.toscrape.com/"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds between retries


def get_soup(url):
    """Return BeautifulSoup object from URL with retries and UTF-8 encoding."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            res = requests.get(url, timeout=30)
            res.raise_for_status()
            res.encoding = 'utf-8'
            return BeautifulSoup(res.text, "html.parser")
        except (requests.Timeout, requests.ConnectionError) as e:
            print(f"Attempt {attempt}/{MAX_RETRIES} failed for {url}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed to fetch {url} after {MAX_RETRIES} attempts.")
                return None
        except requests.HTTPError as e:
            print(f"HTTP error for {url}: {e}")
            return None


def get_book_details(book_url):
    """Scrape book details including description, availability, table data, and category from breadcrumb."""
    soup = get_soup(book_url)
    if soup is None:
        print(f"Skipping {book_url}")
        return {}

    # Parse description, availability, and table data
    description = BookParser.parse_description(soup)
    availability_text = BookParser.parse_availability(soup)
    table = soup.find("table", class_="table table-striped")
    table_data = BookParser.parse_table(table)

    # Extract category from breadcrumb (3rd <a> tag)
    breadcrumb_links = soup.select("ul.breadcrumb li a")
    category = breadcrumb_links[2].text.strip() if len(breadcrumb_links) > 2 else "Unknown"

    return {
        "description": description,
        "availability": availability_text,
        "table_data": table_data,
        "category": category
    }


def get_all_books():
    """Scrape all books from main pages (paginated) with progress prints."""
    all_books = []
    total_pages = 50
    book_counter = 0

    def process_page(page_num):
        nonlocal book_counter
        url = BASE_URL if page_num == 1 else urljoin(BASE_URL, f"catalogue/page-{page_num}.html")
        soup = get_soup(url)
        if soup is None:
            print(f"Page {page_num} failed to load.")
            return []

        books_html = soup.find_all("article", class_="product_pod")
        page_books = []
        for book_html in books_html:
            book_counter += 1
            page_books.append(BookParser.parse_book(book_html))
            print(f"Processing book {book_counter}/1000")
        print(f"Page {page_num}/{total_pages} done with {len(page_books)} books")
        return page_books

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_page, range(1, total_pages + 1))

    for page_books in results:
        all_books.extend(page_books)

    print(f"Total books collected: {len(all_books)}")
    return all_books


def get_book_list_with_details():
    """Fetch all books with their detailed info in parallel, including category."""
    books = get_all_books()
    total_books = len(books)
    book_counter = 0

    def fetch_details(book):
        nonlocal book_counter
        details = get_book_details(book["book_url"])
        book.update(details)
        book_counter += 1
        print(f"Book {book_counter}/{total_books} processed")
        return book

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        books_with_details = list(executor.map(fetch_details, books))

    print(f"All {total_books} books with details processed.")
    return books_with_details


if __name__ == "__main__":
    books = get_all_books()
    Path("data").mkdir(exist_ok=True)

    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    print(f"{len(books)} books saved to data/books.json")

    books_with_details = get_book_list_with_details()
    with open("data/books_with_details.json", "w", encoding="utf-8") as f:
        json.dump(books_with_details, f, ensure_ascii=False, indent=4)
    print(f"{len(books_with_details)} books with details saved to data/books_with_details.json")