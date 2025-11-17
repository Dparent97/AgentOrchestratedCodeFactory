"""
Unit tests for AgentRuntime timeout functionality

Tests the timeout implementation, error handling, and edge cases
for agent execution with timeouts.
"""

import pytest
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from code_factory.core.agent_runtime import AgentRuntime, BaseAgent, DEFAULT_TIMEOUT_SECONDS
from code_factory.core.models import AgentRun, AgentTimeoutError
from pydantic import BaseModel, Field


# Test models
class AgentInput(BaseModel):
    """Simple input model for testing"""
    value: str = Field(..., description="Test value")


class AgentOutput(BaseModel):
    """Simple output model for testing"""
    result: str = Field(..., description="Test result")


# Test agents
class FastAgent(BaseAgent):
    """Agent that completes quickly"""

    @property
    def name(self) -> str:
        return "fast_agent"

    @property
    def description(self) -> str:
        return "Completes execution quickly"

    def execute(self, input_data: AgentInput) -> AgentOutput:
        """Execute quickly"""
        return AgentOutput(result=f"Processed: {input_data.value}")


class SlowAgent(BaseAgent):
    """Agent that takes a long time to complete"""

    def __init__(self, delay_seconds: int = 5):
        self.delay_seconds = delay_seconds

    @property
    def name(self) -> str:
        return "slow_agent"

    @property
    def description(self) -> str:
        return "Takes time to complete execution"

    def execute(self, input_data: AgentInput) -> AgentOutput:
        """Execute slowly"""
        time.sleep(self.delay_seconds)
        return AgentOutput(result=f"Slowly processed: {input_data.value}")


class FailingAgent(BaseAgent):
    """Agent that always fails"""

    @property
    def name(self) -> str:
        return "failing_agent"

    @property
    def description(self) -> str:
        return "Always fails during execution"

    def execute(self, input_data: AgentInput) -> AgentOutput:
        """Always raises an error"""
        raise ValueError("Simulated failure")


class InfiniteLoopAgent(BaseAgent):
    """Agent that enters an infinite loop"""

    @property
    def name(self) -> str:
        return "infinite_loop_agent"

    @property
    def description(self) -> str:
        return "Enters an infinite loop"

    def execute(self, input_data: AgentInput) -> AgentOutput:
        """Never completes"""
        while True:
            pass  # Infinite loop


# Test fixtures
@pytest.fixture
def runtime():
    """Create a fresh runtime for each test"""
    return AgentRuntime()


@pytest.fixture
def fast_agent():
    """Create a fast agent"""
    return FastAgent()


@pytest.fixture
def slow_agent():
    """Create a slow agent (5 second delay)"""
    return SlowAgent(delay_seconds=5)


@pytest.fixture
def failing_agent():
    """Create a failing agent"""
    return FailingAgent()


@pytest.fixture
def infinite_loop_agent():
    """Create an infinite loop agent"""
    return InfiniteLoopAgent()


# Tests
class TestAgentTimeoutError:
    """Tests for AgentTimeoutError exception"""

    def test_timeout_error_creation(self):
        """Test creating AgentTimeoutError"""
        error = AgentTimeoutError("test_agent", 300)
        assert error.agent_name == "test_agent"
        assert error.timeout_seconds == 300
        assert "test_agent" in str(error)
        assert "300" in str(error)

    def test_timeout_error_custom_message(self):
        """Test AgentTimeoutError with custom message"""
        error = AgentTimeoutError("test_agent", 300, "Custom timeout message")
        assert str(error) == "Custom timeout message"


class TestAgentRuntimeBasics:
    """Tests for basic AgentRuntime functionality"""

    def test_runtime_initialization(self, runtime):
        """Test runtime initializes correctly"""
        assert runtime is not None
        assert len(runtime.list_agents()) == 0
        assert len(runtime.get_execution_history()) == 0

    def test_agent_registration(self, runtime, fast_agent):
        """Test agent registration"""
        runtime.register_agent(fast_agent)
        assert "fast_agent" in runtime.list_agents()
        assert runtime.get_agent("fast_agent") == fast_agent

    def test_duplicate_registration_fails(self, runtime, fast_agent):
        """Test that registering same agent twice fails"""
        runtime.register_agent(fast_agent)
        with pytest.raises(ValueError, match="already registered"):
            runtime.register_agent(fast_agent)

    def test_get_nonexistent_agent(self, runtime):
        """Test getting an agent that doesn't exist"""
        assert runtime.get_agent("nonexistent") is None


