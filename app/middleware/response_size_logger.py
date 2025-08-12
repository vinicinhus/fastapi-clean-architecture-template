import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class ResponseSizeLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        # Read the response body
        body = b""
        async for chunk in response.__dict__.get("body_iterator", []):
            body += chunk

        if not body and hasattr(response, "body"):
            body = response.body

        size_kb = len(body) / 1024
        duration = time.time() - start_time

        logger.info(
            f"Route: {request.method} {request.url.path} | Time: {duration:.2f}s | "
            f"Response Size: {size_kb:.2f} KB"
        )

        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
