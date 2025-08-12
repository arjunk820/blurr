from fastapi import FastAPI
from app.routers.health import health_router
from app.routers.upload import upload_router
from app.core.middleware import LoggingMiddleware

app = FastAPI()

app.include_router(health_router)
app.include_router(upload_router)
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}