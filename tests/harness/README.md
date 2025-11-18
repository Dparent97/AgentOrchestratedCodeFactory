# Agent Test Harness

Comprehensive testing utilities for the Agent-Orchestrated Code Factory.

## Overview

The test harness provides a complete toolkit for testing agents:

- **Fixtures** - Pre-configured test data for common scenarios
- **Assertions** - Specialized checks for agent outputs
- **Validators** - Comprehensive validation with detailed feedback
- **Decorators** - Timing, retries, and error handling
- **Generators** - Random and scenario-based test data

---

## Quick Start

```python
from tests.harness import (
    create_marine_engineer_idea,
    assert_valid_task_list,
    validate_spec_structure,
    timed_test,
)

@timed_test(max_seconds=1.0)
def test_planner_marine_scenario():
    """Test PlannerAgent with marine engineering scenario"""
    from code_factory.agents.planner import PlannerAgent

    # Use pre-built fixture
    idea = create_marine_engineer_idea()

    # Execute agent
    planner = PlannerAgent()
    result = planner.execute(idea)

    # Use specialized assertion
    assert_valid_task_list(result.tasks, min_tasks=4)
```

---

## Fixtures

Pre-configured test objects for common scenarios.

### Basic Fixtures

```python
from tests.harness.fixtures import (
    create_test_idea,
    create_test_task,
    create_test_project_spec,
)

# Simple idea
idea = create_test_idea(description="Build a log parser")

# Custom idea
idea = create_test_idea(
    description="Temperature monitor",
    target_users=["marine engineer"],
    environment="engine room, noisy",
)

# Task
task = create_test_task(
    task_id="t1",
    task_type=TaskType.CODE,
    description="Implement parser",
)

# ProjectSpec
spec = create_test_project_spec(
    name="my-tool",
    tech_stack={"language": "python", "cli": "typer"},
)
```

### Role-Specific Fixtures

```python
from tests.harness.fixtures import (
    create_marine_engineer_idea,
    create_data_analyst_idea,
    create_mechanic_idea,
)

# Marine engineer scenario
idea = create_marine_engineer_idea()
# Returns: Idea with engine room environment, alarm logs, offline constraints

# Data analyst scenario
idea = create_data_analyst_idea()
# Returns: Idea with desktop environment, data processing features

# Mechanic scenario
idea = create_mechanic_idea()
# Returns: Idea with garage environment, glove-friendly interface
```

### Edge Cases

```python
from tests.harness.fixtures import (
    create_minimal_idea,
    create_dangerous_idea,
    create_ambiguous_idea,
)

# Minimal valid input
idea = create_minimal_idea()  # Just description="Build a tool"

# Should be blocked by SafetyGuard
idea = create_dangerous_idea()  # Contains "control industrial equipment"

# Vague description
idea = create_ambiguous_idea()  # "Make something useful"
```

### Task Lists

```python
from tests.harness.fixtures import (
    create_linear_task_list,
    create_parallel_task_list,
    create_complex_dependency_graph,
)

# Simple linear dependencies: t1 → t2 → t3 → t4
tasks = create_linear_task_list()

# Parallel execution opportunities
tasks = create_parallel_task_list()
#  t1
#  ├─ t2 ─ t4
#  └─ t3 ─ t5
#     └─── t6

# Complex multi-dependency graph
tasks = create_complex_dependency_graph()
```

---

## Assertions

Specialized assertions for validating agent outputs.

### Task List Assertions

```python
from tests.harness.assertions import (
    assert_valid_task_list,
    assert_task_dependencies_valid,
    assert_no_circular_dependencies,
    assert_has_task_type,
)

# Validate task list structure
assert_valid_task_list(tasks, min_tasks=4)

# Check dependencies are valid
assert_task_dependencies_valid(tasks)

# Ensure no circular dependencies
assert_no_circular_dependencies(tasks)

# Check for specific task type
assert_has_task_type(tasks, TaskType.TEST)
```

### ProjectSpec Assertions

```python
from tests.harness.assertions import (
    assert_valid_project_spec,
    assert_has_tech_stack_key,
    assert_has_dependency,
    assert_folder_exists,
)

# Validate complete spec
assert_valid_project_spec(spec)

# Check tech stack
assert_has_tech_stack_key(spec, "language")
assert_has_tech_stack_key(spec, "cli_framework")

# Check dependencies
assert_has_dependency(spec, "typer")
assert_has_dependency(spec, "pytest")

# Check folder structure
assert_folder_exists(spec, "src/")
assert_folder_exists(spec, "tests/")
```

