import os

from fastapi import FastAPI
from dotenv import load_dotenv
from teams import router as teams_router

load_dotenv()

app = FastAPI()
app.include_router(teams_router, prefix=os.environ["API_PREFIX"])

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}
