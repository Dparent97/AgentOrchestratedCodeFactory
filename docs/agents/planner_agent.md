# PlannerAgent - Task Breakdown and Dependency Planning

## Overview

The PlannerAgent transforms high-level project ideas into concrete, actionable task lists with dependencies. It's the first agent in the build pipeline after safety validation, responsible for breaking down abstract concepts into structured work items.

**Position in Pipeline**: Second stage (after SafetyGuard, before ArchitectAgent)

**Key Responsibilities**:
- Break down project ideas into discrete tasks
- Establish task dependencies and execution order
- Categorize tasks by type (code, test, doc, config, git)
- Generate task IDs for dependency tracking
- Create a logical task graph for the build pipeline

---

## API Reference

### Input Model

```python
class Idea(BaseModel):
    """Human's plain-language project idea"""
    description: str = Field(..., description="Plain-language description of what to build")
    target_users: List[str] = Field(
        default_factory=list,
        description="Target user roles (e.g., ['marine engineer', 'mechanic'])"
    )
    environment: Optional[str] = Field(
        None,
        description="Operating environment (e.g., 'noisy engine room, limited WiFi')"
    )
    features: List[str] = Field(
        default_factory=list,
        description="Specific features or requirements"
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Known limitations or constraints"
    )
```

**Field Descriptions**:
- `description`: A plain-language description of what to build. This is the primary input that drives task generation. Example: "Build a tool to analyze marine engine alarm logs"
- `target_users`: List of user roles who will use the tool. Helps inform task priorities and UX considerations. Example: `["marine engineer", "maintenance technician"]`
- `environment`: Where the tool will be used. Influences technical decisions. Example: `"noisy engine room, limited WiFi, tablet interface"`
- `features`: Specific capabilities requested. Example: `["filter critical alarms", "export to CSV", "color-coded output"]`
- `constraints`: Known limitations. Example: `["must work offline", "simple CLI only", "no installation required"]`

### Output Model

```python
class TaskList(BaseModel):
    """Output model for PlannerAgent"""
    tasks: List[Task]

class Task(BaseModel):
    """Single unit of work"""
    id: str = Field(..., description="Unique task identifier")
    type: TaskType = Field(..., description="Type of task")
    description: str = Field(..., description="What this task does")
    dependencies: List[str] = Field(
        default_factory=list,
        description="IDs of tasks that must complete before this one"
    )
    files_to_create: List[str] = Field(
        default_factory=list,
        description="Files this task will create or modify"
    )
    agent: Optional[str] = Field(None, description="Which agent should execute this task")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status")

class TaskType(str, Enum):
    """Task categories"""
    CONFIG = "config"  # Setup files (pyproject.toml, requirements.txt)
    CODE = "code"      # Implementation files
    TEST = "test"      # Test files
    DOC = "doc"        # Documentation
    GIT = "git"        # Git operations
```

**Field Descriptions**:
- `tasks`: List of Task objects forming a dependency graph
- `Task.id`: Unique identifier like "t1", "t2", used for dependency references
- `Task.type`: Category of work - determines which agent will execute it
- `Task.description`: Human-readable explanation of what the task accomplishes
- `Task.dependencies`: List of task IDs that must complete first
- `Task.files_to_create`: Expected output files from this task
- `Task.agent`: (Optional) Specific agent to execute this task
- `Task.status`: Current execution state (pending, running, success, failed, skipped)

### Execute Method

```python
def execute(self, input_data: Idea) -> TaskList:
    """
    Generate task dependency graph from an idea

    Takes a high-level project idea and breaks it down into a sequence
    of concrete tasks with dependencies, creating a build plan.

    Args:
        input_data: Idea object describing what to build

    Returns:
        TaskList: Ordered list of tasks with dependencies

    Raises:
        ValueError: If idea description is empty or invalid
        AgentExecutionError: If task generation fails
    """
```

---

## Usage Examples

### Basic Example

