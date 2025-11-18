"""
Example Tests - Demonstrates how to use the test harness

These are working examples that show best practices for testing agents.
Run with: pytest tests/harness/examples.py -v
"""

import pytest
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.models import Idea, TaskType

# Import test harness utilities
from tests.harness.fixtures import (
    create_test_idea,
    create_marine_engineer_idea,
    create_data_analyst_idea,
    create_simple_calculator_idea,
    create_dangerous_idea,
)
from tests.harness.assertions import (
    assert_valid_task_list,
    assert_task_dependencies_valid,
    assert_no_circular_dependencies,
    assert_has_task_type,
    assert_valid_project_spec,
    assert_safety_approved,
    assert_safety_rejected,
    assert_blue_collar_friendly,
)
from tests.harness.validators import (
    validate_task_structure,
    validate_spec_structure,
    validate_pipeline_flow,
)
from tests.harness.decorators import (
    timed_test,
    agent_test,
    fast_test,
)
from tests.harness.generators import (
    generate_test_scenarios,
    generate_edge_cases,
)


# ============================================================================
# Example 1: Basic PlannerAgent Test with Fixtures
# ============================================================================

def test_planner_with_basic_fixture():
    """Example: Test PlannerAgent using basic fixture"""

    # Use fixture for test data
    idea = create_test_idea(description="Build a CSV parser")

    # Execute agent
    planner = PlannerAgent()
    result = planner.execute(idea)

    # Use specialized assertions
    assert_valid_task_list(result.tasks, min_tasks=1)
    assert_task_dependencies_valid(result.tasks)
    assert_no_circular_dependencies(result.tasks)


# ============================================================================
# Example 2: ArchitectAgent Test with Role-Specific Fixture
# ============================================================================

def test_architect_with_marine_scenario():
    """Example: Test ArchitectAgent with marine engineering scenario"""

    # Use role-specific fixture
    idea = create_marine_engineer_idea()

    # Execute agent
    architect = ArchitectAgent()
    spec = architect.execute(idea)

    # Validate spec structure
    assert_valid_project_spec(spec)

    # Check blue-collar friendliness
    assert_blue_collar_friendly(spec)


# ============================================================================
# Example 3: SafetyGuard Test with Expected Rejection
# ============================================================================

def test_safety_guard_rejects_dangerous_idea():
    """Example: Test SafetyGuard blocks dangerous ideas"""

    # Use dangerous fixture
    idea = create_dangerous_idea()

    # Execute safety check
    safety = SafetyGuard()
    check = safety.execute(idea)

    # Should be rejected
    assert_safety_rejected(check)
    assert len(check.warnings) > 0


# ============================================================================
# Example 4: Timed Test with Decorator
# ============================================================================

@timed_test(max_seconds=1.0)
def test_planner_performance():
    """Example: Test must complete within 1 second"""

    idea = create_simple_calculator_idea()

    planner = PlannerAgent()
    result = planner.execute(idea)

    assert_valid_task_list(result.tasks)


# ============================================================================
# Example 5: Agent Test Decorator
# ============================================================================

@agent_test("PlannerAgent", timeout_seconds=2.0)
def test_planner_with_decorator():
    """Example: Using agent_test decorator for metadata and timing"""

    idea = create_data_analyst_idea()

    planner = PlannerAgent()
    result = planner.execute(idea)

    assert_has_task_type(result.tasks, TaskType.CODE)
    assert_has_task_type(result.tasks, TaskType.TEST)


# ============================================================================
# Example 6: Validator Usage (Detailed Feedback)
# ============================================================================

def test_task_structure_with_validator():
    """Example: Using validators for detailed feedback"""

    idea = create_test_idea(description="Complex data pipeline")

    planner = PlannerAgent()
    result = planner.execute(idea)

    # Use validator instead of assertion for detailed feedback
    validation = validate_task_structure(result.tasks)

    # Print detailed report
    if not validation.is_valid:
        print("\nValidation Report:")
        print(validation)

    # Still assert for test pass/fail
    assert validation.is_valid, "Task structure validation failed"


