import requests
from bs4 import BeautifulSoup

# Your RSS Source
RSS_URL = "https://www.thehindu.com/news/national/?service=rss"

# PASTE YOUR WEB APP URL HERE
# It should look like https://script.google.com/macros/s/.../exec
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwQhmfIqVtmkdYzE2qqJvh-Is4IhoAcV0IWYlKTFMkGChjOjP-7gu48Fu2BQ1NbBiuE/exec"

def fetch_articles():
    try:
        response = requests.get(RSS_URL, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        
        articles = []
        # Taking the latest 5 articles
        for item in items[:5]:
            articles.append({
                "source": "The Hindu",
                "headline": item.title.text.strip() if item.title else "No Title",
                "link": item.link.text.strip() if item.link else "No Link",
                "published": item.pubDate.text.strip() if item.pubDate else "No Date"
            })
        return articles
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

if __name__ == "__main__":
    news_data = fetch_articles()
    
    if news_data:
        print(f"Found {len(news_data)} articles. Sending to Google Sheets...")
        # We send the whole list because your Apps Script expects data.map()
        response = requests.post(WEBAPP_URL, json=news_data)
        print(f"Server Response: {response.text}")
    else:
        print("No new articles to send.")