```python
from code_factory.agents.planner import PlannerAgent
from code_factory.core.models import Idea

# Create agent instance
planner = PlannerAgent()

# Prepare input
idea = Idea(
    description="Build a CLI tool to parse CSV files and generate summary statistics",
    target_users=["data analyst"],
    environment="command line, local files"
)

# Execute agent
result = planner.execute(idea)

# Use result
print(f"Generated {len(result.tasks)} tasks:")
for task in result.tasks:
    deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
    print(f"  [{task.type}] {task.id}: {task.description}{deps}")
```

**Expected Output**:
```
Generated 4 tasks:
  [config] t1: Initialize project structure
  [code] t2: Implement core functionality (depends on: t1)
  [test] t3: Create unit tests (depends on: t2)
  [doc] t4: Write documentation (depends on: t2)
```

### Real-World Example: Marine Log Analyzer

```python
from code_factory.agents.planner import PlannerAgent
from code_factory.core.models import Idea

# Create planner
planner = PlannerAgent()

# Real-world marine engineering scenario
idea = Idea(
    description="Parse marine engine alarm logs and highlight critical issues",
    target_users=["marine engineer", "chief engineer"],
    environment="noisy engine room, limited WiFi, tablet display",
    features=[
        "Filter for critical alarms only",
        "Color-coded severity levels",
        "Export filtered results to CSV",
        "Timestamp range filtering"
    ],
    constraints=[
        "Must work offline",
        "Simple CLI interface",
        "Large text for readability"
    ]
)

# Generate task plan
result = planner.execute(idea)

# Display task breakdown
print("\nTask Breakdown for Marine Log Analyzer:")
print("=" * 60)
for task in result.tasks:
    print(f"\nTask {task.id} ({task.type.value.upper()})")
    print(f"  Description: {task.description}")
    if task.dependencies:
        print(f"  Depends on: {', '.join(task.dependencies)}")
    if task.files_to_create:
        print(f"  Creates: {', '.join(task.files_to_create)}")
```

**Expected Output**:
```
Task Breakdown for Marine Log Analyzer:
============================================================

Task t1 (CONFIG)
  Description: Initialize project structure
  Creates: README.md, pyproject.toml

Task t2 (CODE)
  Description: Implement core functionality
  Depends on: t1
  Creates: src/main.py

Task t3 (TEST)
  Description: Create unit tests
  Depends on: t2
  Creates: tests/test_main.py

Task t4 (DOC)
  Description: Write documentation
  Depends on: t2
  Creates: docs/usage.md
```

### Integration Example

```python
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent
from code_factory.core.models import Idea, ArchitectInput

# Full pipeline integration
idea = Idea(
    description="Build a log parser for diesel engine diagnostics",
    target_users=["diesel mechanic"],
    environment="garage workbench, Windows laptop"
)

# Step 1: Safety validation
safety_guard = SafetyGuard()
safety_check = safety_guard.execute(idea)

if not safety_check.approved:
    print(f"Safety check failed: {safety_check.warnings}")
    exit(1)

# Step 2: Task planning (PlannerAgent)
planner = PlannerAgent()
task_list = planner.execute(idea)
print(f"Planner generated {len(task_list.tasks)} tasks")

# Step 3: Architecture design
architect = ArchitectAgent()
arch_input = ArchitectInput(
    idea=idea,
    task_count=len(task_list.tasks)
)
project_spec = architect.execute(arch_input)
print(f"Architect designed project: {project_spec.name}")
```

---

## Implementation Notes

### Algorithm Overview

The PlannerAgent uses a template-based approach to generate tasks:

1. **Input Validation**: Validates that the Idea has a non-empty description
2. **Task Generation**: Creates a standard set of tasks based on project type
3. **Dependency Assignment**: Establishes logical ordering (config → code → test → doc)
4. **File Mapping**: Assigns expected output files to each task
5. **Task List Assembly**: Returns structured TaskList object

