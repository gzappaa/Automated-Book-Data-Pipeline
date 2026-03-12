from pathlib import Path
import requests
import re
from concurrent.futures import ThreadPoolExecutor
import json

# ------------------------------
# Create a safe filename for all OS
# ------------------------------
def safe_filename(title: str) -> str:
    # Replace invalid characters and normalize spaces
    filename = re.sub(r'[<>:"/\\|?*]', '_', title)
    filename = re.sub(r'[\s_]+', '_', filename.strip().lower())
    return filename

# ------------------------------
# Download a single image
# ------------------------------
def download_image(book, folder, downloaded_urls):
    url = book["image_url"]

    # Skip duplicate URLs
    if url in downloaded_urls:
        return f"Skipped duplicate: {book['title']}"

    # Generate filepath
    filename = safe_filename(book['title']) + ".jpg"
    filepath = folder / filename

    # Skip if file already exists
    if filepath.exists():
        downloaded_urls.add(url)
        return f"Already exists: {filename}"

    try:
        # Download image
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        filepath.write_bytes(resp.content)
        downloaded_urls.add(url)
        return f"Downloaded: {filename}"

    except requests.RequestException as e:
        return f"Error downloading {filename}: {e}"

# ------------------------------
# Download all images using threads
# ------------------------------
def download_images(books, folder="data/images", max_workers=30):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    downloaded_urls = set()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda b: download_image(b, folder, downloaded_urls), books)
        for r in results:
            print(r)

# ------------------------------
# Run as script
# ------------------------------
if __name__ == "__main__":
    # Load the JSON with book details
    books_json_path = "data/books_with_details.json"
    with open(books_json_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    # Download all book images (parallelized)
    download_images(books, folder="data/images", max_workers=30)