# ============================================================================
# Example 7: Complete Pipeline Test
# ============================================================================

@timed_test(max_seconds=3.0)
def test_complete_wave1_pipeline():
    """Example: Test complete Wave 1 pipeline"""

    # Create test data
    idea = create_marine_engineer_idea()

    # Stage 1: Safety
    safety = SafetyGuard()
    check = safety.execute(idea)
    assert_safety_approved(check)

    # Stage 2: Planning
    planner = PlannerAgent()
    task_result = planner.execute(idea)
    assert_valid_task_list(task_result.tasks, min_tasks=4)

    # Stage 3: Architecture
    architect = ArchitectAgent()
    arch_input = ArchitectInput(idea=idea, task_count=len(task_result.tasks))
    spec = architect.execute(arch_input)
    assert_valid_project_spec(spec)

    # Validate entire pipeline flow
    pipeline_validation = validate_pipeline_flow(
        idea=idea,
        safety_check=check,
        tasks=task_result.tasks,
        spec=spec,
    )

    assert pipeline_validation.is_valid, "Pipeline validation failed"


# ============================================================================
# Example 8: Parametrized Test with Scenarios
# ============================================================================

@pytest.mark.parametrize("scenario", generate_test_scenarios())
def test_planner_with_scenarios(scenario):
    """Example: Test PlannerAgent with multiple generated scenarios"""

    idea = scenario["idea"]
    expected_range = scenario["expected_task_range"]

    planner = PlannerAgent()
    result = planner.execute(idea)

    # Check task count is in expected range
    min_tasks, max_tasks = expected_range
    task_count = len(result.tasks)

    assert min_tasks <= task_count <= max_tasks, \
        f"Task count {task_count} not in expected range [{min_tasks}, {max_tasks}] " \
        f"for scenario '{scenario['name']}'"


# ============================================================================
# Example 9: Edge Case Testing
# ============================================================================

@pytest.mark.parametrize("case_name,idea", generate_edge_cases())
def test_planner_edge_cases(case_name, idea):
    """Example: Test PlannerAgent with edge cases"""

    planner = PlannerAgent()

    try:
        result = planner.execute(idea)

        # If execution succeeds, validate output
        assert_valid_task_list(result.tasks, min_tasks=1)
        print(f"✓ Edge case '{case_name}' handled successfully")

    except Exception as e:
        # Some edge cases may raise errors - that's OK
        print(f"⚠️  Edge case '{case_name}' raised {type(e).__name__}: {str(e)}")
        # Re-raise if it's an unexpected error type
        if not isinstance(e, (ValueError, TypeError)):
            raise


# ============================================================================
# Example 10: Fast Test Decorator
# ============================================================================

@fast_test(max_seconds=0.5)
def test_safety_guard_quick():
    """Example: Test that must be very fast"""

    idea = create_test_idea(description="Simple tool")

    safety = SafetyGuard()
    check = safety.execute(idea)

    assert_safety_approved(check)


# ============================================================================
# Example 11: Spec Validation with Detailed Feedback
# ============================================================================

def test_architect_spec_validation():
    """Example: Validate ProjectSpec with detailed feedback"""

    idea = create_data_analyst_idea()

    architect = ArchitectAgent()
    spec = architect.execute(idea)

    # Use validator for detailed report
    validation = validate_spec_structure(spec)

    # Print any warnings
    if validation.warnings:
        print("\nWarnings:")
        for warning in validation.warnings:
            print(f"  ⚠️  {warning}")

    # Print info
    if validation.info:
        print("\nInfo:")
        for info in validation.info:
            print(f"  ℹ️  {info}")

    assert validation.is_valid


# ============================================================================
# Example 12: Multiple Assertions in Sequence
# ============================================================================

