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

def get_finnhub_news():
    resp = requests.get(FINNHUB_URL, params={
        "category": "general",
        "token": os.getenv("FINNHUB_API_KEY")
    })
    return resp.json()  # If this returns a list directly, you’re good. Otherwise adjust like below:
    # return resp.json().get("data", []) if it's a dict with "data" key

def analyze_sentiment(headline):
    l = headline.lower()
    score = 0
    alerts = []
    if any(x in l for x in ["fed", "federal reserve", "rate hike", "inflation"]):
        score -= 2; alerts.append("HIGH_ALERT")
    if any(x in l for x in ["earnings beat", "guidance raised", "profit surge"]):
        score += 2; alerts.append("BULLISH")
    if any(x in l for x in ["layoff", "missed earnings", "cut forecast"]):
        score -= 2; alerts.append("BEARISH")
    return score, alerts

def fetch_and_parse_news():
    items = []
    for article in get_marketaux_news() + get_finnhub_news():
        url = article.get("url") or article.get("headline")
        title = article.get("title") or article.get("headline")
        ts = article.get("published_at") or article.get("datetime")
        score, tags = analyze_sentiment(title)
        items.append({
            "title": title,
            "url": url,
            "timestamp": ts,
            "sentiment": score,
            "tags": tags
        })
    return items
