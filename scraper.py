import requests
import json

from bs4 import BeautifulSoup

# URL of the website to scrape
URL = "https://www.bbc.com/news"

# Send a request to the website
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Find all headlines
headlines = soup.find_all("h3")

# Open a JSON file and write the data
data = [headline.get_text(strips=True) for headline in headlines]

with open("headlines.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
