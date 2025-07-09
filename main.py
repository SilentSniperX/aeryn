from fastapi import FastAPI
from news_handler import fetch_and_parse_news

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Service is up. Use /news to get news data."}

@app.get("/news")
def get_news():
    return {"news": fetch_and_parse_news()}
