import re
import unittest
from src.scraper import get_all_books, get_soup, get_book_details

class TestBookScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run the scraper once for the entire test class
        cls.book_list = get_all_books()  # <-- changed from get_book_list()
        cls.details_list = [get_book_details(book["book_url"]) for book in cls.book_list]

    def test_catalogue_size(self):
        # Test if the total number of books across all pages is 1000
        self.assertEqual(len(self.__class__.book_list), 50 * 20)


    def test_get_soup(self):
        # Test if get_soup returns a BeautifulSoup object
        soup = get_soup("https://books.toscrape.com/")
        self.assertEqual(soup.__class__.__name__, "BeautifulSoup")

    def test_book_details_fetchable(self):
        # Test if each book detail is a dictionary and has expected keys
        for details in self.__class__.details_list:
            self.assertIsInstance(details, dict)
            self.assertIn("description", details)
            self.assertIn("availability", details)
            self.assertIn("table_data", details)

    def test_book_urls_exist(self):
        # Test if each book has a 'book_url' field and it's not empty
        for book in self.__class__.book_list:
            self.assertIn("book_url", book)
            self.assertTrue(book["book_url"])

    def test_scrape_not_empty(self):
        # Test that the book list is not empty
        self.assertTrue(len(self.__class__.book_list) > 0)

    def test_book_urls_format(self):
        # Test if each book_url is a valid URL format
        for book in self.__class__.book_list:
            url = book["book_url"]
            self.assertTrue(re.match(r"^https?://", url),
                            msg=f"Invalid URL: {url}")

    def test_books_fields(self):
        # Test if each book has all required fields
        for book in self.__class__.book_list:
            self.assertIn("title", book)
            self.assertIn("price", book)
            self.assertIn("rating", book)
            self.assertIn("image_url", book)

    def test_types(self):
        # Test the data types of each field
        for book in self.__class__.book_list:
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["price"], float)
            self.assertIsInstance(book["rating"], int)
            self.assertIsInstance(book["image_url"], str)


if __name__ == "__main__":
    unittest.main()