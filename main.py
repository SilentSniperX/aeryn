from fastapi import FastAPI
from news_handler import fetch_and_parse_news

app = FastAPI()

@app.get("/news")
def get_news():
    return {"news": fetch_and_parse_news()}
