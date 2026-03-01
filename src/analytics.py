import json

# Function to load book data from JSON file.
def load_books_from_json(filepath="data/books.json"):

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Reads JSON file and calculates statistics.
def calculate_stats_from_json(filepath="data/books.json"):


    books = load_books_from_json(filepath)

    if not books:
        raise ValueError("Book list is empty.")

    prices = [book["price"] for book in books]

    average_price = round(sum(prices) / len(prices), 2)
    max_price = round(max(prices), 2)
    min_price = round(min(prices), 2)

    most_expensive = max(books, key=lambda x: x["price"])
    cheapest = min(books, key=lambda x: x["price"])

    return {
        "total_books": len(books),
        "average_price": average_price,
        "max_price": max_price,
        "min_price": min_price,
        "most_expensive": most_expensive,
        "cheapest": cheapest,
        "books": books
    }

