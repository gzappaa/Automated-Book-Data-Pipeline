import unittest
from src.scraper import get_book_list, get_book_details


class TestBookDetailsReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # pega um livro real do site
        book_list = get_book_list()
        cls.book_url = book_list[0]["book_url"]

        # pega os detalhes reais
        cls.details = get_book_details(cls.book_url)
        cls.table = cls.details["table_data"]

    def test_table_fields_exist(self):
        self.assertIn("UPC", self.table)
        self.assertIn("Product Type", self.table)
        self.assertIn("Price (excl. tax)", self.table)
        self.assertIn("Price (incl. tax)", self.table)
        self.assertIn("Tax", self.table)
        self.assertIn("Availability", self.table)
        self.assertIn("Number of reviews", self.table)

    def test_types(self):
        self.assertIsInstance(self.table["UPC"], str)
        self.assertIsInstance(self.table["Product Type"], str)
        self.assertIsInstance(self.table["Price (excl. tax)"], float)
        self.assertIsInstance(self.table["Price (incl. tax)"], float)
        self.assertIsInstance(self.table["Tax"], float)
        self.assertIsInstance(self.table["Availability"], str)
        self.assertIsInstance(self.table["Number of reviews"], int)


if __name__ == "__main__":
    unittest.main()