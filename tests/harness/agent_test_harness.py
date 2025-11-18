"""
Agent Test Harness - Reusable test framework for all agents

Provides standardized testing utilities that work with any agent
implementing the BaseAgent interface. This ensures consistent
testing across all agent implementations.

Usage:
    harness = AgentTestHarness()
    harness.test_agent_interface(my_agent)
    result = harness.test_agent_execution(my_agent, input_data, ExpectedOutputType)
    harness.test_agent_error_handling(my_agent, invalid_input)
"""

import logging
from typing import Any, Type

import pytest
from pydantic import BaseModel, ValidationError

from code_factory.core.agent_runtime import BaseAgent

logger = logging.getLogger(__name__)


class AgentTestHarness:
    """
    Reusable test framework for all agents

    Provides standard test methods that verify:
    - Agent interface compliance (BaseAgent)
    - Execution correctness
    - Error handling
    - Input/output validation
    """

    def test_agent_interface(self, agent: BaseAgent) -> None:
        """
        Verify agent implements BaseAgent interface correctly

        Checks for:
        - Required 'execute' method
        - Required 'name' property
        - Required 'description' property
        - Proper types for all properties

        Args:
            agent: Agent instance to test

        Raises:
            AssertionError: If agent doesn't meet interface requirements
        """
        # Check required methods exist
        assert hasattr(agent, "execute"), f"{agent.__class__.__name__} missing execute method"
        assert callable(agent.execute), f"{agent.__class__.__name__}.execute is not callable"

        # Check required properties exist
        assert hasattr(agent, "name"), f"{agent.__class__.__name__} missing name property"
        assert hasattr(
            agent, "description"
        ), f"{agent.__class__.__name__} missing description property"

        # Check types
        assert isinstance(agent.name, str), f"{agent.__class__.__name__}.name must be str"
        assert isinstance(
            agent.description, str
        ), f"{agent.__class__.__name__}.description must be str"

        # Check values are not empty
        assert len(agent.name) > 0, f"{agent.__class__.__name__}.name cannot be empty"
        assert (
            len(agent.description) > 0
        ), f"{agent.__class__.__name__}.description cannot be empty"

        logger.info(f"✅ {agent.name} implements BaseAgent interface correctly")

    def test_agent_execution(
        self,
        agent: BaseAgent,
        input_data: BaseModel,
        expected_output_type: Type[BaseModel],
    ) -> BaseModel:
        """
        Test agent executes correctly with valid input

        Args:
            agent: Agent instance to test
            input_data: Valid input for the agent
            expected_output_type: Expected type of output (e.g., TaskList, ProjectSpec)

        Returns:
            BaseModel: The agent's output (for further validation)

        Raises:
            AssertionError: If execution fails or output type is wrong
        """
        logger.info(f"Testing {agent.name} execution...")

        # Execute agent
        result = agent.execute(input_data)

        # Verify output type
        assert isinstance(
            result, expected_output_type
        ), f"{agent.name} should return {expected_output_type.__name__}, got {type(result).__name__}"

        # Verify result is valid BaseModel
        assert isinstance(
            result, BaseModel
        ), f"{agent.name} output must be Pydantic BaseModel"

        logger.info(f"✅ {agent.name} execution successful")
        return result

    def test_agent_error_handling(
        self,
        agent: BaseAgent,
        invalid_input: Any,
        expected_error: Type[Exception] = None,
    ) -> None:
        """
        Test agent handles invalid input gracefully

        Verifies that agents don't crash with invalid input and
        raise appropriate exceptions.

        Args:
            agent: Agent instance to test
            invalid_input: Invalid input to test with
            expected_error: Expected exception type (defaults to ValueError or ValidationError)

        Raises:
            AssertionError: If agent doesn't handle errors properly
        """
        logger.info(f"Testing {agent.name} error handling...")

        # Default to expecting ValueError or ValidationError
        if expected_error is None:
            expected_errors = (ValueError, ValidationError, TypeError)
        else:
            expected_errors = expected_error

        # Agent should raise an exception for invalid input
        with pytest.raises(expected_errors):
            agent.execute(invalid_input)

        logger.info(f"✅ {agent.name} handles errors gracefully")

    def test_agent_idempotency(
        self,
        agent: BaseAgent,
        input_data: BaseModel,
        expected_output_type: Type[BaseModel],
    ) -> None:
        """
        Test that running agent multiple times produces consistent results

        Note: This tests structural idempotency, not exact output matching,
        since some agents may generate unique IDs or timestamps.

        Args:
            agent: Agent instance to test
            input_data: Valid input for the agent
            expected_output_type: Expected output type

        Raises:
            AssertionError: If outputs differ significantly
        """
        logger.info(f"Testing {agent.name} idempotency...")

        # Run agent twice
        result1 = agent.execute(input_data)
        result2 = agent.execute(input_data)

        # Both should be same type
        assert isinstance(result1, expected_output_type)
        assert isinstance(result2, expected_output_type)
        assert type(result1) == type(result2)

        logger.info(f"✅ {agent.name} produces consistent output types")

    def test_agent_properties_not_empty(self, agent: BaseAgent) -> None:
        """
        Test that agent properties contain meaningful values

        Verifies:
        - name is lowercase and snake_case or kebab-case
        - description is a complete sentence
        - no placeholder text

        Args:
            agent: Agent instance to test

        Raises:
            AssertionError: If properties don't meet quality standards
        """
        # Name should be lowercase
        assert agent.name == agent.name.lower(), f"{agent.name} should be lowercase"

        # Name should not contain spaces
        assert " " not in agent.name, f"{agent.name} should not contain spaces"

        # Description should be reasonable length
        assert (
            len(agent.description) >= 10
        ), f"{agent.name} description too short: '{agent.description}'"
        assert (
            len(agent.description) <= 200
        ), f"{agent.name} description too long: '{agent.description}'"

        # No placeholder text
        placeholders = ["todo", "tbd", "fixme", "placeholder", "xxx"]
        desc_lower = agent.description.lower()
        for placeholder in placeholders:
            assert (
                placeholder not in desc_lower
            ), f"{agent.name} description contains placeholder: '{placeholder}'"

        logger.info(f"✅ {agent.name} properties are high quality")

    def validate_output_schema(self, output: BaseModel, required_fields: list[str]) -> None:
        """
        Validate that output has all required fields

        Args:
            output: Agent output to validate
            required_fields: List of field names that must be present

        Raises:
            AssertionError: If required fields are missing
        """
        for field in required_fields:
            assert hasattr(output, field), f"Output missing required field: {field}"
            value = getattr(output, field)
            assert value is not None, f"Required field '{field}' is None"

        logger.info(f"✅ Output schema validated: {output.__class__.__name__}")


