import os
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter

router = APIRouter()

@router.get("/news")
def get_news():
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        return {"error": "Missing FINNHUB_API_KEY"}

    url = "https://finnhub.io/api/v1/news"
    params = {
        "category": "general",  # other options: forex, crypto, merger
        "token": api_key
    }

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return {"finnhub_news": resp.json()}
    except requests.HTTPError as e:
        return {"finnhub_news": [{"error": str(e)}]}
