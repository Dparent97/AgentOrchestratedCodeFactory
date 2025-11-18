"""
Test Harness for Agent-Orchestrated Code Factory

Provides reusable testing utilities for all agents:
- Fixture helpers for creating test data
- Assertion utilities for validating outputs
- Mock data generators for common scenarios
- Result validators for comprehensive checks
- Test decorators for timing and retries
"""

from tests.harness.fixtures import (
    create_test_idea,
    create_test_task,
    create_test_project_spec,
    create_test_safety_check,
    create_marine_engineer_idea,
    create_data_analyst_idea,
    create_mechanic_idea,
)

from tests.harness.assertions import (
    assert_valid_task_list,
    assert_valid_project_spec,
    assert_valid_safety_check,
    assert_task_dependencies_valid,
    assert_no_circular_dependencies,
    assert_blue_collar_friendly,
)

from tests.harness.validators import (
    validate_agent_output,
    validate_task_structure,
    validate_spec_structure,
    validate_pipeline_flow,
)

from tests.harness.decorators import (
    timed_test,
    retry_on_failure,
    expect_agent_error,
)

from tests.harness.generators import (
    generate_random_idea,
    generate_test_scenarios,
    generate_edge_cases,
)

__all__ = [
    # Fixtures
    "create_test_idea",
    "create_test_task",
    "create_test_project_spec",
    "create_test_safety_check",
    "create_marine_engineer_idea",
    "create_data_analyst_idea",
    "create_mechanic_idea",
    # Assertions
    "assert_valid_task_list",
    "assert_valid_project_spec",
    "assert_valid_safety_check",
    "assert_task_dependencies_valid",
    "assert_no_circular_dependencies",
    "assert_blue_collar_friendly",
    # Validators
    "validate_agent_output",
    "validate_task_structure",
    "validate_spec_structure",
    "validate_pipeline_flow",
    # Decorators
    "timed_test",
    "retry_on_failure",
    "expect_agent_error",
    # Generators
    "generate_random_idea",
    "generate_test_scenarios",
    "generate_edge_cases",
]
