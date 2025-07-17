"""
AgentMCP REST API Main Application

Professional FastAPI application providing REST endpoints for AgentMCP.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
import time
import logging

from .middleware.cors import setup_cors
from .middleware.auth import AuthMiddleware
from .middleware.logging import LoggingMiddleware
from .routers import health, agent
from .dependencies import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 AgentMCP API starting up...")
    logger.info("📋 Loading MCP schemas...")
    logger.info("🔧 Initializing services...")
    logger.info("✅ AgentMCP API ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 AgentMCP API shutting down...")
    logger.info("💾 Saving any pending data...")
    logger.info("✅ AgentMCP API shutdown complete!")


# Create FastAPI application
app = FastAPI(
    title="AgentMCP REST API",
    description="""
    🤖 **AgentMCP REST API** - Enterprise-grade business automation platform
    
    ## Features
    
    * **🏢 CRM Operations**: Client management, balance updates, filtering
    * **📦 ERP Operations**: Order processing, inventory tracking, status updates  
    * **🤖 AI Agent**: Natural language business command processing
    * **🔐 Security**: Authentication, rate limiting, input validation
    * **📊 Monitoring**: Request logging, performance metrics, health checks
    * **📚 Documentation**: Interactive OpenAPI/Swagger documentation
    
    ## Authentication
    
    Most endpoints require authentication via API key:
    ```
    Authorization: Bearer your-api-key-here
    ```
    
    Available demo keys:
    - `demo-key-123` (Free tier: 100 req/hour)
    - `premium-key-456` (Premium tier: 1000 req/hour)  
    - `dev-key-789` (Development: 10000 req/hour)
    
    ## Rate Limiting
    
    - **Free tier**: 100 requests/hour
    - **Premium tier**: 1000 requests/hour
    - **Development**: 10000 requests/hour
    
    ## Support
    
    - 📧 Email: support@agentmcp.com  
    - 📚 Documentation: https://docs.agentmcp.com
    - 🐛 Issues: https://github.com/onchainlabs1/llm-agent-mcp/issues
    """,
    version="1.0.0",
    contact={
        "name": "AgentMCP Team",
        "email": "figueiredo.fabio@gmail.com",
        "url": "https://github.com/onchainlabs1/llm-agent-mcp",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and system status endpoints",
        },
        {
            "name": "agent", 
            "description": "AI Agent operations - natural language business commands",
        },
        {
            "name": "crm",
            "description": "Customer Relationship Management operations",
        },
        {
            "name": "erp",
            "description": "Enterprise Resource Planning operations",
        },
    ],
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)
setup_cors(app)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "HTTPException",
                "timestamp": time.time(),
                "path": str(request.url.path),
            }
        },
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "type": "InternalServerError", 
                "timestamp": time.time(),
                "path": str(request.url.path),
            }
        },
    )

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(agent.router, prefix="/api/v1", tags=["agent"])

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """API root endpoint with basic information."""
    return {
        "name": "AgentMCP REST API",
        "version": "1.0.0",
        "description": "Enterprise-grade business automation platform",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": "/api/v1/health",
        "repository": "https://github.com/onchainlabs1/llm-agent-mcp",
        "features": [
            "Natural language processing",
            "CRM automation",
            "ERP integration", 
            "Real-time monitoring",
            "Enterprise security"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
