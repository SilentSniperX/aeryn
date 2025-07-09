import os, requests
from datetime import datetime, timedelta

def fetch_news():
    key = os.getenv("NEWSAPI_KEY")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "language": "en",
        "pageSize": 10,
        "apiKey": key
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("articles", [])
    except Exception as e:
        return [{"error": str(e)}]

from fastapi import APIRouter
router = APIRouter()

@router.get("/news")
def news_handler():
    articles = fetch_news()
    return {"news": articles}
