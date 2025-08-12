from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import uuid
from app.core.logging import log_request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        log_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration_ms, 2)
        )
        return response