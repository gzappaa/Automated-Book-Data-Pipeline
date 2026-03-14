import json

BAD_CATEGORIES = {"default", "add a comment"}

with open("data/books_with_details.json", "r", encoding="utf-8") as f:
    books = json.load(f)

clean_books = []

for book in books:
    category = book["category"]

    if category.lower() in BAD_CATEGORIES:
        category = "Miscellaneous"

    clean_books.append({
        "title": book["title"],
        "category": category,
        "price": book["price"],
        "rating": book["rating"],
        "image_url": book["image_url"],
        "book_url": book["book_url"],
        "description": book["description"],
        "upc": book["table_data"]["UPC"]
    })

with open("data/clean_books.json", "w", encoding="utf-8") as f:
    json.dump(clean_books, f, indent=4, ensure_ascii=False)