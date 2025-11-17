"""
Unit tests for AgentRuntime and BaseAgent

Tests cover:
- Agent registration and retrieval
- Agent execution with success and failure cases
- Error handling and error propagation
- Execution history tracking
- Duration calculations
- Input validation
- Edge cases and error conditions
"""

import time
from datetime import datetime
from typing import Any

import pytest
from pydantic import BaseModel, Field

from code_factory.core.agent_runtime import (
    AgentExecutionError,
    AgentRuntime,
    BaseAgent,
)
from code_factory.core.models import Idea, SafetyCheck


# Test fixtures - Mock agents for testing


class MockInput(BaseModel):
    """Mock input model for testing"""
    value: str = Field(..., description="Test value")


class MockOutput(BaseModel):
    """Mock output model for testing"""
    result: str = Field(..., description="Test result")
    processed: bool = Field(default=True)


class SuccessAgent(BaseAgent):
    """Mock agent that always succeeds"""

    @property
    def name(self) -> str:
        return "success_agent"

    @property
    def description(self) -> str:
        return "Agent that always succeeds"

    def execute(self, input_data: MockInput) -> MockOutput:
        validated = self.validate_input(input_data, MockInput)
        return MockOutput(result=f"Processed: {validated.value}")


class FailureAgent(BaseAgent):
    """Mock agent that always fails"""

    @property
    def name(self) -> str:
        return "failure_agent"

    @property
    def description(self) -> str:
        return "Agent that always fails"

    def execute(self, input_data: MockInput) -> MockOutput:
        validated = self.validate_input(input_data, MockInput)
        raise AgentExecutionError(f"Intentional failure for: {validated.value}")


class SlowAgent(BaseAgent):
    """Mock agent that takes time to execute"""

    def __init__(self, delay_seconds: float = 0.1):
        self.delay_seconds = delay_seconds

    @property
    def name(self) -> str:
        return "slow_agent"

    @property
    def description(self) -> str:
        return "Agent that executes slowly"

    def execute(self, input_data: MockInput) -> MockOutput:
        validated = self.validate_input(input_data, MockInput)
        time.sleep(self.delay_seconds)
        return MockOutput(result=f"Slowly processed: {validated.value}")


class InvalidInputAgent(BaseAgent):
    """Mock agent that expects specific input type"""

    @property
    def name(self) -> str:
        return "invalid_input_agent"

    @property
    def description(self) -> str:
        return "Agent with strict input validation"

    def execute(self, input_data: Idea) -> SafetyCheck:
        validated = self.validate_input(input_data, Idea)
        return SafetyCheck(
            approved=True,
            warnings=[],
            required_confirmations=[],
            blocked_keywords=[]
        )


# Tests


