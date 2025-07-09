from fastapi import FastAPI
from news_handler import NewsFetcher

app = FastAPI()
news_fetcher = NewsFetcher()

@app.get("/news")
def get_news():
    marketaux_news = news_fetcher.get_marketaux_news()
    finnhub_news = news_fetcher.get_finnhub_news()
    return {
        "marketaux_news": marketaux_news["news"],
        "finnhub_news": finnhub_news["news"]
    }
