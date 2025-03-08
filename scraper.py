import requests
import json
import csv
import sqlite3
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# URL of the website to scrape
URL = "https://www.bbc.com/news"

# function to fetch the webpage
def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the page: {e}")
        print("Failed to fetch webpage. Check logs for details.")
        return None

# fuction to parse the page and extract headlines
def extract_headlines(html):
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.find_all("h3")
    return [headline.get_text(strip=True) for headline in headlines]

# function to save data in csv
def save_to_csv(data, filename="data/headlines.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Headline"])
        for row in data:
            writer.writerow([row])
    logging.info(f"saved {len(data)} headlines to {filename}")

# function to save data in JSON
def save_to_json(data, filename="data/headlines.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    with logging.info(f"saved {len(data)} headlines to {filename}")


# function to save data in SQLite database
def save_to_db(data, db_name="database/headlines.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, headline TEXT)")
    for row in data:
        cursor.execute("INSERT INTO news (headline) VALUES (?)", (row,))

    conn.commit()
    conn.close()
    logging.info(f"saved {len(data)} headlines to database {db_name}")

# main script execution
if __name__=="__main__":
    print("Starting web scraper...")
    
    html = fetch_page(URL)
    if html:
        headlines = extract_headlines(html)

        if headlines:
            save_to_csv(headlines)
            save_to_json(headlines)
            save_to_db(headlines)
            print(f"Scraped and saved {len(headlines)} headlines successfully!")
        else:
            print("No headlines found.")
    else:
        print("Could not retrieve the webpage.")

