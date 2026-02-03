import requests
from bs4 import BeautifulSoup

RSS_URL = "https://www.thehindu.com/news/national/?service=rss"

def fetch_articles():
    response = requests.get(RSS_URL)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")

    articles = []

    for item in items[:5]:
        articles.append({
            "source": "The Hindu",
            "headline": item.title.text.strip(),
            "link": item.link.text.strip(),
            "published": item.pubDate.text.strip()
        })

    return articles

if __name__ == "__main__":
    data = fetch_articles()
    for article in data:
        print(article)


