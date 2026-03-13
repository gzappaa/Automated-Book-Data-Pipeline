import unittest
import json
from pathlib import Path
from urllib.parse import urlparse
from re import sub

'''
UNITTEST FOR BOOKS JSON AND IMAGE FILES

Note: This test should only be run **after all main scripts have been executed**.
It validates:

1. All books have required fields: title, table_data, and UPC
2. UPCs are unique
3. image_url is valid
4. Price is positive
5. All downloaded image files exist on disk (in data/images)

Make sure to run this test after all main scripts have been executed.
'''

class TestBooksJSON(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load JSON once for all tests
        json_path = Path("data/books_with_details.json")
        with json_path.open("r", encoding="utf-8") as f:
            cls.books = json.load(f)
        # Define the images folder path
        cls.images_folder = Path("data/images")

        # Load categories JSON
        categories_json_path = Path("data/books_with_categories.json")
        with categories_json_path.open("r", encoding="utf-8") as f:
            cls.books_with_categories = json.load(f)

    def test_all_books_have_required_fields(self):
        """All books must have title, table_data, and UPC"""
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                self.assertIn("title", book)
                self.assertIn("table_data", book)
                self.assertIn("UPC", book["table_data"])
                self.assertTrue(book["table_data"]["UPC"], "UPC cannot be empty")

    def test_no_duplicate_upc(self):
        """No duplicate UPCs should exist"""
        upcs = [b["table_data"]["UPC"] for b in self.books if "table_data" in b and "UPC" in b["table_data"]]
        self.assertEqual(len(upcs), len(set(upcs)), "Duplicate UPCs found")

    def test_image_url_valid(self):
        """All books must have a valid image_url"""
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                self.assertIn("image_url", book)
                url = book["image_url"]
                parsed = urlparse(url)
                self.assertTrue(parsed.scheme in ("http", "https"), f"Invalid URL: {url}")

    def test_image_file_exists(self):
        """Check that the downloaded image file exists on disk"""
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                upc = book["table_data"]["UPC"]
                # Filename pattern used in downloader: UPC + safe title
                safe_title = sub(r'[<>:"/\\|?*]', '_', book['title']).strip().lower()
                safe_title = sub(r'[\s_]+', '_', safe_title)
                filename = f"{upc}_{safe_title}.jpg"
                filepath = self.images_folder / filename
                self.assertTrue(filepath.exists(), f"Image file missing: {filename}")

    def test_price_positive(self):
        """The price should be a positive number"""
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                price = book.get("price")
                self.assertIsInstance(price, (int, float), "Price must be a number")
                self.assertGreaterEqual(price, 0, "Negative price found")

    # All books in the categories JSON must have a non-empty category
    def test_all_books_have_category(self):
        for book in self.books_with_categories:
            with self.subTest(book=book.get("title", "No title")):
                self.assertIn("category", book, "Category field missing")
                self.assertTrue(book["category"], "Category cannot be empty")


if __name__ == "__main__":
    unittest.main()