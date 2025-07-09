import os
import requests
from datetime import datetime, timedelta

def fetch_and_parse_news():
    marketaux_api_key = os.getenv("MARKETAUX_API_KEY")
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")

    published_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())

    marketaux_url = (
        f"https://api.marketaux.com/v1/news/all"
        f"?api_token={marketaux_api_key}&language=en&limit=10&published_after={published_after}"
    )
    finnhub_url = (
        f"https://finnhub.io/api/v1/news?category=general&token={finnhub_api_key}"
    )

    news_data = {
        "marketaux_news": [],
        "finnhub_news": []
    }

    try:
        response = requests.get(marketaux_url)
        response.raise_for_status()
        marketaux_results = response.json().get("data", [])
        news_data["marketaux_news"] = marketaux_results
    except Exception as e:
        news_data["marketaux_news"] = [{"error": str(e)}]

    try:
        response = requests.get(finnhub_url)
        response.raise_for_status()
        finnhub_results = response.json()
        news_data["finnhub_news"] = finnhub_results
    except Exception as e:
        news_data["finnhub_news"] = [{"error": str(e)}]

    return news_data
