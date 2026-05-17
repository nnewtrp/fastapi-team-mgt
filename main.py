from fastapi import FastAPI

from teams import router as teams_router

app = FastAPI()
app.include_router(teams_router)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}
