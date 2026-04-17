"""
AI Agent Module

This module provides the agent management system including:
- Agent factory for creating configured agents
- Agent manager for lifecycle and execution
- System instructions and prompts
"""

from .factory import AgentFactory
from .manager import (
    AgentManager,
    initialize_agent_manager,
    get_agent_manager,
    shutdown_agent_manager
)
from .instructions import (
    AGENT_SYSTEM_PROMPT,
    get_full_system_prompt,
    get_scenario_prompt,
    get_error_handling_prompt
)

__all__ = [
    # Factory
    "AgentFactory",
    
    # Manager
    "AgentManager",
    "initialize_agent_manager",
    "get_agent_manager",
    "shutdown_agent_manager",
    
    # Instructions
    "AGENT_SYSTEM_PROMPT",
    "get_full_system_prompt",
    "get_scenario_prompt",
    "get_error_handling_prompt",
]
