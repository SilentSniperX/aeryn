import os
import requests
from datetime import datetime, timedelta

def fetch_and_parse_news():
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_key:
        return {"finnhub_news": [{"error": "Missing FINNHUB_API_KEY"}]}

    published_after = int((datetime.utcnow() - timedelta(hours=24)).timestamp())
    url = (
        "https://finnhub.io/api/v1/news?"
        f"category=top&token={finnhub_key}"
    )

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return {"finnhub_news": resp.json()}
    except Exception as e:
        return {"finnhub_news": [{"error": str(e)}]}
