import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

BOOKS_JSON_PATH = Path("data/books_with_details.json")
OUTPUT_JSON_PATH = Path("data/books_with_categories.json")
BASE_CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/"

CATEGORIES = [
    # ... sua lista de categorias ...
]

# ===== Function to add categories =====
def add_categories():
    with BOOKS_JSON_PATH.open("r", encoding="utf-8") as f:
        books_data = json.load(f)

    for cat_slug in CATEGORIES:
        category_name = cat_slug.split("_")[0].replace("-", " ").title()
        category_url = urljoin(BASE_CATEGORY_URL, f"{cat_slug}/index.html")
        print(f"\n🔹 Processing category: {category_name}")

        page = 1
        while True:
            page_url = category_url if page == 1 else urljoin(BASE_CATEGORY_URL, f"{cat_slug}/page-{page}.html")
            resp = requests.get(page_url)
            if resp.status_code != 200:
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.select("article.product_pod h3 a")
            if not links:
                break

            for a in links:
                href = a["href"]
                full_url = urljoin(page_url, href)

                found = False
                for book in books_data:
                    if book["book_url"] == full_url:
                        book["category"] = category_name
                        found = True
                        print(f'Title: {book["title"]}')
                        print(f'URL: {book["book_url"]}')
                        print(f'Category: {book["category"]}')
                        print("-----")
                        break
                if not found:
                    print(f"Book not found in JSON: {full_url}")

            page += 1

    with OUTPUT_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(books_data, f, indent=4, ensure_ascii=False)
    print("\n✅ Todas as categorias adicionadas. JSON atualizado em", OUTPUT_JSON_PATH)

# ===== Only run when executed directly =====
if __name__ == "__main__":
    add_categories()