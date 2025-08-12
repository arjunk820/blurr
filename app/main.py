from fastapi import FastAPI
from app.routers.health import router
from app.core.middleware import LoggingMiddleware

app = FastAPI()

app.include_router(router)
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}