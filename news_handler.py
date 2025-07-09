import os
import requests

class NewsFetcher:
    def __init__(self):
        self.marketaux_api_key = os.environ.get("MARKETAUX_API_KEY")

    def get_marketaux_news(self):
        url = (
            f"https://api.marketaux.com/v1/news/all?"
            f"api_token={self.marketaux_api_key}&language=en&limit=10"
        )
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])

    def fetch_and_parse_news(self):
        news_data = self.get_marketaux_news()
        return {"news": news_data}
