import os
import requests
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/news?category=general"

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    news_data = {}

    if FINNHUB_API_KEY:
        try:
            response = requests.get(
                FINNHUB_URL,
                headers={"X-Finnhub-Token": FINNHUB_API_KEY}
            )
            response.raise_for_status()
            news_data["finnhub_news"] = response.json()
        except requests.RequestException as e:
            news_data["finnhub_news"] = [{"error": str(e)}]
    else:
        news_data["finnhub_news"] = [{"error": "Missing FINNHUB_API_KEY"}]

    return templates.TemplateResponse("news.html", {"request": request, **news_data})
