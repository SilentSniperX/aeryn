import os
import requests
from datetime import datetime, timedelta

def fetch_and_parse_news():
    token = os.getenv("MARKETAUX_API_TOKEN")
    if not token:
        raise RuntimeError("Missing environment variable MARKETAUX_API_TOKEN")

    published_after = int(datetime.utcnow().timestamp()) - 24*3600
    url = (
        "https://api.marketaux.com/v1/news/all"
        f"?language=en&limit=10&published_after={published_after}"
        f"&api_token={token}"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
    except Exception as e:
        return [{"error": str(e)}]

    return data
