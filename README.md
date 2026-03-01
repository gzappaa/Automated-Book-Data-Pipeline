# Automated Book Data Pipeline

## Overview
This project scrapes book data from Books to Scrape, calculates analytics, and generates reports in PDF and Excel formats. Unit tests ensure data integrity.

## Features
Scrapes:

Title

Price

Rating

Image URL

Cleans and converts price to float

Converts star rating to integer

Calculates analytics:

Total books

Average, min, max prices

Most expensive & cheapest books

Saves data in JSON format

Generates:

PDF report

Excel report

Includes unit tests using unittest

Easily extensible (image download, extra analytics, etc.)

## Project Structure

``` 
Automated-Book-Data-Pipeline/
│
├── data/
│
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── analytics.py
│   ├── report.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_scraper.py
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

