import os
import requests
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("MARKETAUX_API_KEY")
        if not self.api_key:
            raise ValueError("MARKETAUX_API_KEY is not set in environment variables.")

    def get_marketaux_news(self):
        base_url = "https://api.marketaux.com/v1/news/all"
        published_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())
        params = {
            "api_token": self.api_key,
            "language": "en",
            "limit": 10,
            "published_after": published_after
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

def fetch_and_parse_news():
    fetcher = NewsFetcher()
    return fetcher.get_marketaux_news()
