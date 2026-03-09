from pathlib import Path
import requests

def download_images(books, folder="data/images"):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)

    for book in books:
        url = book["image_url"]
        # safe filename by replacing problematic characters
        filename = f"{book['title'].replace('/', '_').replace(':', '')}.jpg"
        filepath = folder / filename

        if filepath.exists():
            print(f"Already exists: {filename}")
            continue

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            filepath.write_bytes(resp.content)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Error downloading {filename}: {e}")