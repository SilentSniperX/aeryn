import os
import requests
from datetime import datetime, timedelta

MARKETAUX_URL = "https://api.marketaux.com/v1/news/all"
FINNHUB_URL = "https://finnhub.io/api/v1/news"

def get_marketaux_news():
    base_url = "https://api.marketaux.com/v1/news/all"
    current_time = int(time.time())
    params = {
        "api_token": os.getenv("MARKETAUX_API_KEY"),
        "language": "en",
        "limit": 10,
        "published_after": current_time - 86400  # 24 hours ago
    }

    resp = requests.get(base_url, params=params)
    resp.raise_for_status()

    news_items = resp.json().get("data", [])
    results = []
    for item in news_items:
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "published": item.get("published_at"),
            "score": 0,
            "tags": item.get("tickers", [])
        })

    return results
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
