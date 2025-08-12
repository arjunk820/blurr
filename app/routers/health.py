from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health", response_class=JSONResponse)
async def health():
        return {"status": "ok"}

@router.get("/version", response_class=JSONResponse)
async def version():
        return {"version": "1.0.0"}