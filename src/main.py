# main.py
"""
Main pipeline for Automated Book Data Pipeline:
1. Scrape books from the website
2. Save scraped data to JSON
3. Calculate analytics/statistics
4. Generate a PDF report
"""

import os
import json
from .scraper import get_all_books, get_book_list_with_details
from .analytics import calculate_stats_from_json
from .report import generate_pdf, generate_excel
from .cover_downloader import download_images

# ===== Create data folder if it doesn't exist =====
os.makedirs("data", exist_ok=True)
os.makedirs("data/images", exist_ok=True)

# ===== Step 1: Scrape basic book data =====
print("Scraping basic book data...")
books = get_all_books()
books_json_path = "data/books.json"
with open(books_json_path, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)
print(f"{len(books)} books saved to {books_json_path}")

## ===== Step 2: Scrape book data & Download images =====
books_with_details = get_book_list_with_details()

# create books_raw.json
with open("data/books_raw.json", "w", encoding="utf-8") as f:
    json.dump(books_with_details, f, ensure_ascii=False, indent=4)
print(f"{len(books_with_details)} books with details saved to data/books_raw.json")

## ===== Download book images =====  
print("Downloading book images...")
download_images(books_with_details, folder="data/images")

## ===== Step 3: Save scraped data to JSON =====
books_json_path = "data/books.json"
with open(books_json_path, "w", encoding="utf-8") as f:
    json.dump(books_with_details, f, ensure_ascii=False, indent=4)
print(f"Book data saved to {books_json_path}")

# ===== Step 4: Calculate analytics =====
print("Calculating analytics...")
stats = calculate_stats_from_json(books_json_path)
print("Analytics calculated successfully.")

# ===== Step 5: Generate PDF report + Excel report =====
report_path = "data/book_report.pdf"
print("Generating PDF report...")
generate_pdf(stats, output_path=report_path)
print(f"PDF report generated successfully at {report_path}")
generate_excel(stats, output_path="data/book_report.xlsx")

# ===== Pipeline complete =====
print("Pipeline executed successfully!")