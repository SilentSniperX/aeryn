import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")

def get_finnhub_news():
    if not FINNHUB_API_KEY:
        return {"error": "FINNHUB_API_KEY not set"}
    
    url = "https://finnhub.io/api/v1/news?category=general&token=" + FINNHUB_API_KEY
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_marketaux_news():
    if not MARKETAUX_API_KEY:
        return {"error": "MARKETAUX_API_KEY not set"}

    # Get news from the last 24 hours
    published_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())

    url = f"https://api.marketaux.com/v1/news/all?api_token={MARKETAUX_API_KEY}&language=en&limit=10&published_after={published_after}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        return {"error": str(e)}

def fetch_and_parse_news():
    finnhub_news = get_finnhub_news()
    marketaux_news = get_marketaux_news()

    return {
        "finnhub_news": finnhub_news,
        "marketaux_news": marketaux_news,
    }
