from fastapi import FastAPI
from news_handler import fetch_and_parse_news
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Aeryn is live, watching the charts..."}
@app.get("/news")
async def news():
    data = fetch_and_parse_news()
    return {"news": sorted(data, key=lambda x: x["score"], reverse=True)}
