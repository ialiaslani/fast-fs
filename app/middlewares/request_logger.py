from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.modules.common.elastic import configure_logger

# Initialize the logger
logger = configure_logger()

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        start_time = time.time()
        logger.info({
            "event": "request",
            "method": request.method,
            "url": request.url.path,
            "client": request.client.host,
            "headers": dict(request.headers),
        })

        # Process the request
        response = await call_next(request)

        # Log response details
        process_time = time.time() - start_time
        logger.info({
            "event": "response",
            "status_code": response.status_code,
            "url": request.url.path,
            "client": request.client.host,
            "processing_time": f"{process_time:.4f}s",
        })

        return response