class AgentPerformanceHarness:
    """
    Performance testing utilities for agents

    Tests execution time, memory usage, and scalability.
    """

    def test_agent_performance(
        self,
        agent: BaseAgent,
        input_data: BaseModel,
        max_execution_time_seconds: float = 30.0,
    ) -> float:
        """
        Test agent completes within reasonable time

        Args:
            agent: Agent to test
            input_data: Valid input
            max_execution_time_seconds: Maximum allowed execution time

        Returns:
            float: Actual execution time in seconds

        Raises:
            AssertionError: If execution takes too long
        """
        import time

        start_time = time.time()
        agent.execute(input_data)
        execution_time = time.time() - start_time

        assert (
            execution_time <= max_execution_time_seconds
        ), f"{agent.name} took {execution_time:.2f}s (max: {max_execution_time_seconds}s)"

        logger.info(f"✅ {agent.name} completed in {execution_time:.2f}s")
        return execution_time


# Convenience function for quick testing
def run_all_standard_tests(
    agent: BaseAgent,
    valid_input: BaseModel,
    expected_output_type: Type[BaseModel],
    invalid_input: Any = "invalid",
) -> None:
    """
    Run all standard agent tests in one call

    Convenience function that runs:
    - Interface tests
    - Execution tests
    - Error handling tests
    - Property tests

    Args:
        agent: Agent to test
        valid_input: Valid input for execution test
        expected_output_type: Expected output type
        invalid_input: Invalid input for error handling test
    """
    harness = AgentTestHarness()

    harness.test_agent_interface(agent)
    harness.test_agent_execution(agent, valid_input, expected_output_type)
    harness.test_agent_error_handling(agent, invalid_input)
    harness.test_agent_properties_not_empty(agent)

    logger.info(f"✅ All standard tests passed for {agent.name}")
