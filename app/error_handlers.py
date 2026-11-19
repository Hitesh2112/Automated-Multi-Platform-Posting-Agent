"""
FastAPI error and exception handlers.
"""
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppException, ErrorContainer, ErrorDetail, ErrorResponse

logger = logging.getLogger("multi_platform_posting.errors")


def register_error_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI application."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Transform Pydantic and FastAPI validation errors into a clean, uniform schema."""
        details = []
        for err in exc.errors():
            # Get field name, omitting 'body' if present
            loc = [str(x) for x in err.get("loc", []) if str(x) != "body"]
            field_name = ".".join(loc) if loc else None
            msg = err.get("msg", "Invalid value")

            # Remove Pydantic's "Value error, " prefix if present for cleaner message
            if msg.startswith("Value error, "):
                msg = msg[len("Value error, "):]

            details.append(ErrorDetail(field=field_name, issue=msg))

        error_response = ErrorResponse(
            success=False,
            error=ErrorContainer(
                code="VALIDATION_ERROR",
                message="Input validation failed",
                details=details,
            ),
        )
        return JSONResponse(
            status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
            content=error_response.model_dump(),
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """Handle domain application exceptions."""
        details = [ErrorDetail(**d) if isinstance(d, dict) else d for d in exc.details] if exc.details else None
        error_response = ErrorResponse(
            success=False,
            error=ErrorContainer(
                code=exc.code,
                message=exc.message,
                details=details,
            ),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all handler for unhandled exceptions to prevent stack trace leakage."""
        logger.exception("Unhandled server exception encountered on %s %s", request.method, request.url.path)
        error_response = ErrorResponse(
            success=False,
            error=ErrorContainer(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected internal server error occurred.",
                details=[ErrorDetail(field=None, issue="Please contact system support if this persists.")],
            ),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )
