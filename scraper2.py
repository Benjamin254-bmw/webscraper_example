import requests
import json
import csv
import sqlite3
from bs4 import BeautifulSoup
import logging
import time

# Set up logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base URL of Hacker News
BASE_URL = "https://news.ycombinator.com/"

# Function to fetch the webpage
def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the page: {e}")
        print("Failed to fetch webpage. Check logs for details.")
        return None

# FIX: Update function to correctly extract headlines
def extract_headlines(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.select("span.titleline > a")  # FIX: Correct selector for headlines
    return [title.get_text(strip=True) for title in titles]

# FIX: Update function to correctly find the "More" button
def find_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.find("a", string="More")  # FIX: Use 'string' instead of 'text'
    if next_page:
        return "https://news.ycombinator.com/" + next_page["href"]    
    return None

# Function to save data in CSV
def save_to_csv(data, filename="data/headlines.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Headline"])
        for row in data:
            writer.writerow([row])
            logging.info(f"Saved {len(data)} headlines to {filename}")

# Function to save data in JSON
def save_to_json(data, filename="data/headlines.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        logging.info(f"Saved {len(data)} headlines to {filename}")

# Function to save data in SQLite database
def save_to_db(data, db_name="database/headlines.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, headline TEXT)")
    for row in data:
        cursor.execute("INSERT INTO news (headline) VALUES (?)", (row,))
    conn.commit()
    conn.close()
    logging.info(f"Saved {len(data)} headlines to database {db_name}")

# Function to scrape multiple pages
def scrape_multiple_pages(start_url, max_pages=3):
    url = start_url
    all_headlines = []
    page_count = 0

    while url and page_count < max_pages:
        print(f"Scraping Page {page_count + 1}: {url}")
        html = fetch_page(url)    
        if not html:
            break
        headlines = extract_headlines(html)
        all_headlines.extend(headlines)

        url = find_next_page(html)  # Get next page URL
        page_count += 1

        time.sleep(2)  # Pause to avoid overwhelming the server
    return all_headlines

# Main script execution
if __name__ == "__main__":
    print("Starting multi-page web scraper...")

headlines = scrape_multiple_pages(BASE_URL, max_pages=3)

if headlines:
    save_to_csv(headlines)
    save_to_json(headlines)
    save_to_db(headlines)
    print(f"Scraped and saved {len(headlines)} headlines from multiple pages successfully!")

else:

    print("No headlines found.")

