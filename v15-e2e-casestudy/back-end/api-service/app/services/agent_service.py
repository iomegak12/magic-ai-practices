"""
Agent Service - Initialize and manage the MAF Agent.
"""
from agent_framework import MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity.aio import AzureCliCredential
from typing import Optional
import os

from ..tools.order_tools import initialize_order_manager, get_all_order_tools
from ..config import settings


class AgentService:
    """
    Service for managing the MAF Customer Service Agent.
    Handles initialization, session creation, and agent execution.
    """
    
    def __init__(self):
        """Initialize the agent service."""
        self.agent = None
        self.client = None
        self._initialize()
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt from template file."""
        prompt_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'prompts', 
            'agent_system_prompt.txt'
        )
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        
        return system_prompt
    
    def _initialize(self):
        """Initialize the MAF agent with tools and configuration."""
        print(f"🚀 Initializing Customer Service Agent...")
        
        # Load system prompt from template
        system_prompt = self._load_system_prompt()
        print(f"✅ Loaded system prompt template")
        
        # Initialize order management tools
        initialize_order_manager(settings.ORDER_DB_PATH)
        order_tools = get_all_order_tools()
        print(f"✅ Initialized {len(order_tools)} order management tools")
        
        # Initialize MCP tool for complaint management
        complaint_mcp_tool = MCPStreamableHTTPTool(
            name="Complaint Management System",
            url=settings.MCP_COMPLAINT_SERVER_URL
        )
        print(f"✅ Configured MCP tool: {settings.MCP_COMPLAINT_SERVER_URL}")
        
        # Create Azure OpenAI client
        credential = AzureCliCredential()
        self.client = AzureOpenAIResponsesClient(
            project_endpoint=settings.AZURE_AI_PROJECT_ENDPOINT,
            deployment_name=settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME,
            credential=credential,
        )
        print(f"✅ Connected to Azure OpenAI: {settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME}")
        
        # Create the agent
        self.agent = self.client.as_agent(
            name="Customer Service Representative",
            instructions=system_prompt,
            tools=order_tools + [complaint_mcp_tool]
        )
        print(f"✅ Customer Service Agent created successfully")
        print(f"   Total tools: {len(order_tools)} custom + 1 MCP tool")
    
    async def run(self, message: str, session):
        """
        Run the agent with a user message.
        
        Args:
            message: User's message
            session: Agent session for conversation context
            
        Returns:
            Agent's response as a string
        """
        return await self.agent.run(message, session=session)
    
    def create_session(self):
        """Create a new agent session for conversation."""
        return self.agent.create_session()


# Singleton instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """Get the singleton AgentService instance."""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
