import os
import requests
import time

class NewsFetcher:
    def __init__(self):
        self.marketaux_api_key = os.environ.get("MARKETAUX_API_KEY")

    def get_marketaux_news(self):
        # Use current time minus 1 day (safe fallback)
        timestamp = int(time.time()) - 86400
        url = (
            f"https://api.marketaux.com/v1/news/all?"
            f"api_token={self.marketaux_api_key}&language=en&limit=10&published_after={timestamp}"
        )
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])

    def fetch_and_parse_news(self):
        marketaux = self.get_marketaux_news()
        return {"news": marketaux}
