from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from ..config.exception_logging_config import logger

class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all exceptions in FastAPI"""
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            logger.error(f"HTTPException: {http_exc.detail} - Status Code: {http_exc.status_code}")
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"error": http_exc.detail},
            )
        except Exception as exc:
            logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error"},
            )