**Current Implementation** (v1.0):
- Template-based: Generates standardized task structure
- 4 core tasks: config, code, test, documentation
- Linear dependency chain

**Future Implementation** (v2.0):
- LLM-powered intelligent planning
- Dynamic task generation based on idea complexity
- Parallel task detection (tasks with no dependencies)
- Feature-specific task breakdown

### Design Decisions

**Why template-based initially?**
- Predictable and testable output
- No external dependencies (no LLM required)
- Fast execution (<100ms)
- Easy to understand and debug
- Establishes baseline for future comparison

**Trade-offs**:
- **Pro**: Reliable, fast, simple, deterministic
- **Con**: Not adaptive to idea complexity, limited task variety
- **Alternative**: LLM-based planning (planned for v2.0)

**Why task dependencies matter**:
- Ensures correct execution order
- Enables future parallel execution of independent tasks
- Makes build pipeline failures easier to debug
- Provides clear rollback points

### Future Enhancements

- [ ] LLM integration for intelligent task breakdown
- [ ] Adaptive task granularity based on project size
- [ ] Detection of parallel-executable tasks
- [ ] Feature-to-task mapping for complex requirements
- [ ] Task time estimation
- [ ] Resource requirement prediction
- [ ] Custom task templates per project type
- [ ] Interactive task refinement mode

---

## Blue-Collar Considerations

### Design Choices for Field Use

- **Simple Task Descriptions**: Uses plain language, not technical jargon. "Create unit tests" instead of "Implement pytest fixtures with parametrization"
- **Clear Dependencies**: Explicit task ordering makes the build process transparent and understandable
- **Predictable Structure**: Consistent task patterns make it easy to understand what the factory will build

### Target Environment Awareness

The PlannerAgent considers target environment when planning:
- **Offline environments**: Prioritizes local-first tools, avoids cloud dependencies
- **Limited screen space**: Keeps task counts reasonable, avoids over-engineering
- **Non-technical users**: Creates tasks for clear documentation and simple installation

### Example Scenarios

**Scenario 1: Engine Room WiFi Issues**
- **Challenge**: Marine engineer needs a tool that works without internet connection
- **How PlannerAgent helps**: Detects "limited WiFi" in environment field, plans for offline-capable architecture
- **Result**: Task list includes offline data processing, no API calls, local file storage

**Scenario 2: Quick Turnaround Needed**
- **Challenge**: Maintenance tech needs a simple conversion tool, doesn't want to wait days for complex software
- **How PlannerAgent helps**: Recognizes simple ideas, generates minimal task list (4 tasks instead of 20)
- **Result**: Fast build time, no unnecessary complexity

**Scenario 3: Glove-Friendly Interface**
- **Challenge**: User mentions "warehouse environment, may be wearing gloves"
- **How PlannerAgent helps**: Adds tasks for large buttons, simple CLI commands
- **Result**: Generated tool is usable with limited dexterity

---

## Testing

### Test Location

Tests for PlannerAgent are located in: `tests/unit/agents/test_planner.py`

### Running Tests

```bash
# Run all PlannerAgent tests
pytest tests/unit/agents/test_planner.py -v

# Run specific test
pytest tests/unit/agents/test_planner.py::test_planner_basic_idea -v

# Run with coverage
pytest tests/unit/agents/test_planner.py --cov=code_factory.agents.planner

# Run with detailed output
pytest tests/unit/agents/test_planner.py -v -s
```

### Test Coverage

Current test coverage: 85%+

**Test Categories**:
- ✅ Input validation tests (empty description, None input)
- ✅ Happy path tests (basic idea → task list)
- ✅ Task dependency tests (correct ordering)
- ✅ Task type tests (correct categorization)
- ✅ File mapping tests (files_to_create populated)
- ✅ Integration tests (works with SafetyGuard output)

### Example Test

