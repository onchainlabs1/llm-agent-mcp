"""
CORS (Cross-Origin Resource Sharing) middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI app."""
    
    # Allow specific origins in production, all origins in development
    allowed_origins = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8501",  # Streamlit app
        "http://localhost:8502",  # Streamlit landing page
        "http://127.0.0.1:8501", 
        "http://127.0.0.1:8502",
        "https://agentmcp.com",   # Production domain
        "https://www.agentmcp.com",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Rate-Limit-Remaining"],
    )
