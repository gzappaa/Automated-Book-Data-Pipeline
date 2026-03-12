import unittest
from unittest.mock import patch, Mock
import re
from urllib.parse import urljoin
from src.scraper import get_book_list, BASE_URL
from bs4 import BeautifulSoup

# Paths of the fake HTML files saved for testing
CATALOGUE_HTML_PATH = "tests/data/catalogue.html"
BOOK_DETAIL_HTML_PATH = "tests/data/book_detail.html"

class TestBookScraperMock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Patch requests.get for the entire class
        patcher = patch("requests.get")
        cls.mock_get = patcher.start()
        cls.addClassCleanup(patcher.stop)

        # Mock response for the catalogue page
        mock_response = Mock()
        with open(CATALOGUE_HTML_PATH, "r", encoding="utf-8") as f:
            mock_response.text = f.read()
        cls.mock_get.return_value = mock_response

        # Scrape the book list (uses mocked HTML)
        cls.book_list = get_book_list()

        # Add book_url to each book based on the mocked HTML
        soup = BeautifulSoup(mock_response.text, "html.parser")
        book_articles = soup.find_all("article", class_="product_pod")
        for i, book in enumerate(cls.book_list):
            relative_url = book_articles[i].h3.a["href"]
            book["book_url"] = urljoin(BASE_URL + "catalogue/", relative_url)

    def test_scrape_not_empty(self):
        # Test that the book list is not empty
        self.assertTrue(len(self.book_list) > 0)

    def test_books_fields(self):
        # Test that each book has all required fields
        for book in self.book_list:
            self.assertIn("title", book)
            self.assertIn("price", book)
            self.assertIn("rating", book)
            self.assertIn("image_url", book)
            self.assertIn("book_url", book)

    def test_book_urls_exist(self):
        # Test that book_url exists and is not empty
        for book in self.book_list:
            self.assertTrue(book["book_url"])

    def test_book_urls_format(self):
        # Test that each book_url is a valid URL format
        for book in self.book_list:
            url = book["book_url"]
            self.assertTrue(re.match(r"^https?://", url), msg=f"Invalid URL: {url}")

    def test_types(self):
        # Test the data types of each field
        for book in self.book_list:
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["price"], float)
            self.assertIsInstance(book["rating"], int)
            self.assertIsInstance(book["image_url"], str)
            self.assertIsInstance(book["book_url"], str)


if __name__ == "__main__":
    unittest.main()