class TestAgentExecutionWithoutTimeout:
    """Tests for agent execution without timeout concerns"""

    def test_successful_execution(self, runtime, fast_agent):
        """Test successful agent execution"""
        runtime.register_agent(fast_agent)
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("fast_agent", input_data)

        assert run.status == "success"
        assert run.output_data is not None
        assert run.output_data["result"] == "Processed: test"
        assert run.error is None
        assert run.duration_seconds is not None
        assert run.duration_seconds < 1  # Should be very fast

    def test_failed_execution(self, runtime, failing_agent):
        """Test agent execution that fails"""
        runtime.register_agent(failing_agent)
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("failing_agent", input_data)

        assert run.status == "failed"
        assert run.output_data is None
        assert run.error is not None
        assert "Simulated failure" in run.error

    def test_nonexistent_agent_execution(self, runtime):
        """Test executing an agent that doesn't exist"""
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("nonexistent", input_data)

        assert run.status == "failed"
        assert "not found" in run.error.lower()

    def test_execution_history_tracking(self, runtime, fast_agent):
        """Test that execution history is tracked"""
        runtime.register_agent(fast_agent)
        input_data = AgentInput(value="test")

        assert len(runtime.get_execution_history()) == 0

        runtime.execute_agent("fast_agent", input_data)
        assert len(runtime.get_execution_history()) == 1

        runtime.execute_agent("fast_agent", input_data)
        assert len(runtime.get_execution_history()) == 2


class TestTimeoutFunctionality:
    """Tests for timeout functionality"""

    def test_timeout_with_infinite_loop(self, runtime, infinite_loop_agent):
        """Test that infinite loop agent times out"""
        runtime.register_agent(infinite_loop_agent)
        input_data = AgentInput(value="test")

        # Use a very short timeout (2 seconds)
        start_time = time.time()
        run = runtime.execute_agent("infinite_loop_agent", input_data, timeout_seconds=2)
        elapsed_time = time.time() - start_time

        assert run.status == "failed"
        assert "TIMEOUT" in run.error
        assert "infinite_loop_agent" in run.error
        assert elapsed_time < 3  # Should timeout around 2 seconds
        assert run.duration_seconds == 2  # Recorded as timeout duration

    def test_timeout_with_slow_agent(self, runtime, slow_agent):
        """Test that slow agent times out with short timeout"""
        runtime.register_agent(slow_agent)
        input_data = AgentInput(value="test")

        # Agent takes 5 seconds, timeout at 2 seconds
        run = runtime.execute_agent("slow_agent", input_data, timeout_seconds=2)

        assert run.status == "failed"
        assert "TIMEOUT" in run.error
        assert run.duration_seconds == 2

    def test_no_timeout_with_sufficient_time(self, runtime, slow_agent):
        """Test that slow agent succeeds with sufficient timeout"""
        runtime.register_agent(slow_agent)
        input_data = AgentInput(value="test")

        # Agent takes 5 seconds, timeout at 10 seconds
        run = runtime.execute_agent("slow_agent", input_data, timeout_seconds=10)

        assert run.status == "success"
        assert run.output_data is not None
        assert "Slowly processed: test" in run.output_data["result"]
        assert run.duration_seconds >= 5  # Should take at least 5 seconds
        assert run.duration_seconds < 10  # But less than timeout

    def test_default_timeout_used(self, runtime, fast_agent):
        """Test that default timeout is used when not specified"""
        runtime.register_agent(fast_agent)
        input_data = AgentInput(value="test")

        # Don't specify timeout - should use default
        run = runtime.execute_agent("fast_agent", input_data)

        assert run.status == "success"
        # Verify it ran (default timeout didn't interfere)
        assert run.output_data is not None

    def test_custom_timeout_value(self, runtime):
        """Test that custom timeout values are respected"""
        # Create a slow agent with 3 second delay
        slow_agent = SlowAgent(delay_seconds=3)
        runtime.register_agent(slow_agent)
        input_data = AgentInput(value="test")

        # Test with timeout less than execution time (should timeout)
        run = runtime.execute_agent("slow_agent", input_data, timeout_seconds=1)
        assert run.status == "failed"
        assert "TIMEOUT" in run.error

        # Create a new runtime and faster agent for success test
        runtime2 = AgentRuntime()
        fast_slow_agent = SlowAgent(delay_seconds=1)
        runtime2.register_agent(fast_slow_agent)

        # Test with timeout more than execution time (should succeed)
        run = runtime2.execute_agent("slow_agent", input_data, timeout_seconds=5)
        assert run.status == "success"


