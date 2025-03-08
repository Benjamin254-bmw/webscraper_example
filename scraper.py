import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
URL = "https://www.bbc.com/news"

# Send a request to the website
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Find all headlines
headlines = soup.find_all("h3")

# Save the headlines
with open("headlines.txt", "w", encoding="utf-8") as file:
    for headline in headlines:
        text = headline.get_text(strip=True)
        print(text)
        file.write(text + "\n")

print("Headlines saved to headlines.txt")

