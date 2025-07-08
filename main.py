from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Aeryn is live, watching the charts..."}
