import asyncio
import time
import traceback
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from core.heatlh import health_check


REQUEST_TIMEOUT_ERROR = 120  # seconds


class CustomHealthCheckMiddleware(BaseHTTPMiddleware):
    bypass_routes = [
        "/v1/health"
    ]

    async def dispatch(self, request: Request, call_next):
        try:
            health_status = health_check()
            if health_status["status_code"] == 500:
                if request.url.path not in CustomHealthCheckMiddleware.bypass_routes:
                    return JSONResponse(
                        status_code=503,
                        content={
                            'detail': 'Service is unavailable! Try again later.',
                        },
                    )
            response = await call_next(request)
            return response
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=503,
                content={
                    'detail': 'Service is unavailable! Try again later.',
                },
            )


class CustomErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            logging.error(f"HTTP error occurred: {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"success": False, "detail": exc.detail},
            )
        except RequestValidationError as exc:
            logging.error(f"Validation error occurred: {exc.errors()}")
            return JSONResponse(
                status_code=422,
                content={"success": False, "detail": exc.errors()},
            )
        except Exception as exc:
            logging.error(f"An unexpected error occurred: {str(exc)}")
            logging.error(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={"success": False, "detail": "Internal server error."},
            )


class CustomTimeoutHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start_time = time.time()
            return await asyncio.wait_for(
                call_next(request),
                timeout=REQUEST_TIMEOUT_ERROR
            )
        except asyncio.TimeoutError:
            process_time = time.time() - start_time
            return JSONResponse(
                status_code=504,
                content={
                    'detail': 'Request processing time excedeed limit.',
                    'processing_time': process_time
                },
            )
