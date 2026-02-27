import unittest
from src.scraper import get_book_list

class TestBookScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run the scraper once for the entire test class
        cls.book_list = get_book_list()

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