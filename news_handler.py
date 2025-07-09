import os
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

MARKETAUX_API_TOKEN = os.getenv("MARKETAUX_API_TOKEN")

def get_marketaux_news():
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)
    published_after = int(one_day_ago.timestamp())

    url = (
        f"https://api.marketaux.com/v1/news/all?"
        f"api_token={MARKETAUX_API_TOKEN}"
        f"&language=en&limit=10"
        f"&published_after={published_after}"
    )

    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("data", [])

@router.get("/news")
def fetch_and_parse_news():
    try:
        news_data = get_marketaux_news()
        filtered = [
            {
                "title": item.get("title"),
                "source": item.get("source"),
                "published_at": item.get("published_at"),
                "url": item.get("url"),
                "description": item.get("description") or item.get("snippet", "")
            }
            for item in news_data
            if item.get("title") and item.get("published_at")
        ]
        return {"news": filtered}
    except Exception as e:
        return {"error": str(e)}
