import traceback
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError


class CustomErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Continue processing the request
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            # Catch HTTPException errors
            logging.error(f"HTTP error occurred: {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"success": False, "detail": exc.detail},
            )
        except RequestValidationError as exc:
            # Handle validation errors
            logging.error(f"Validation error occurred: {exc.errors()}")
            return JSONResponse(
                status_code=422,
                content={"success": False, "detail": exc.errors()},
            )
        except Exception as exc:
            # Log the stack trace for debugging purposes
            logging.error(f"An unexpected error occurred: {str(exc)}")
            logging.error(traceback.format_exc())
            # Return a generic error response
            return JSONResponse(
                status_code=500,
                content={"success": False, "detail": "Internal server error."},
            )
