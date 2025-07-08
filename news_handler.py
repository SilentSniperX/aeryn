import os
import requests
from datetime import datetime, timedelta

MARKETAUX_URL = "https://api.marketaux.com/v1/news/all"
FINNHUB_URL = "https://finnhub.io/api/v1/news"

def get_marketaux_news(limit=10):
    resp = requests.get(MARKETAUX_URL, params={
        "api_token": os.getenv("MARKETAUX_API_KEY"),
        "language": "en",
        "limit": limit,
        "published_after": (datetime.utcnow() - timedelta(hours=6)).isoformat()
    })
    return resp.json().get("data", [])

def get_finnhub_news(limit=10):
    resp = requests.get(FINNHUB_URL, params={
        "category": "general",
        "token": os.getenv("FINNHUB_API_KEY")
    })
    data = resp.json()
    return data if isinstance(data, list) else []

def analyze_sentiment(headline):
    l = headline.lower()
    score = 0
    alerts = []
    if any(x in l for x in ["fed", "federal reserve", "interest rate", "inflation"]):
        score -= 2
        alerts.append("HIGH_ALERT")
    if any(x in l for x in ["earnings beat", "guidance raised", "record revenue"]):
        score += 2
        alerts.append("BULLISH")
    if any(x in l for x in ["layoff", "missed earnings", "profit warning"]):
        score -= 2
        alerts.append("BEARISH")
    return score, alerts

def fetch_and_parse_news():
    items = []
    all_articles = get_marketaux_news() + get_finnhub_news()
    for article in all_articles:
        url = article.get("url") or article.get("headline", "")
        title = article.get("title") or article.get("headline", "")
        ts = article.get("published_at") or article.get("datetime", "")
        score, tags = analyze_sentiment(title)
        items.append({
            "title": title,
            "url": url,
            "published": ts,
            "score": score,
            "tags": tags
        })
    return items
