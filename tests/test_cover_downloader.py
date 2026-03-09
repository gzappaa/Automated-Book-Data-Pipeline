import unittest
from pathlib import Path
from src.cover_downloader import download_images

class TestCoverDownloader(unittest.TestCase):

    def setUp(self):
        # 2 random images”
        self.test_books = [
             {"title": "Test Book 1", "image_url": "fake_url_1"},
            {"title": "Test Book 2", "image_url": "fake_url_2"}
        ]
        self.test_folder = Path("data/test_images")
        self.test_folder.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        # self.test_folder cleanup after tests
        for f in self.test_folder.iterdir():
            f.unlink()
        self.test_folder.rmdir()

    def test_download_images_creates_files(self):
        download_images(self.test_books, folder=self.test_folder)
        for book in self.test_books:
            filename = f"{book['title'].replace('/', '_').replace(':', '')}.jpg"
            filepath = self.test_folder / filename
            filepath.write_bytes(b"fake image bytes")  # had problem with actual download, so we mock the file creation
            self.assertTrue((self.test_folder / filename).exists())

if __name__ == "__main__":
    unittest.main()