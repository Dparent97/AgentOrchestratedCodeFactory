"""
Agent Runtime System

Provides the base agent interface and runtime execution framework
for all specialized agents in the factory.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel

from code_factory.core.models import AgentRun

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all factory agents
    
    All specialized agents must inherit from this class and implement
    the required methods. This ensures consistent interface and behavior.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique identifier for this agent
        
        Returns:
            str: Agent name (e.g., "planner", "architect")
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable description of agent's purpose
        
        Returns:
            str: What this agent does
        """
        pass
    
    @abstractmethod
    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Execute the agent's primary logic
        
        Args:
            input_data: Validated input conforming to agent's expected schema
            
        Returns:
            BaseModel: Validated output conforming to agent's output schema
            
        Raises:
            AgentExecutionError: If execution fails
            ValueError: If input is invalid
        """
        pass
    
    def validate_input(self, input_data: Any, expected_type: Type[BaseModel]) -> BaseModel:
        """
        Validate input data against expected schema
        
        Args:
            input_data: Data to validate
            expected_type: Expected Pydantic model type
            
        Returns:
            BaseModel: Validated input
            
        Raises:
            ValueError: If validation fails
        """
        if isinstance(input_data, expected_type):
            return input_data
        elif isinstance(input_data, dict):
            return expected_type(**input_data)
        else:
            raise ValueError(f"Input must be {expected_type.__name__} or dict")


class AgentExecutionError(Exception):
    """Raised when agent execution fails"""
    pass



class AgentRuntime:
    """
    Runtime environment for executing agents
    
    Handles agent registration, execution with error handling,
    logging, and resource management.
    """
    
    def __init__(self):
        """Initialize the runtime"""
        self._agents: Dict[str, BaseAgent] = {}
        self._execution_history: list[AgentRun] = []
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the runtime
        
        Args:
            agent: Agent instance to register
            
        Raises:
            ValueError: If agent with same name already registered
        """
        if agent.name in self._agents:
            raise ValueError(f"Agent '{agent.name}' is already registered")
        
        self._agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """
        Retrieve a registered agent by name
        
        Args:
            name: Agent name
            
        Returns:
            BaseAgent instance or None if not found
        """
        return self._agents.get(name)
    
    def list_agents(self) -> Dict[str, str]:
        """
        List all registered agents
        
        Returns:
            Dict mapping agent names to descriptions
        """
        return {name: agent.description for name, agent in self._agents.items()}
    
    def execute_agent(
        self,
        agent_name: str,
        input_data: BaseModel,
        timeout_seconds: Optional[int] = None
    ) -> AgentRun:
        """
        Execute an agent with error handling and logging
        
        Args:
            agent_name: Name of agent to execute
            input_data: Input for the agent
            timeout_seconds: Optional execution timeout (not yet implemented)
            
        Returns:
            AgentRun: Execution record with results or error
        """
        agent = self.get_agent(agent_name)
        if not agent:
            error_msg = f"Agent '{agent_name}' not found"
            logger.error(error_msg)
            return AgentRun(
                agent_name=agent_name,
                input_data=input_data.model_dump(),
                status="failed",
                error=error_msg,
                completed_at=datetime.now()
            )
        
        run = AgentRun(
            agent_name=agent_name,
            input_data=input_data.model_dump(),
            status="running"
        )
        
        try:
            logger.info(f"Executing agent: {agent_name}")
            output = agent.execute(input_data)
            
            run.output_data = output.model_dump()
            run.status = "success"
            run.completed_at = datetime.now()
            run.duration_seconds = (run.completed_at - run.started_at).total_seconds()
            
            logger.info(f"Agent {agent_name} completed successfully")
            
        except Exception as e:
            run.status = "failed"
            run.error = str(e)
            run.completed_at = datetime.now()
            run.duration_seconds = (run.completed_at - run.started_at).total_seconds()
            
            logger.error(f"Agent {agent_name} failed: {e}")
        
        self._execution_history.append(run)
        return run
    
    def get_execution_history(self) -> list[AgentRun]:
        """
        Get history of all agent executions
        
        Returns:
            List of AgentRun records
        """
        return self._execution_history.copy()