def test_planner_comprehensive():
    """Example: Multiple assertions for thorough validation"""

    idea = create_marine_engineer_idea()

    planner = PlannerAgent()
    result = planner.execute(idea)

    # Structure checks
    assert_valid_task_list(result.tasks, min_tasks=4)

    # Dependency checks
    assert_task_dependencies_valid(result.tasks)
    assert_no_circular_dependencies(result.tasks)

    # Content checks
    assert_has_task_type(result.tasks, TaskType.CONFIG)
    assert_has_task_type(result.tasks, TaskType.CODE)
    assert_has_task_type(result.tasks, TaskType.TEST)
    assert_has_task_type(result.tasks, TaskType.DOC)


# ============================================================================
# Example 13: Comparing Agents with Same Input
# ============================================================================

def test_consistency_across_agents():
    """Example: Test consistency between PlannerAgent and ArchitectAgent"""

    idea = create_simple_calculator_idea()

    # Plan tasks
    planner = PlannerAgent()
    tasks = planner.execute(idea)

    # Design architecture
    architect = ArchitectAgent()
    spec = architect.execute(idea)

    # Validate consistency
    assert_valid_task_list(tasks.tasks)
    assert_valid_project_spec(spec)

    # Check that spec.user_profile matches idea.target_users
    if spec.user_profile:
        assert spec.user_profile in idea.target_users


# ============================================================================
# Example 14: Testing with Custom Idea
# ============================================================================

def test_planner_with_custom_idea():
    """Example: Create custom test idea inline"""

    # Custom idea for specific test case
    idea = Idea(
        description="Build a tool to monitor server logs and send alerts",
        target_users=["system administrator", "devops engineer"],
        environment="data center, 24/7 operation",
        features=[
            "Real-time log monitoring",
            "Regex pattern matching",
            "Email/Slack alerts",
            "Log rotation handling",
        ],
        constraints=[
            "Low CPU usage",
            "Minimal memory footprint",
            "Should not interfere with server operation",
        ],
    )

    planner = PlannerAgent()
    result = planner.execute(idea)

    # Validate
    assert_valid_task_list(result.tasks, min_tasks=5)

    # Should have tasks for monitoring, alerting, and testing
    assert_has_task_type(result.tasks, TaskType.CODE)
    assert_has_task_type(result.tasks, TaskType.TEST)


# ============================================================================
# Example 15: Integration Test with All Validators
# ============================================================================

def test_full_validation_suite():
    """Example: Run all validators for comprehensive check"""

    idea = create_marine_engineer_idea()

    # Execute pipeline
    safety = SafetyGuard()
    check = safety.execute(idea)

    planner = PlannerAgent()
    tasks = planner.execute(idea)

    architect = ArchitectAgent()
    spec = architect.execute(idea)

    # Validate each component
    task_validation = validate_task_structure(tasks.tasks)
    spec_validation = validate_spec_structure(spec)
    pipeline_validation = validate_pipeline_flow(idea, check, tasks.tasks, spec)

    # Print comprehensive report
    print("\n=== Task Validation ===")
    print(task_validation)

    print("\n=== Spec Validation ===")
    print(spec_validation)

    print("\n=== Pipeline Validation ===")
    print(pipeline_validation)

    # All must be valid
    assert task_validation.is_valid
    assert spec_validation.is_valid
    assert pipeline_validation.is_valid


# ============================================================================
# Helper function for running examples
# ============================================================================

if __name__ == "__main__":
    print("Test Harness Examples")
    print("=" * 60)
    print("\nRun these examples with:")
    print("  pytest tests/harness/examples.py -v")
    print("  pytest tests/harness/examples.py::test_planner_with_basic_fixture -v")
    print("  pytest tests/harness/examples.py -v -s  # With print output")
    print("\nOr run individual examples:")
    print("  python tests/harness/examples.py")
    print("\n" + "=" * 60)

    # Run one example
    print("\nRunning Example: Basic PlannerAgent Test")
    test_planner_with_basic_fixture()
    print("✓ Example passed!")
