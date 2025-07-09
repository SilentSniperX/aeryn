from fastapi import FastAPI
from news_handler import router as news_router

app = FastAPI()

app.include_router(news_router)