class TestBaseAgentInterface:
    """Test BaseAgent abstract interface and methods"""

    def test_base_agent_cannot_be_instantiated(self):
        """Test that BaseAgent cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseAgent()

    def test_agent_has_required_properties(self):
        """Test that agents must implement required properties"""
        agent = SuccessAgent()
        assert hasattr(agent, "name")
        assert hasattr(agent, "description")
        assert callable(agent.execute)

    def test_validate_input_with_correct_type(self):
        """Test validate_input accepts correct type"""
        agent = SuccessAgent()
        input_data = MockInput(value="test")
        result = agent.validate_input(input_data, MockInput)
        assert isinstance(result, MockInput)
        assert result.value == "test"

    def test_validate_input_with_dict(self):
        """Test validate_input converts dict to model"""
        agent = SuccessAgent()
        input_dict = {"value": "test"}
        result = agent.validate_input(input_dict, MockInput)
        assert isinstance(result, MockInput)
        assert result.value == "test"

    def test_validate_input_with_invalid_type(self):
        """Test validate_input rejects invalid types"""
        agent = SuccessAgent()
        with pytest.raises(ValueError, match="Input must be"):
            agent.validate_input("invalid", MockInput)

    def test_validate_input_with_none(self):
        """Test validate_input rejects None"""
        agent = SuccessAgent()
        with pytest.raises(ValueError):
            agent.validate_input(None, MockInput)


class TestAgentRuntimeRegistration:
    """Test agent registration functionality"""

    def test_runtime_initialization(self):
        """Test AgentRuntime initializes correctly"""
        runtime = AgentRuntime()
        assert runtime is not None
        assert runtime.list_agents() == {}
        assert runtime.get_execution_history() == []

    def test_register_single_agent(self):
        """Test registering a single agent"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        assert "success_agent" in runtime.list_agents()
        assert runtime.get_agent("success_agent") is agent

    def test_register_multiple_agents(self):
        """Test registering multiple agents"""
        runtime = AgentRuntime()
        agent1 = SuccessAgent()
        agent2 = FailureAgent()
        agent3 = SlowAgent()

        runtime.register_agent(agent1)
        runtime.register_agent(agent2)
        runtime.register_agent(agent3)

        agents = runtime.list_agents()
        assert len(agents) == 3
        assert "success_agent" in agents
        assert "failure_agent" in agents
        assert "slow_agent" in agents

    def test_register_duplicate_agent_raises_error(self):
        """Test that registering duplicate agent name raises error"""
        runtime = AgentRuntime()
        agent1 = SuccessAgent()
        agent2 = SuccessAgent()

        runtime.register_agent(agent1)
        with pytest.raises(ValueError, match="already registered"):
            runtime.register_agent(agent2)

    def test_get_agent_returns_none_for_unknown(self):
        """Test that get_agent returns None for unknown agent"""
        runtime = AgentRuntime()
        assert runtime.get_agent("unknown_agent") is None

    def test_list_agents_returns_descriptions(self):
        """Test that list_agents returns name->description mapping"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        agents = runtime.list_agents()
        assert agents["success_agent"] == agent.description


class TestAgentExecution:
    """Test agent execution functionality"""

    def test_execute_successful_agent(self):
        """Test executing an agent that succeeds"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test_data")
        result = runtime.execute_agent("success_agent", input_data)

        assert result.status == "success"
        assert result.error is None
        assert result.output_data is not None
        assert result.output_data["result"] == "Processed: test_data"
        assert result.agent_name == "success_agent"

    def test_execute_failing_agent(self):
        """Test executing an agent that fails"""
        runtime = AgentRuntime()
        agent = FailureAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test_data")
        result = runtime.execute_agent("failure_agent", input_data)

        assert result.status == "failed"
        assert result.error is not None
        assert "Intentional failure" in result.error
        assert result.output_data is None

    def test_execute_nonexistent_agent(self):
        """Test executing an agent that doesn't exist"""
        runtime = AgentRuntime()
        input_data = MockInput(value="test")

        result = runtime.execute_agent("nonexistent", input_data)

        assert result.status == "failed"
        assert result.error is not None
        assert "not found" in result.error
        assert result.agent_name == "nonexistent"

    def test_execution_records_timing(self):
        """Test that execution records timing information"""
        runtime = AgentRuntime()
        agent = SlowAgent(delay_seconds=0.1)
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        result = runtime.execute_agent("slow_agent", input_data)

        assert result.started_at is not None
        assert result.completed_at is not None
        assert result.duration_seconds is not None
        assert result.duration_seconds >= 0.1  # Should take at least the delay time
        assert result.completed_at > result.started_at

    def test_execution_duration_on_failure(self):
        """Test that duration is recorded even on failure"""
        runtime = AgentRuntime()
        agent = FailureAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        result = runtime.execute_agent("failure_agent", input_data)

        assert result.duration_seconds is not None
        assert result.duration_seconds >= 0
        assert result.completed_at is not None

    def test_execution_preserves_input_data(self):
        """Test that input data is preserved in execution record"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="important_data")
        result = runtime.execute_agent("success_agent", input_data)

        assert result.input_data is not None
        assert result.input_data["value"] == "important_data"


class TestExecutionHistory:
    """Test execution history tracking"""

    def test_execution_history_is_recorded(self):
        """Test that executions are added to history"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        runtime.execute_agent("success_agent", input_data)

        history = runtime.get_execution_history()
        assert len(history) == 1
        assert history[0].agent_name == "success_agent"

    def test_multiple_executions_in_history(self):
        """Test that multiple executions are tracked"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        for i in range(5):
            input_data = MockInput(value=f"test_{i}")
            runtime.execute_agent("success_agent", input_data)

        history = runtime.get_execution_history()
        assert len(history) == 5

    def test_failed_executions_in_history(self):
        """Test that failed executions are also recorded"""
        runtime = AgentRuntime()
        success_agent = SuccessAgent()
        failure_agent = FailureAgent()
        runtime.register_agent(success_agent)
        runtime.register_agent(failure_agent)

        input_data = MockInput(value="test")
        runtime.execute_agent("success_agent", input_data)
        runtime.execute_agent("failure_agent", input_data)

        history = runtime.get_execution_history()
        assert len(history) == 2
        assert history[0].status == "success"
        assert history[1].status == "failed"

    def test_execution_history_is_copy(self):
        """Test that get_execution_history returns a copy"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        runtime.execute_agent("success_agent", input_data)

        history1 = runtime.get_execution_history()
        history2 = runtime.get_execution_history()

        assert history1 is not history2  # Different list objects
        assert len(history1) == len(history2)

    def test_history_preserves_execution_order(self):
        """Test that history maintains execution order"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        for i in range(3):
            input_data = MockInput(value=f"test_{i}")
            runtime.execute_agent("success_agent", input_data)

        history = runtime.get_execution_history()
        assert history[0].input_data["value"] == "test_0"
        assert history[1].input_data["value"] == "test_1"
        assert history[2].input_data["value"] == "test_2"


class TestErrorHandling:
    """Test error handling in agent execution"""

    def test_agent_execution_error_is_caught(self):
        """Test that AgentExecutionError is caught and recorded"""
        runtime = AgentRuntime()
        agent = FailureAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        result = runtime.execute_agent("failure_agent", input_data)

        assert result.status == "failed"
        assert result.error is not None

    def test_generic_exception_is_caught(self):
        """Test that generic exceptions are caught"""

        class ExceptionAgent(BaseAgent):
            @property
            def name(self) -> str:
                return "exception_agent"

            @property
            def description(self) -> str:
                return "Throws generic exception"

            def execute(self, input_data: MockInput) -> MockOutput:
                raise RuntimeError("Unexpected error occurred")

        runtime = AgentRuntime()
        agent = ExceptionAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        result = runtime.execute_agent("exception_agent", input_data)

        assert result.status == "failed"
        assert "Unexpected error occurred" in result.error

    def test_execution_continues_after_failure(self):
        """Test that runtime can execute agents after a failure"""
        runtime = AgentRuntime()
        success_agent = SuccessAgent()
        failure_agent = FailureAgent()
        runtime.register_agent(success_agent)
        runtime.register_agent(failure_agent)

        input_data = MockInput(value="test")

        # First execution fails
        result1 = runtime.execute_agent("failure_agent", input_data)
        assert result1.status == "failed"

        # Subsequent execution should succeed
        result2 = runtime.execute_agent("success_agent", input_data)
        assert result2.status == "success"


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_multiple_agents_workflow(self):
        """Test executing multiple agents in sequence"""
        runtime = AgentRuntime()

        # Register multiple agents
        runtime.register_agent(SuccessAgent())
        runtime.register_agent(SlowAgent())

        # Execute workflow
        input_data = MockInput(value="workflow_test")
        result1 = runtime.execute_agent("success_agent", input_data)
        result2 = runtime.execute_agent("slow_agent", input_data)

        # Verify both succeeded
        assert result1.status == "success"
        assert result2.status == "success"

        # Verify history
        history = runtime.get_execution_history()
        assert len(history) == 2

    def test_agent_state_isolation(self):
        """Test that agents don't share state between executions"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        # Execute same agent multiple times
        input1 = MockInput(value="first")
        input2 = MockInput(value="second")

        result1 = runtime.execute_agent("success_agent", input1)
        result2 = runtime.execute_agent("success_agent", input2)

        # Results should be different
        assert result1.output_data["result"] == "Processed: first"
        assert result2.output_data["result"] == "Processed: second"

    def test_runtime_with_real_agents(self):
        """Test runtime with actual factory agents"""
        from code_factory.agents.safety_guard import SafetyGuard

        runtime = AgentRuntime()
        safety_guard = SafetyGuard()
        runtime.register_agent(safety_guard)

        idea = Idea(description="Build a maintenance tracking tool")
        result = runtime.execute_agent("safety_guard", idea)

        assert result.status == "success"
        assert result.output_data is not None
        assert "approved" in result.output_data


class TestTimeoutHandling:
    """Test timeout-related functionality"""

    def test_timeout_parameter_accepted(self):
        """Test that timeout parameter is accepted (even if not enforced yet)"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        result = runtime.execute_agent("success_agent", input_data, timeout_seconds=10)

        # Should execute successfully (timeout not enforced yet)
        assert result.status == "success"

    def test_none_timeout_works(self):
        """Test that None timeout works"""
        runtime = AgentRuntime()
        agent = SuccessAgent()
        runtime.register_agent(agent)

        input_data = MockInput(value="test")
        result = runtime.execute_agent("success_agent", input_data, timeout_seconds=None)

        assert result.status == "success"
