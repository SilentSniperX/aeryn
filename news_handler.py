import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class NewsFetcher:
    def __init__(self):
        self.markettaux_token = os.getenv("MARKETAUX_API_KEY")
        self.api_url = "https://api.marketaux.com/v1/news/all"

    def get_marketaux_news(self):
        published_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())
        params = {
            "api_token": self.markettaux_token,
            "language": "en",
            "limit": 10,
            "published_after": published_after
        }
        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

def fetch_and_parse_news():
    fetcher = NewsFetcher()
    raw_news = fetcher.get_marketaux_news()
    parsed_news = []
    for article in raw_news:
        parsed_news.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "published_at": article.get("published_at"),
            "source": article.get("source")
        })
    return parsed_news
