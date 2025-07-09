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
        "published_after": int((datetime.utcnow() - timedelta(hours=1)).timestamp())
    })
    resp.raise_for_status()
    return resp.json().get("data", [])

def get_finnhub_news(limit=10):
    resp = requests.get(FINNHUB_URL, params={
        "category": "general",
        "token": os.getenv("FINNHUB_API_KEY")
    })
    resp.raise_for_status()
    return resp.json()[:limit]

def analyze_sentiment(headline: str):
    l = headline.lower()
    score = 0
    tags = []
    if any(x in l for x in ["fed", "federal reserve"]):
        score -= 2
        tags.append("HIGH_ALERT")
    if any(x in l for x in ["earnings beat", "guidance"]):
        score += 2
        tags.append("BULLISH")
    if any(x in l for x in ["layoff", "missed earnings"]):
        score -= 2
        tags.append("BEARISH")
    return score, tags

def fetch_and_parse_news():
    mat = get_marketaux_news()
    fhb = get_finnhub_news()
    items = []
    seen = set()

    for article in mat + fhb:
        title = article.get("title")
        url = article.get("url") or article.get("newsUrl")
        if not title or not url:
            continue
        if url in seen:
            continue
        seen.add(url)

        score, tags = analyze_sentiment(title)
        items.append({
            "title": title,
            "url": url,
            "published": article.get("published_at") or article.get("datetime"),
            "score": score,
            "tags": tags
        })

    return items

if __name__ == "__main__":
    print(fetch_and_parse_news())
