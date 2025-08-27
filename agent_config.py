"""
Agent Mode Configuration for Streamlit Cloud

Simplified configuration for agent functionality in Streamlit Cloud environment.
"""

import os
from typing import Optional

class AgentConfig:
    """Simplified agent configuration for Streamlit Cloud."""
    
    def __init__(self):
        # LLM Configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "simulated")
        self.llm_model = os.getenv("LLM_MODEL", "llama3-70b-8192")
        
        # API Keys (optional for Streamlit Cloud)
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        # MCP Configuration
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self.mcp_schemas_path = os.getenv("MCP_SCHEMAS_PATH", "mcp_server/")
        
        # Data Configuration
        self.data_path = os.getenv("DATA_PATH", "data/")
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/agent_actions.log")
        
        # Security Configuration
        self.max_requests_per_minute = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
        self.session_timeout = int(os.getenv("SESSION_TIMOUT", "3600"))
    
    def get_llm_api_key(self) -> Optional[str]:
        """Get the appropriate API key based on provider."""
        if self.llm_provider == "groq":
            return self.groq_api_key
        elif self.llm_provider == "openai":
            return self.openai_api_key
        elif self.llm_provider == "anthropic":
            return self.anthropic_api_key
        return None
    
    def is_simulated_mode(self) -> bool:
        """Check if running in simulated mode."""
        return (
            self.llm_provider == "simulated" or
            not any([self.groq_api_key, self.openai_api_key, self.anthropic_api_key])
        )

# Global configuration instance
agent_config = AgentConfig()
