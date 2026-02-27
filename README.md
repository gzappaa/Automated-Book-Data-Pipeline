# Automated Book Data Pipeline

## Overview
This project scrapes book data from [Books to Scrape](https://books.toscrape.com/), processes it, and saves it in structured formats. It also includes unit tests to ensure data integrity.

## Features
- Scrapes:
  - Title
  - Price
  - Rating
  - Image URL
- Cleans and converts price to float
- Converts star rating to integer
- Saves data in `JSON` format
- Includes unit tests using `unittest`
- Designed to be easily extended (image download, PDF report, etc.)

## Project Structure

``` 
Automated-Book-Data-Pipeline/
│
├── data/ # scraped JSON will be saved here
│
├── src/
│ ├── init.py
│ └── scraper.py # main scraper code
│
├── tests/
│ ├── init.py
│ └── test_scraper.py # main scraper code
│
├── README.md
└── requirements.txt
```

## Getting Started

1. **Clone the repo**
```
git clone https://github.com/gzappaa/Automated-Book-Data-Pipeline
cd Automated-Book-Data-Pipeline
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Run the scraper**

```
python -m src.scraper
```

