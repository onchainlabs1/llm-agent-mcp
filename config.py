"""
AgentMCP Configuration Module

Centralized configuration management for the AgentMCP project.
Uses environment variables with fallback defaults.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables only.")


class LLMConfig:
    """LLM provider configuration."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "groq")
        self.model = os.getenv("LLM_MODEL", "llama3-70b-8192")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("TIMEOUT", "30"))


class LoggingConfig:
    """Logging configuration."""

    def __init__(self):
        self.level = os.getenv("LOG_LEVEL", "INFO")
        self.file = os.getenv("LOG_FILE", "logs/actions.log")


class MCPConfig:
    """MCP server configuration."""

    def __init__(self):
        self.server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self.schemas_path = os.getenv("MCP_SCHEMAS_PATH", "mcp_server/")


class DatabaseConfig:
    """Database configuration."""

    def __init__(self):
        self.crm_data_file = os.getenv("CRM_DATA_FILE", "data/clients.json")
        self.erp_data_file = os.getenv("ERP_DATA_FILE", "data/orders.json")
        self.hr_data_file = os.getenv("HR_DATA_FILE", "data/employees.json")


class AppConfig:
    """Application configuration."""

    def __init__(self):
        self.streamlit_host = os.getenv("STREAMLIT_HOST", "localhost")
        self.streamlit_port = int(os.getenv("STREAMLIT_PORT", "8501"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.development = os.getenv("DEVELOPMENT", "true").lower() == "true"


class SecurityConfig:
    """Security configuration."""

    def __init__(self):
        self.max_requests_per_minute = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
        self.max_requests_per_hour = int(os.getenv("MAX_REQUESTS_PER_HOUR", "1000"))
        self.session_timeout = int(os.getenv("SESSION_TIMEOUT", "3600"))


class Config:
    """Main configuration class."""

    def __init__(self):
        self.llm = LLMConfig()
        self.logging = LoggingConfig()
        self.mcp = MCPConfig()
        self.database = DatabaseConfig()
        self.app = AppConfig()
        self.security = SecurityConfig()

        # Create necessary directories
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories."""
        directories = [
            Path(self.logging.file).parent,
            Path(self.database.crm_data_file).parent,
            Path(self.mcp.schemas_path),
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True, parents=True)

    def get_llm_api_key(self) -> Optional[str]:
        """Get the appropriate API key based on provider."""
        if self.llm.provider == "groq":
            return self.llm.groq_api_key
        elif self.llm.provider == "openai":
            return self.llm.openai_api_key
        elif self.llm.provider == "anthropic":
            return self.llm.anthropic_api_key
        return None

    def validate_config(self) -> list:
        """Validate configuration and return list of errors."""
        errors = []

        # Validate API keys
        api_key = self.get_llm_api_key()
        if not api_key or api_key == "your-api-key-here":
            if self.llm.provider != "simulated":
                errors.append(f"Missing or invalid API key for {self.llm.provider}")

        # Validate file paths
        if not Path(self.mcp.schemas_path).exists():
            errors.append(f"MCP schemas directory not found: {self.mcp.schemas_path}")

        return errors

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.development and not self.debug

    def get_log_level(self):
        """Get logging level as logging module constant."""
        import logging

        return getattr(logging, self.logging.level.upper(), logging.INFO)


# Global configuration instance
config = Config()
