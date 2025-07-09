from fastapi import FastAPI
from news_handler import NewsFetcher

app = FastAPI()
news_fetcher = NewsFetcher()

@app.get("/")
def read_root():
    return {"message": "Aeryn is live, watching the markets."}

@app.get("/news")
async def get_news():
    data = news_fetcher.fetch_and_parse_news()
    return data
