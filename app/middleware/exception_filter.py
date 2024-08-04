from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from app.config.logger_config import get_logger

logger = get_logger()

async def httpexception_handler(request: Request, exc: FastAPIHTTPException):
    logger.error(f"HTTPException occurred: {exc.status_code} - {exc.detail}")
    logger.error(f"Failed method {request.method} at URL {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "status_code": exc.status_code,
            "message": exc.detail,
            "detail": (
                f"Failed method {request.method} at URL {request.url}."
            )
        },
    )

async def exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception occurred: {exc!r}")
    logger.error(f"Failed method {request.method} at URL {request.url}")
    logger.exception("Exception traceback:")
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "status_code": 500,
            "message": "Internal Server Error",
            "detail": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        }
    )