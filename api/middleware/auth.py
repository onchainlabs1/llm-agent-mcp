"""
Authentication middleware for the AgentMCP API.
"""

import time
from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for API endpoints."""
    
    # Public endpoints that don't require authentication
    PUBLIC_ENDPOINTS = {
        "/",
        "/docs",
        "/redoc", 
        "/openapi.json",
        "/api/v1/health",
        "/api/v1/health/status",
    }
    
    # Demo API keys (in production, use proper key management)
    VALID_API_KEYS = {
        "demo-key-123": {"tier": "free", "requests_per_hour": 100},
        "premium-key-456": {"tier": "premium", "requests_per_hour": 1000},
        "dev-key-789": {"tier": "development", "requests_per_hour": 10000},
    }
    
    def __init__(self, app):
        super().__init__(app)
        self.request_counts = {}  # Simple in-memory rate limiting
    
    async def dispatch(self, request: Request, call_next):
        """Process request authentication."""
        
        # Skip authentication for public endpoints
        if request.url.path in self.PUBLIC_ENDPOINTS:
            return await call_next(request)
        
        # Extract API key from Authorization header
        api_key = self._extract_api_key(request)
        
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "code": 401,
                        "message": "Missing API key. Include 'Authorization: Bearer your-api-key' header.",
                        "type": "AuthenticationError",
                        "timestamp": time.time(),
                    }
                }
            )
        
        # Validate API key
        key_info = self.VALID_API_KEYS.get(api_key)
        if not key_info:
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "code": 401,
                        "message": "Invalid API key",
                        "type": "AuthenticationError", 
                        "timestamp": time.time(),
                    }
                }
            )
        
        # Rate limiting
        if not self._check_rate_limit(api_key, key_info):
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": 429,
                        "message": f"Rate limit exceeded. Max {key_info['requests_per_hour']} requests per hour for {key_info['tier']} tier.",
                        "type": "RateLimitError",
                        "timestamp": time.time(),
                    }
                }
            )
        
        # Add user info to request state
        request.state.api_key = api_key
        request.state.user_tier = key_info["tier"]
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-Rate-Limit-Limit"] = str(key_info["requests_per_hour"])
        response.headers["X-Rate-Limit-Remaining"] = str(
            key_info["requests_per_hour"] - self.request_counts.get(api_key, 0)
        )
        
        return response
    
    def _extract_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from Authorization header."""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        try:
            scheme, token = auth_header.split(" ", 1)
            if scheme.lower() == "bearer":
                return token
        except ValueError:
            pass
        
        return None
    
    def _check_rate_limit(self, api_key: str, key_info: dict) -> bool:
        """Simple rate limiting check."""
        current_hour = int(time.time() // 3600)
        key_with_hour = f"{api_key}:{current_hour}"
        
        if key_with_hour not in self.request_counts:
            self.request_counts[key_with_hour] = 0
        
        if self.request_counts[key_with_hour] >= key_info["requests_per_hour"]:
            return False
        
        self.request_counts[key_with_hour] += 1
        return True
