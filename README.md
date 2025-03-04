# Hites Product Comment Scraper

This project is a Python-based web scraping tool using Selenium to extract product review data from the chilean retail website "hites.com." The script collects product review details, such as the product's category, the author's name, the review text, and the rating given by the author. This information is scraped from multiple product pages based on URLs provided in `test_hites_urls.txt` and saved in a CSV file `hites_comments.csv`.

## 1. Prerequisites

* Python 3.12.9
* Required Python packages (install with `pip install -r requirements.txt`)

## 2. Usage

1.  Place the product URLs you want to scrape in `content/test_hites_urls.txt`, one URL per line.
2.  Run the script: `python hites_scraper.py`.
3.  The scraped comments will be saved in `content/hites_comments.csv`.

## 3. `hites_comments.csv` Structure

* `category`: The product's department.
* `author`: The reviewer's name.
* `text`: The review text.
* `rating`: The reviewer's rating (1-5 stars).

Example CSV Output:

|category| author|	text|	rating|
|---|---|---|---|
|technology|	John Doe|	"Great tablet, really useful for daily tasks."|	5.0 star rating|
|home|	Jane Smith|	"Very comfortable chair, but it could use more support."|	4.0 star rating|
|technology|	Mark Lee|	"Decent laptop, good for light work but a bit slow."|	3.0 star rating|

## 4. File Structure
```
hites-web-scraper/
│
├── content/
│   ├── test_hites_urls.txt        # List of product URLs to scrape
│   └── hites_comments.csv         # Output CSV file containing scraped reviews
│
├── hites_scraper.py               # Python script that performs the scraping
├── requirements.txt               # List of Python dependencies
└── README.md                      # Project documentation
```