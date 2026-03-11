import re
import unittest
from src.scraper import get_book_list, get_soup, get_book_details

class TestBookScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run the scraper once for the entire test class
        cls.book_list = get_book_list()
        cls.details_list = [get_book_details(book["book_url"]) for book in cls.book_list]

    def test_get_soup(self):
        from src.scraper import get_soup
        soup = get_soup("https://books.toscrape.com/")
        self.assertEqual(soup.__class__.__name__, "BeautifulSoup")

    # Test if each book has a book_url field and it's not empty
    def test_book_urls_exist(self):
        for book in self.book_list:
            self.assertIn("book_url", book)
            self.assertTrue(book["book_url"])  # not empty


    # Test if the scraper returns the expected number of books (20 per page)
    def test_catalogue_size(self):
        books = get_book_list()
        self.assertEqual(len(books), 20)


    # Test if each book_url is a valid URL format
    def test_book_urls_format(self):
        for book in self.book_list:
            url = book["book_url"]
            self.assertTrue(re.match(r"^https?://", url),
                            msg=f"Invalid URL: {url}")

    # Test if the book list is not empty
    def test_scrape_not_empty(self):
        self.assertTrue(len(self.book_list) > 0)

    # Test if each book has all required fields
    def test_books_fields(self):
        for book in self.book_list:
            self.assertIn("title", book)
            self.assertIn("price", book)
            self.assertIn("rating", book)
            self.assertIn("image_url", book)
    
    # Test the data types of each field
    def test_types(self):
        for book in self.book_list:
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["price"], float)
            self.assertIsInstance(book["rating"], int)
            self.assertIsInstance(book["image_url"], str)



if __name__ == "__main__":
    unittest.main()