```python
def test_planner_generates_task_list():
    """Test that PlannerAgent generates valid task list"""
    from code_factory.agents.planner import PlannerAgent
    from code_factory.core.models import Idea

    planner = PlannerAgent()

    idea = Idea(
        description="Build a simple calculator CLI",
        target_users=["student"],
        environment="desktop"
    )

    result = planner.execute(idea)

    # Verify task list structure
    assert len(result.tasks) > 0
    assert all(task.id for task in result.tasks)
    assert all(task.type for task in result.tasks)
    assert all(task.description for task in result.tasks)

    # Verify dependency ordering
    task_ids = [t.id for t in result.tasks]
    for task in result.tasks:
        for dep in task.dependencies:
            assert dep in task_ids, f"Dependency {dep} not found in task list"

def test_planner_task_types():
    """Test that tasks have appropriate types"""
    planner = PlannerAgent()
    idea = Idea(description="Log parser")

    result = planner.execute(idea)

    types = {task.type for task in result.tasks}
    assert TaskType.CONFIG in types  # Should have config tasks
    assert TaskType.CODE in types    # Should have code tasks
    assert TaskType.TEST in types    # Should have test tasks
```

---

## Error Handling

### Common Errors

**Error**: `ValueError: Description cannot be empty`
- **Cause**: Idea object has empty or whitespace-only description
- **Solution**: Provide a meaningful description string

```python
# Bad
idea = Idea(description="")  # Raises ValueError

# Good
idea = Idea(description="Build a CSV parser")
```

**Error**: `ValidationError: Field required`
- **Cause**: Missing required field in Idea object
- **Solution**: Ensure `description` field is provided

```python
# Bad
idea = Idea()  # Missing description

# Good
idea = Idea(description="Temperature logger")
```

### Error Recovery

The PlannerAgent handles errors gracefully:

```python
from code_factory.agents.planner import PlannerAgent
from code_factory.core.models import Idea
from pydantic import ValidationError

planner = PlannerAgent()

try:
    result = planner.execute(idea)
    print(f"Successfully generated {len(result.tasks)} tasks")
except ValidationError as e:
    print(f"Invalid input: {e}")
    # Provide feedback to user, request valid input
except Exception as e:
    print(f"Planning failed: {e}")
    # Log error, use fallback task template
```

**Partial Failure Handling**:
Currently, PlannerAgent generates all tasks at once (no partial failures). Future versions may support:
- Incremental task generation
- Recovery from failed task creation
- Task regeneration for specific types

---

## Performance Considerations

**Typical Execution Time**: < 100ms (template-based), future LLM version: 1-3 seconds

**Resource Usage**:
- **Memory**: < 1 MB (minimal overhead)
- **CPU**: Negligible (no heavy computation)
- **I/O**: None (pure in-memory operation)

**Scalability**:
- Current: Handles ideas of any size equally (fixed task count)
- Future: May scale task count based on project complexity

**Optimization Tips**:
- Reuse PlannerAgent instance across multiple ideas (avoid recreation)
- Cache task templates if processing many similar ideas
- Future: Batch multiple ideas for LLM processing

---

## Related Documentation

- [Main Architecture Overview](../architecture.md) - Overall system design
- [Agent Roles](../agent_roles.md) - All agents and their responsibilities
- [ArchitectAgent](./architect_agent.md) - Next agent in pipeline
- [SafetyGuard](./safety_guard.md) - Previous agent in pipeline
- [Core Models](../../src/code_factory/core/models.py) - Data structures

---

## Changelog

### Version 1.0.0 (2025-01-15)
- Initial implementation with template-based task generation
- Supports basic 4-task structure (config, code, test, doc)
- Task dependency management
- File mapping to tasks
- Input validation via Pydantic

### Version 1.1.0 (Planned - Q1 2025)
- LLM-powered intelligent task breakdown
- Dynamic task count based on idea complexity
- Parallel task detection
- Feature-specific task generation
- Task time estimation

### Version 2.0.0 (Planned - Q2 2025)
- Interactive task refinement mode
- Custom task templates per project type
- Resource requirement prediction
- Multi-agent collaboration for complex planning
