import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://quotes.toscrape.com/page/{}/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_page(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def parse_quotes(soup):
    quotes_data = []
    for block in soup.select("div.quote"):
        text = block.select_one("span.text").get_text(strip=True)
        author = block.select_one("small.author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.select("div.tags a")]
        quotes_data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })
    return quotes_data

def scrape_all(pages=3):
    results = []
    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        print(f"Собираем данные со страницы {page}...")
        soup = get_page(url)
        results.extend(parse_quotes(soup))
    return results

def save_csv(data, filename="quotes.csv"):
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    data = scrape_all(pages=3)
    save_csv(data)
    print("✅ Данные сохранены в quotes.csv")

if __name__ == "__main__":
    main()
