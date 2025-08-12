from fastapi import FastAPI
from routers.health import router

app = FastAPI()

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}