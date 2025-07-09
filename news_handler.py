import os
import requests
from datetime import datetime, timedelta

def fetch_and_parse_news():
    news_data = {
        "finnhub_news": [],
        "newsapi": []
    }

    # 📈 Finnhub
    try:
        finnhub_key = os.getenv("FINNHUB_API_KEY")
        finnhub_url = "https://finnhub.io/api/v1/news"
        params = {"category": "top"}  # you can customize category
        headers = {"X-Finnhub-Key": finnhub_key}
        r = requests.get(finnhub_url, params=params, headers=headers)
        r.raise_for_status()
        news_data["finnhub_news"] = r.json()
    except Exception as e:
        news_data["finnhub_news"] = [{"error": str(e)}]

    # 📰 NewsAPI (top US business headlines)
    try:
        api_key = os.getenv("NEWSAPI_API_KEY")
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "category": "business",
            "apiKey": api_key,
            "pageSize": 10
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        articles = r.json().get("articles", [])
        news_data["newsapi"] = [
            {
                "source": a.get("source", {}).get("name"),
                "title": a.get("title"),
                "url": a.get("url"),
                "image": a.get("urlToImage"),
                "summary": a.get("description")
            }
            for a in articles
        ]
    except Exception as e:
        news_data["newsapi"] = [{"error": str(e)}]

    return news_data
