from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from news_handler import fetch_finnhub_news

app = FastAPI()

# Mount static directory (this line assumes there's a 'static' folder in root)
app.mount("static", StaticFiles(directory="static"), name="static")

# Use the templates folder (direct in root)
templates = Jinja2Templates(directory="templates")

@app.get("/news")
async def get_news(request: Request):
    news = await fetch_finnhub_news()
    return templates.TemplateResponse("news.html", {"request": request, "news": news})
