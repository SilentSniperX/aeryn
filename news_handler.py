import os
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter

router = APIRouter()

@router.get("/news")
def fetch_finnhub_news():
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")

    # Get timestamp for 24 hours ago
    published_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())

    url = f"https://finnhub.io/api/v1/news?category=top&token={finnhub_api_key}"

    news_data = {
        "finnhub_news": []
    }

    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data["finnhub_news"] = response.json()
    except Exception as e:
        news_data["finnhub_news"] = [{"error": str(e)}]

    return news_data
