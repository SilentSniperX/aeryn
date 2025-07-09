from fastapi import FastAPI
from news_handler import fetch_and_parse_news

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Aeryn News API"}

@app.get("/news")
def get_news():
    news = fetch_and_parse_news()
    return news