### SafetyCheck Assertions

```python
from tests.harness.assertions import (
    assert_valid_safety_check,
    assert_safety_approved,
    assert_safety_rejected,
    assert_has_warning,
)

# Validate structure
assert_valid_safety_check(check)

# Check approval status
assert_safety_approved(check)  # Passes if approved=True
assert_safety_rejected(check)  # Passes if approved=False

# Check warnings
assert_has_warning(check, "equipment")  # Check for keyword in warnings
```

### Blue-Collar Assertions

```python
from tests.harness.assertions import (
    assert_blue_collar_friendly,
    assert_offline_capable,
)

# Check design follows blue-collar principles
assert_blue_collar_friendly(spec)
# Validates: CLI over web, minimal dependencies, clear entry point

# Check offline capability
assert_offline_capable(spec)
# Ensures no cloud dependencies
```

---

## Validators

Comprehensive validation with detailed feedback (doesn't raise exceptions).

### Task Validation

```python
from tests.harness.validators import validate_task_structure

result = validate_task_structure(tasks)

if result.is_valid:
    print("✓ Task structure is valid")
else:
    print(f"✗ Validation failed:")
    for error in result.errors:
        print(f"  - {error}")

# Print full report
print(result)
# Output:
# ✓ Validation passed
#
# Info (3):
#   - Task count: 4
#   - No circular dependencies detected
#   - Task type distribution: {'config': 1, 'code': 1, 'test': 1, 'doc': 1}
```

### Spec Validation

```python
from tests.harness.validators import validate_spec_structure

result = validate_spec_structure(spec)

print(f"Valid: {result.is_valid}")
print(f"Errors: {len(result.errors)}")
print(f"Warnings: {len(result.warnings)}")

# Access details
for warning in result.warnings:
    print(f"⚠️  {warning}")
```

### Pipeline Validation

```python
from tests.harness.validators import validate_pipeline_flow

# Validate entire Wave 1 pipeline
result = validate_pipeline_flow(
    idea=idea,
    safety_check=safety_check,
    tasks=tasks,
    spec=spec,
)

# Get summary
from tests.harness.validators import get_validation_summary
summary = get_validation_summary(result)
print(f"Valid: {summary['is_valid']}")
print(f"Errors: {summary['error_count']}")
print(f"Warnings: {summary['warning_count']}")
```

---

## Decorators

Test decorators for timing, retries, and error handling.

### Timing Decorator

```python
from tests.harness.decorators import timed_test

@timed_test(max_seconds=1.0)
def test_fast_planner():
    """Test must complete within 1 second"""
    planner = PlannerAgent()
    result = planner.execute(idea)
    assert result is not None

# Without time limit (just report)
@timed_test()
def test_any_operation():
    result = agent.execute(data)
```

### Retry Decorator

```python
from tests.harness.decorators import retry_on_failure

@retry_on_failure(max_retries=3, delay_seconds=0.5)
def test_flaky_operation():
    """Will retry up to 3 times on failure"""
    result = agent.execute(idea)
    assert result.tasks is not None
```

### Error Expectation

```python
from tests.harness.decorators import expect_agent_error

@expect_agent_error(ValueError, "description cannot be empty")
def test_empty_description():
    """Test should raise ValueError with specific message"""
    planner = PlannerAgent()
    planner.execute(Idea(description=""))  # Should raise
```

### Benchmarking

```python
from tests.harness.decorators import benchmark

@benchmark(iterations=100, warmup=10)
def test_planner_performance():
    """Benchmark planner over 100 iterations"""
    planner.execute(idea)

# Output:
# 📈 Benchmark Results for 'test_planner_performance':
#    Average: 45.32ms
#    Median:  44.89ms
#    Min:     41.23ms
#    Max:     52.17ms
```

### Agent Test Decorator

```python
from tests.harness.decorators import agent_test

@agent_test("PlannerAgent", timeout_seconds=2.0)
def test_planner_basic():
    """Combined timing and metadata for agent testing"""
    planner = PlannerAgent()
    result = planner.execute(idea)

# Output:
# 🧪 Testing PlannerAgent: test_planner_basic
# ✓ PlannerAgent test passed in 0.087s
```

### Combined Decorators

```python
from tests.harness.decorators import fast_test, slow_test, flaky_test

@fast_test(max_seconds=0.3)
def test_quick_validation():
    """Must be very fast"""
    validator.check(data)

@slow_test(min_seconds=2.0)
def test_complex_operation():
    """Expected to be slow"""
    agent.execute(complex_idea)

@flaky_test(max_retries=5)
def test_timing_sensitive():
    """Known to be flaky, retry 5 times"""
    result = agent.execute(idea)
```

---

## Generators

Generate random test data and scenarios.

### Random Ideas

```python
from tests.harness.generators import (
    generate_random_idea,
    generate_random_ideas,
)

# Single random idea
idea = generate_random_idea()

# Multiple random ideas
ideas = generate_random_ideas(count=10)

# Use in tests
for idea in ideas:
    result = planner.execute(idea)
    assert len(result.tasks) > 0
```

### Test Scenarios

```python
from tests.harness.generators import generate_test_scenarios

scenarios = generate_test_scenarios()

for scenario in scenarios:
    print(f"Testing: {scenario['name']}")
    idea = scenario['idea']
    expected_range = scenario['expected_task_range']

    result = planner.execute(idea)

    min_tasks, max_tasks = expected_range
    assert min_tasks <= len(result.tasks) <= max_tasks
```

### Edge Cases

```python
from tests.harness.generators import generate_edge_cases

edge_cases = generate_edge_cases()

for case_name, idea in edge_cases:
    print(f"Testing edge case: {case_name}")
    try:
        result = planner.execute(idea)
    except Exception as e:
        print(f"  Handled: {type(e).__name__}")
```

### Safety Test Cases

```python
from tests.harness.generators import generate_safety_test_cases

safety_cases = generate_safety_test_cases()

for case_name, idea, should_approve in safety_cases:
    check = safety_guard.execute(idea)
    assert check.approved == should_approve, \
        f"{case_name}: Expected approved={should_approve}"
```

### Domain-Specific Generation

```python
from tests.harness.generators import (
    generate_blue_collar_ideas,
    generate_data_processing_ideas,
)

# Blue-collar scenarios
blue_collar_ideas = generate_blue_collar_ideas(count=5)
for idea in blue_collar_ideas:
    # Test offline capability, simple interface, etc.
    ...

# Data processing scenarios
data_ideas = generate_data_processing_ideas(count=5)
for idea in data_ideas:
    # Test data handling, performance, etc.
    ...
```

---

## Complete Example

Here's a complete test using multiple harness features:

```python
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent
from code_factory.agents.safety_guard import SafetyGuard

from tests.harness import (
    # Fixtures
    create_marine_engineer_idea,
    # Assertions
    assert_valid_task_list,
    assert_valid_project_spec,
    assert_safety_approved,
    # Validators
    validate_pipeline_flow,
    # Decorators
    timed_test,
)


@timed_test(max_seconds=2.0)
def test_complete_wave1_pipeline():
    """Test complete Wave 1 pipeline with marine engineering scenario"""

    # Stage 1: Create test data
    idea = create_marine_engineer_idea(
        description="Parse marine diesel engine alarm logs and highlight critical issues"
    )

    # Stage 2: Safety validation
    safety = SafetyGuard()
    check = safety.execute(idea)
    assert_safety_approved(check)

    # Stage 3: Task planning
    planner = PlannerAgent()
    task_result = planner.execute(idea)
    assert_valid_task_list(task_result.tasks, min_tasks=4)

    # Stage 4: Architecture design
    architect = ArchitectAgent()
    spec = architect.execute(idea)
    assert_valid_project_spec(spec)

    # Stage 5: Validate pipeline flow
    validation = validate_pipeline_flow(
        idea=idea,
        safety_check=check,
        tasks=task_result.tasks,
        spec=spec,
    )

    if not validation.is_valid:
        print("\nValidation failed:")
        for error in validation.errors:
            print(f"  ✗ {error}")
        for warning in validation.warnings:
            print(f"  ⚠️  {warning}")

    assert validation.is_valid, "Pipeline validation failed"
    print("\n✓ Complete Wave 1 pipeline test passed!")
```

---

## Best Practices

### 1. Use Fixtures for Consistency

```python
# ✓ Good: Use fixtures
idea = create_marine_engineer_idea()

# ✗ Bad: Create manually each time
idea = Idea(
    description="Parse marine engine logs...",
    target_users=["marine engineer"],
    # ... lots of boilerplate
)
```

### 2. Use Validators for Detailed Feedback

```python
# ✓ Good: Use validator for detailed feedback
result = validate_task_structure(tasks)
if not result.is_valid:
    print(result)  # See all errors and warnings

# ✗ Less helpful: Just assert
assert len(tasks) > 0
```

### 3. Combine Decorators

```python
# ✓ Good: Stack decorators
@agent_test("PlannerAgent", timeout_seconds=1.0)
@retry_on_failure(max_retries=3)
def test_planner():
    ...

# Works: timing + retry + metadata
```

### 4. Test with Multiple Scenarios

```python
# ✓ Good: Test multiple scenarios
scenarios = generate_test_scenarios()
for scenario in scenarios:
    result = agent.execute(scenario['idea'])
    # Validate against expectations

# ✗ Limited: Only test one scenario
idea = create_test_idea()
result = agent.execute(idea)
```

### 5. Use Appropriate Assertions

```python
# ✓ Good: Use specialized assertion
assert_blue_collar_friendly(spec)

# ✗ Less clear: Generic assertion
assert "cli" in str(spec.tech_stack).lower()
```

---

## API Reference

### Fixtures Module

| Function | Returns | Description |
|----------|---------|-------------|
| `create_test_idea()` | Idea | Basic test idea |
| `create_test_task()` | Task | Basic test task |
| `create_test_project_spec()` | ProjectSpec | Basic test spec |
| `create_marine_engineer_idea()` | Idea | Marine engineering scenario |
| `create_data_analyst_idea()` | Idea | Data analyst scenario |
| `create_mechanic_idea()` | Idea | Mechanic scenario |
| `create_linear_task_list()` | List[Task] | Linear dependency chain |
| `create_parallel_task_list()` | List[Task] | Parallel tasks |

### Assertions Module

| Function | Checks | Raises |
|----------|--------|--------|
| `assert_valid_task_list()` | Task structure | AssertionError |
| `assert_task_dependencies_valid()` | Dependencies exist | AssertionError |
| `assert_no_circular_dependencies()` | No cycles | AssertionError |
| `assert_valid_project_spec()` | Spec structure | AssertionError |
| `assert_blue_collar_friendly()` | Design principles | AssertionError |

### Validators Module

| Function | Returns | Description |
|----------|---------|-------------|
| `validate_task_structure()` | ValidationResult | Comprehensive task validation |
| `validate_spec_structure()` | ValidationResult | Comprehensive spec validation |
| `validate_pipeline_flow()` | ValidationResult | Pipeline consistency |

### Generators Module

| Function | Returns | Description |
|----------|---------|-------------|
| `generate_random_idea()` | Idea | Random plausible idea |
| `generate_test_scenarios()` | List[Dict] | Common scenarios |
| `generate_edge_cases()` | List[Tuple] | Edge case ideas |
| `generate_safety_test_cases()` | List[Tuple] | Safety test data |

### Decorators Module

| Decorator | Purpose | Args |
|-----------|---------|------|
| `@timed_test()` | Time execution | max_seconds |
| `@retry_on_failure()` | Retry on fail | max_retries, delay_seconds |
| `@expect_agent_error()` | Expect error | error_type, message_contains |
| `@benchmark()` | Performance test | iterations, warmup |
| `@agent_test()` | Agent metadata | agent_name, timeout_seconds |

---

## Troubleshooting

### Import Errors

```python
# If you get import errors, ensure the package is installed
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/AgentOrchestratedCodeFactory"
```

### Assertion Failures

```python
# Use validators for detailed feedback instead of assertions
result = validate_task_structure(tasks)
print(result)  # See exactly what's wrong

# Then fix and use assertion
assert_valid_task_list(tasks)
```

---

## Contributing

To add new test utilities:

1. **Fixtures**: Add to `fixtures.py`
2. **Assertions**: Add to `assertions.py`
3. **Validators**: Add to `validators.py`
4. **Decorators**: Add to `decorators.py`
5. **Generators**: Add to `generators.py`
6. **Update `__init__.py`**: Export new functions

---

## Related Documentation

- [Architecture Overview](../../docs/architecture.md)
- [Agent Integration Guide](../../docs/agent_integration.md)
- [PlannerAgent Docs](../../docs/agents/planner_agent.md)
- [ArchitectAgent Docs](../../docs/agents/architect_agent.md)