class TestTimeoutLogging:
    """Tests for timeout logging and debugging information"""

    def test_timeout_includes_agent_name(self, runtime, infinite_loop_agent):
        """Test that timeout error includes agent name"""
        runtime.register_agent(infinite_loop_agent)
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("infinite_loop_agent", input_data, timeout_seconds=1)

        assert "infinite_loop_agent" in run.error

    def test_timeout_includes_duration(self, runtime, infinite_loop_agent):
        """Test that timeout error includes timeout duration"""
        runtime.register_agent(infinite_loop_agent)
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("infinite_loop_agent", input_data, timeout_seconds=2)

        assert "2" in run.error

    def test_successful_execution_logs_duration(self, runtime, fast_agent):
        """Test that successful execution logs duration"""
        runtime.register_agent(fast_agent)
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("fast_agent", input_data)

        assert run.duration_seconds is not None
        assert run.duration_seconds >= 0


class TestEdgeCases:
    """Tests for edge cases and unusual scenarios"""

    def test_very_short_timeout(self, runtime, infinite_loop_agent):
        """Test behavior with very short timeout"""
        runtime.register_agent(infinite_loop_agent)
        input_data = AgentInput(value="test")

        # Use a very short timeout (0.1 seconds)
        # Even with a very short timeout, the infinite loop should timeout
        run = runtime.execute_agent("infinite_loop_agent", input_data, timeout_seconds=0.1)

        # Should timeout very quickly
        assert run.status == "failed"
        assert "TIMEOUT" in run.error

    def test_very_large_timeout(self, runtime, fast_agent):
        """Test behavior with very large timeout"""
        runtime.register_agent(fast_agent)
        input_data = AgentInput(value="test")

        # Should complete normally even with huge timeout
        run = runtime.execute_agent("fast_agent", input_data, timeout_seconds=999999)

        assert run.status == "success"
        assert run.duration_seconds < 10  # Should still be fast

    def test_multiple_sequential_executions(self, runtime, fast_agent):
        """Test multiple sequential executions work correctly"""
        runtime.register_agent(fast_agent)
        input_data = AgentInput(value="test")

        for i in range(5):
            run = runtime.execute_agent("fast_agent", input_data, timeout_seconds=10)
            assert run.status == "success"

        # Check history
        history = runtime.get_execution_history()
        assert len(history) == 5
        assert all(r.status == "success" for r in history)


class TestRuntimeRecordKeeping:
    """Tests for runtime record keeping with timeouts"""

    def test_timeout_recorded_in_history(self, runtime, infinite_loop_agent):
        """Test that timeouts are recorded in execution history"""
        runtime.register_agent(infinite_loop_agent)
        input_data = AgentInput(value="test")

        run = runtime.execute_agent("infinite_loop_agent", input_data, timeout_seconds=1)

        history = runtime.get_execution_history()
        assert len(history) == 1
        assert history[0].status == "failed"
        assert "TIMEOUT" in history[0].error

    def test_mixed_success_and_timeout_history(self, runtime, fast_agent, infinite_loop_agent):
        """Test history with mix of successful and timeout executions"""
        runtime.register_agent(fast_agent)
        runtime.register_agent(infinite_loop_agent)
        input_data = AgentInput(value="test")

        # Success
        runtime.execute_agent("fast_agent", input_data)
        # Timeout
        runtime.execute_agent("infinite_loop_agent", input_data, timeout_seconds=1)
        # Success
        runtime.execute_agent("fast_agent", input_data)

        history = runtime.get_execution_history()
        assert len(history) == 3
        assert history[0].status == "success"
        assert history[1].status == "failed"
        assert "TIMEOUT" in history[1].error
        assert history[2].status == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
