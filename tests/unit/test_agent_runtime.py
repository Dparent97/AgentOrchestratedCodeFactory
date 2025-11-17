"""
Tests for AgentRuntime including timeout functionality
"""

import time
import pytest

from code_factory.core.agent_runtime import AgentRuntime, BaseAgent, AgentExecutionError
from code_factory.core.models import Idea, SafetyCheck, AgentTimeoutError
from pydantic import BaseModel


class SimpleInput(BaseModel):
    """Simple input model for testing"""
    value: str


class SimpleOutput(BaseModel):
    """Simple output model for testing"""
    result: str


class FastAgent(BaseAgent):
    """Agent that completes quickly for testing"""

    @property
    def name(self) -> str:
        return "fast_agent"

    @property
    def description(self) -> str:
        return "Fast test agent"

    def execute(self, input_data: BaseModel) -> BaseModel:
        validated = self.validate_input(input_data, SimpleInput)
        return SimpleOutput(result=f"Processed: {validated.value}")


class SlowAgent(BaseAgent):
    """Agent that takes time to complete"""

    def __init__(self, delay_seconds: float = 2.0):
        self.delay_seconds = delay_seconds

    @property
    def name(self) -> str:
        return "slow_agent"

    @property
    def description(self) -> str:
        return "Slow test agent"

    def execute(self, input_data: BaseModel) -> BaseModel:
        validated = self.validate_input(input_data, SimpleInput)
        time.sleep(self.delay_seconds)
        return SimpleOutput(result=f"Processed: {validated.value}")


class FailingAgent(BaseAgent):
    """Agent that always fails"""

    @property
    def name(self) -> str:
        return "failing_agent"

    @property
    def description(self) -> str:
        return "Failing test agent"

    def execute(self, input_data: BaseModel) -> BaseModel:
        raise ValueError("Intentional failure for testing")


class TestAgentRuntime:
    """Tests for AgentRuntime basic functionality"""

    def test_register_agent(self):
        """Test agent registration"""
        runtime = AgentRuntime()
        agent = FastAgent()

        runtime.register_agent(agent)

        assert "fast_agent" in runtime.list_agents()

    def test_register_duplicate_agent(self):
        """Test that registering duplicate agent raises error"""
        runtime = AgentRuntime()
        agent1 = FastAgent()
        agent2 = FastAgent()

        runtime.register_agent(agent1)

        with pytest.raises(ValueError, match="already registered"):
            runtime.register_agent(agent2)

    def test_get_agent(self):
        """Test retrieving registered agent"""
        runtime = AgentRuntime()
        agent = FastAgent()
        runtime.register_agent(agent)

        retrieved = runtime.get_agent("fast_agent")

        assert retrieved is agent

    def test_get_nonexistent_agent(self):
        """Test retrieving nonexistent agent returns None"""
        runtime = AgentRuntime()

        retrieved = runtime.get_agent("nonexistent")

        assert retrieved is None

    def test_list_agents(self):
        """Test listing all agents"""
        runtime = AgentRuntime()
        agent1 = FastAgent()
        agent2 = SlowAgent()

        runtime.register_agent(agent1)
        runtime.register_agent(agent2)

        agents = runtime.list_agents()

        assert len(agents) == 2
        assert "fast_agent" in agents
        assert "slow_agent" in agents


class TestAgentExecution:
    """Tests for agent execution"""

    def test_execute_successful_agent(self):
        """Test successful agent execution"""
        runtime = AgentRuntime()
        agent = FastAgent()
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        run = runtime.execute_agent("fast_agent", input_data, timeout_seconds=5)

        assert run.status == "success"
        assert run.output_data is not None
        assert run.output_data["result"] == "Processed: test"
        assert run.error is None
        assert run.duration_seconds is not None
        assert run.duration_seconds > 0

    def test_execute_failing_agent(self):
        """Test execution of agent that fails"""
        runtime = AgentRuntime()
        agent = FailingAgent()
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        run = runtime.execute_agent("failing_agent", input_data, timeout_seconds=5)

        assert run.status == "failed"
        assert run.output_data is None
        assert run.error is not None
        assert "Intentional failure" in run.error

    def test_execute_nonexistent_agent(self):
        """Test execution of nonexistent agent"""
        runtime = AgentRuntime()

        input_data = SimpleInput(value="test")
        run = runtime.execute_agent("nonexistent", input_data, timeout_seconds=5)

        assert run.status == "failed"
        assert "not found" in run.error

    def test_execution_history(self):
        """Test that execution history is tracked"""
        runtime = AgentRuntime()
        agent = FastAgent()
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        runtime.execute_agent("fast_agent", input_data, timeout_seconds=5)
        runtime.execute_agent("fast_agent", input_data, timeout_seconds=5)

        history = runtime.get_execution_history()

        assert len(history) == 2
        assert all(run.agent_name == "fast_agent" for run in history)


class TestAgentTimeout:
    """Tests for agent timeout functionality"""

    def test_fast_agent_within_timeout(self):
        """Test that fast agent completes within timeout"""
        runtime = AgentRuntime()
        agent = FastAgent()
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        run = runtime.execute_agent("fast_agent", input_data, timeout_seconds=5)

        assert run.status == "success"
        assert run.duration_seconds < 5

    def test_slow_agent_exceeds_timeout(self):
        """Test that slow agent times out"""
        runtime = AgentRuntime()
        agent = SlowAgent(delay_seconds=3.0)
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        start_time = time.time()
        run = runtime.execute_agent("slow_agent", input_data, timeout_seconds=1)
        elapsed = time.time() - start_time

        assert run.status == "timeout"
        assert run.error is not None
        assert "timeout" in run.error.lower()
        # Should fail quickly, not wait for full delay
        assert elapsed < 2.0

    def test_default_timeout_used(self):
        """Test that default timeout is used when not specified"""
        runtime = AgentRuntime()
        agent = FastAgent()
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        # Don't specify timeout - should use default from config
        run = runtime.execute_agent("fast_agent", input_data)

        assert run.status == "success"

    def test_zero_timeout_disables_timeout(self):
        """Test that zero timeout disables timeout checking"""
        runtime = AgentRuntime()
        agent = SlowAgent(delay_seconds=1.0)
        runtime.register_agent(agent)

        input_data = SimpleInput(value="test")
        run = runtime.execute_agent("slow_agent", input_data, timeout_seconds=0)

        # Should complete successfully even though it's slow
        assert run.status == "success"


class TestBaseAgent:
    """Tests for BaseAgent functionality"""

    def test_validate_input_with_correct_type(self):
        """Test input validation with correct type"""
        agent = FastAgent()
        input_data = SimpleInput(value="test")

        validated = agent.validate_input(input_data, SimpleInput)

        assert isinstance(validated, SimpleInput)
        assert validated.value == "test"

    def test_validate_input_with_dict(self):
        """Test input validation with dict"""
        agent = FastAgent()
        input_data = {"value": "test"}

        validated = agent.validate_input(input_data, SimpleInput)

        assert isinstance(validated, SimpleInput)
        assert validated.value == "test"

    def test_validate_input_with_wrong_type(self):
        """Test input validation with wrong type"""
        agent = FastAgent()
        input_data = "wrong type"

        with pytest.raises(ValueError, match="Input must be"):
            agent.validate_input(input_data, SimpleInput)

    def test_validate_input_with_invalid_dict(self):
        """Test input validation with invalid dict"""
        agent = FastAgent()
        input_data = {"wrong_key": "test"}

        with pytest.raises(Exception):  # Pydantic validation error
            agent.validate_input(input_data, SimpleInput)
