import time
from fastapi import Request #type: ignore
from app.core.logger import logger

async def logging_middleware(request: Request, call_next):
    start = time.time()

    logger.info(f"REQUEST: {request.method} {request.url}")

    response = await call_next(request)

    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"RESPONSE: {response.status_code} in {duration}ms")

    return response

