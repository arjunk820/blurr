from fastapi import APIRouter
from fastapi.responses import JSONResponse

health_router = APIRouter()

@health_router.get("/health", response_class=JSONResponse)
async def health():
        return {"status": "OK"}

@health_router.get("/version", response_class=JSONResponse)
async def version():
        return {"version":"0.1.0","python":"3.11"}

@health_router.get("/upload/health")
async def upload_health():
    return {"status": "ok", "message": "Upload service is healthy"}