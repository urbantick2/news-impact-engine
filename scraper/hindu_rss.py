import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import os
import json

RSS_URL = "https://www.thehindu.com/news/national/?service=rss"

def fetch_articles():
    response = requests.get(RSS_URL)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    articles = []
    for item in items[:5]:
        articles.append([
            "The Hindu",
            item.title.text.strip(),
            item.link.text.strip(),
            item.pubDate.text.strip()
        ])
    return articles

def update_google_sheet(data):
    # 1. Authenticate using GitHub Secrets
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Load credentials from the environment variable
    creds_dict = json.loads(os.environ.get("GCP_SERVICE_ACCOUNT"))
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)

    # 2. Open the sheet (Make sure the Service Account Email is shared on this sheet!)
    # Replace 'Your Sheet Name' with the actual name of your Google Sheet
    sheet = client.open("News Impact Engine").sheet1 

    # 3. Avoid Duplicates (Optional but recommended)
    # Get all existing links in Column C
    existing_links = sheet.col_values(3) 

    for row in data:
        if row[2] not in existing_links:
            sheet.append_row(row)
            print(f"Added: {row[1]}")
        else:
            print(f"Skipped (Already exists): {row[1]}")

if __name__ == "__main__":
    articles = fetch_articles()
    if articles:
        update_google_sheet(articles)
    else:
        print("No articles found.")
