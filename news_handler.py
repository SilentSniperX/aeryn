import os
import requests
from datetime import datetime, timedelta

MARKETAUX_API_TOKEN = os.getenv("MARKETAUX_API_TOKEN")

def get_marketaux_news():
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)
    published_after = int(one_day_ago.timestamp())

    url = (
        f"https://api.marketaux.com/v1/news/all?"
        f"api_token={MARKETAUX_API_TOKEN}"
        f"&language=en&limit=10&published_after={published_after}"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return data.get("data", [])

def fetch_and_parse_news():
    try:
        raw_news = get_marketaux_news()
        parsed = []

        for item in raw_news:
            parsed.append({
                "uuid": item.get("uuid"),
                "title": item.get("title"),
                "description": item.get("description"),
                "keywords": item.get("keywords"),
                "snippet": item.get("snippet"),
                "url": item.get("url"),
                "image_url": item.get("image_url"),
                "language": item.get("language"),
                "published_at": item.get("published_at"),
                "source": item.get("source")
            })

        return parsed
    except Exception as e:
        return [{"error": str(e)}]
