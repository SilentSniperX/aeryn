from fastapi import FastAPI
from news_handler import fetch_and_parse_news

app = FastAPI()

@app.get("/news")
async def get_news():
    return fetch_and_parse_news()
