import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict

class NewsFetcher:
    def __init__(self):
        self.sources = {
            "marketaux": self.get_marketaux_news,
            "finnhub": self.get_finnhub_news
        }

    def fetch_all_news(self) -> List[Dict]:
        all_news = []

        for name, fetch_function in self.sources.items():
            try:
                news_items = fetch_function()
                all_news.extend(news_items)
            except Exception as e:
                print(f"Error fetching news from {name}: {e}")

        return sorted(all_news, key=lambda x: x["published"], reverse=True)

    def get_marketaux_news(self) -> List[Dict]:
        api_key = os.getenv("MARKETAUX_API_KEY")
        if not api_key:
            raise ValueError("MARKETAUX_API_KEY is not set.")

        url = "https://api.marketaux.com/v1/news/all"
        params = {
            "api_token": api_key,
            "language": "en",
            "limit": 10,
            "published_after": int((datetime.utcnow() - timedelta(hours=1)).timestamp())
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        articles = response.json().get("data", [])
        return [
            {
                "title": a.get("title"),
                "url": a.get("url"),
                "published": a.get("published_at", ""),
                "score": a.get("overall_sentiment_score", 0),
                "tags": a.get("entities", [])
            }
            for a in articles
        ]

    def get_finnhub_news(self) -> List[Dict]:
        api_key = os.getenv("FINNHUB_API_KEY")
        if not api_key:
            raise ValueError("FINNHUB_API_KEY is not set.")

        url = "https://finnhub.io/api/v1/news"
        params = {
            "category": "general",
            "token": api_key
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        articles = response.json()
        return [
            {
                "title": a.get("headline"),
                "url": a.get("url"),
                "published": a.get("datetime"),
                "score": a.get("related", ""),
                "tags": []
            }
            for a in articles
        ]

def fetch_and_parse_news() -> Dict[str, List[Dict]]:
    fetcher = NewsFetcher()
    news = fetcher.fetch_all_news()
    return {"news": news}
