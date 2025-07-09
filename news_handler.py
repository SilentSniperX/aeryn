import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict


class NewsFetcher:
    def __init__(self):
        pass

    def get_marketaux_news(self) -> List[Dict]:
        api_key = os.getenv("MARKETAUX_API_KEY")
        if not api_key:
            raise ValueError("MARKETAUX_API_KEY is not set.")

        url = "https://api.marketaux.com/v1/news/all"
        published_after = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"  # ISO 8601

        params = {
            "api_token": api_key,
            "language": "en",
            "limit": 10,
            "published_after": published_after
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

    def fetch_and_parse_news(self) -> Dict[str, List[Dict]]:
        try:
            marketaux_news = self.get_marketaux_news()
        except Exception as e:
            print(f"Error fetching news from marketaux: {e}")
            marketaux_news = []

        return {
            "news": marketaux_news
        }
