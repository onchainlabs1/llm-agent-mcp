"""
Common dependencies for the FastAPI application.
"""

import functools
from typing import Generator

from config import Config


@functools.lru_cache()
def get_config() -> Config:
    """Get application configuration (cached)."""
    return Config()


def get_agent_core():
    """Get AgentCore instance."""
    try:
        from agent.agent_core import AgentCore, AgentConfig
        
        config = get_config()
        agent_config = AgentConfig(
            llm_provider=config.llm.provider,
            llm_model=config.llm.model,
            api_key=config.get_llm_api_key(),
        )
        return AgentCore(agent_config)
    except ImportError:
        from agent.agent_core import AgentCore, AgentConfig
        config = get_config()
        agent_config = AgentConfig(
            llm_provider=config.llm.provider,
            llm_model=config.llm.model,
            api_key=config.get_llm_api_key(),
        )
        return AgentCore(agent_config)


def get_crm_service():
    """Get CRM service instance."""
    try:
        from services.crm_service import CRMService
        return CRMService()
    except ImportError:
        from services.crm_service import CRMService
        return CRMService()


def get_erp_service():
    """Get ERP service instance."""
    try:
        from services.erp_service import ERPService
        return ERPService()
    except ImportError:
        from services.erp_service import ERPService
        return ERPService()
