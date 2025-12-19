from fastapi import Request #type: ignore
from fastapi.responses import JSONResponse #type: ignore
from app.core.logger import logger

async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)

    except Exception as e:
        logger.error(f"ERROR: {str(e)}", exc_info=True)

        return JSONResponse(
            content={"detail": "Internal server error"},
            status_code=500
        )
