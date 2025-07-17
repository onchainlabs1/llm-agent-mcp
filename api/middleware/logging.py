"""
Request logging middleware for the AgentMCP API.
"""

import time
import logging
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all API requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Log request and response details."""
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        logger.info(
            f"🔵 REQUEST {request_id} | {request.method} {request.url.path} | "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        status_emoji = "🟢" if response.status_code < 400 else "🔴"
        logger.info(
            f"{status_emoji} RESPONSE {request_id} | {response.status_code} | "
            f"{duration:.3f}s"
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
