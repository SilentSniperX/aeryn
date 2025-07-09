import os
import requests
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self):
        self.marketaux_api_key = os.getenv("MARKETAUX_API_KEY")
        self.finnhub_api_key = os.getenv("FINNHUB_API_KEY")

    def get_marketaux_news(self):
        if not self.marketaux_api_key:
            return {"news": [{"error": "MARKETAUX_API_KEY not found"}]}

        url = "https://api.marketaux.com/v1/news/all"
        published_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())
        params = {
            "api_token": self.marketaux_api_key,
            "language": "en",
            "limit": 10,
            "published_after": published_after
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"news": data.get("data", [])}
        except requests.exceptions.HTTPError as e:
            return {"news": [{"error": f"{str(e)}"}]}
        except Exception as e:
            return {"news": [{"error": f"Unexpected error: {str(e)}"}]}

    def get_finnhub_news(self):
        if not self.finnhub_api_key:
            return {"news": [{"error": "FINNHUB_API_KEY not found"}]}

        url = "https://finnhub.io/api/v1/news"
        params = {
            "category": "general",
            "token": self.finnhub_api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"news": data[:10]}  # Get the latest 10 articles
        except requests.exceptions.HTTPError as e:
            return {"news": [{"error": f"{str(e)}"}]}
        except Exception as e:
            return {"news": [{"error": f"Unexpected error: {str(e)}"}]}
