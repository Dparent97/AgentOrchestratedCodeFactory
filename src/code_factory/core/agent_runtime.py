"""
Agent Runtime System

Provides the base agent interface and runtime execution framework
for all specialized agents in the factory.
"""

import logging
import threading
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel

from code_factory.core.models import AgentRun, AgentTimeoutError

logger = logging.getLogger(__name__)

# Default timeout for agent execution (5 minutes)
DEFAULT_TIMEOUT_SECONDS = 300


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
        Execute an agent with error handling, timeout, and logging

        Args:
            agent_name: Name of agent to execute
            input_data: Input for the agent
            timeout_seconds: Optional execution timeout (defaults to 300 seconds)

        Returns:
            AgentRun: Execution record with results or error

        Raises:
            AgentTimeoutError: If execution exceeds timeout (captured in run.error)
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

        # Set default timeout if not provided
        if timeout_seconds is None:
            timeout_seconds = DEFAULT_TIMEOUT_SECONDS

        run = AgentRun(
            agent_name=agent_name,
            input_data=input_data.model_dump(),
            status="running"
        )

        # Use threading to implement timeout
        result_container = {"output": None, "error": None, "timed_out": False}

        def execute_with_wrapper():
            """Wrapper function to execute agent and capture result"""
            try:
                logger.info(f"Executing agent: {agent_name} (timeout: {timeout_seconds}s)")
                output = agent.execute(input_data)
                result_container["output"] = output
            except Exception as e:
                result_container["error"] = e

        # Start execution in a separate thread
        execution_thread = threading.Thread(target=execute_with_wrapper, daemon=True)
        execution_thread.start()

        # Wait for completion or timeout
        execution_thread.join(timeout=timeout_seconds)

        # Check if thread is still alive (timed out)
        if execution_thread.is_alive():
            result_container["timed_out"] = True
            timeout_error = AgentTimeoutError(agent_name, timeout_seconds)

            # Log timeout with agent state for debugging
            logger.error(
                f"Agent {agent_name} timed out after {timeout_seconds}s. "
                f"Input: {input_data.model_dump()}, "
                f"Thread still running: {execution_thread.is_alive()}"
            )

            run.status = "failed"
            run.error = f"TIMEOUT: {str(timeout_error)}"
            run.completed_at = datetime.now()
            run.duration_seconds = timeout_seconds

            # Note: Thread will be terminated when daemon thread exits
            # Partial progress cannot be easily saved in thread-based approach
            logger.warning(f"Agent {agent_name} execution thread abandoned due to timeout")

        elif result_container["error"]:
            # Execution completed with error
            error = result_container["error"]
            run.status = "failed"
            run.error = str(error)
            run.completed_at = datetime.now()
            run.duration_seconds = (run.completed_at - run.started_at).total_seconds()

            logger.error(f"Agent {agent_name} failed: {error}")

        else:
            # Execution completed successfully
            output = result_container["output"]
            run.output_data = output.model_dump()
            run.status = "success"
            run.completed_at = datetime.now()
            run.duration_seconds = (run.completed_at - run.started_at).total_seconds()

            logger.info(
                f"Agent {agent_name} completed successfully "
                f"in {run.duration_seconds:.2f}s"
            )

        self._execution_history.append(run)
        return run
    
    def get_execution_history(self) -> list[AgentRun]:
        """
        Get history of all agent executions
        
        Returns:
            List of AgentRun records
        """
        return self._execution_history.copy()
