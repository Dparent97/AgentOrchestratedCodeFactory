# Agent Integration Guide

## Overview

This guide explains how agents in the Code Factory work together as a coordinated pipeline. Each agent transforms data from one stage to the next, building up from a simple idea to a complete working project.

**Wave 1 Agents** (documented here):
- SafetyGuard → PlannerAgent → ArchitectAgent

**Future Waves**:
- ImplementerAgent, TesterAgent, DocWriterAgent, GitOpsAgent

---

## Pipeline Flow

### Wave 1: Idea to Specification

```
┌─────────────────────────────────────────────────────────────────┐
│                         WAVE 1 PIPELINE                         │
└─────────────────────────────────────────────────────────────────┘

  Human Input (Idea)
         │
         │ "Build a tool to parse marine engine logs"
         ↓
  ┌──────────────┐
  │ SafetyGuard  │  Validates safety (no equipment control, exploits, etc.)
  └──────────────┘
         │
         │ SafetyCheck(approved=True, warnings=[...])
         ↓
  ┌──────────────┐
  │ PlannerAgent │  Breaks down into tasks
  └──────────────┘
         │
         │ TaskList(tasks=[t1, t2, t3, t4])
         ↓
  ┌──────────────┐
  │ ArchitectAgent│ Designs technical architecture
  └──────────────┘
         │
         │ ProjectSpec(name, tech_stack, structure, ...)
         ↓
  Ready for Implementation
```

### Complete Pipeline (Future)

```
  Idea → SafetyGuard → PlannerAgent → ArchitectAgent → ImplementerAgent
                                                              ↓
  GitOpsAgent ← DocWriterAgent ← TesterAgent ←──────────────┘
       ↓
  Complete Project Repository
```

---

## Integration Points

### 1. Human → SafetyGuard

**Input**: Plain text or structured Idea
**Output**: SafetyCheck
**Purpose**: Ensure idea is safe to proceed

```python
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.models import Idea

# Create idea
idea = Idea(
    description="Parse alarm logs and highlight critical events",
    target_users=["marine engineer"],
    environment="engine room, limited WiFi"
)

# Validate safety
safety = SafetyGuard()
check = safety.execute(idea)

if not check.approved:
    print(f"BLOCKED: {check.warnings}")
    exit(1)

# Safe to proceed
print("✓ Safety validation passed")
```

**Data Transformation**:
- `Idea` (user input) → `SafetyCheck` (approval decision)
- SafetyCheck contains:
  - `approved: bool` - Whether to proceed
  - `warnings: List[str]` - Safety concerns
  - `required_confirmations: List[str]` - User must confirm risky operations
  - `blocked_keywords: List[str]` - Dangerous patterns found
  - `metadata: SafetyCheckMetadata` - Audit trail

**Error Handling**:
- If `approved == False`, pipeline MUST stop
- Display `warnings` to user
- Log decision in `metadata` for audit

---

### 2. SafetyGuard → PlannerAgent

**Input**: Original Idea (from user, after safety approval)
**Output**: TaskList
**Purpose**: Break idea into actionable tasks

```python
from code_factory.agents.planner import PlannerAgent

# Assuming safety check passed
planner = PlannerAgent()
task_list = planner.execute(idea)  # Same idea from above

print(f"Generated {len(task_list.tasks)} tasks:")
for task in task_list.tasks:
    print(f"  [{task.type}] {task.id}: {task.description}")
    if task.dependencies:
        print(f"      Depends on: {', '.join(task.dependencies)}")
```

**Data Transformation**:
- `Idea` (unchanged from input) → `TaskList` (task graph)
- TaskList contains:
  - `tasks: List[Task]` - Ordered list of work items
- Each Task contains:
  - `id: str` - Unique identifier ("t1", "t2", ...)
  - `type: TaskType` - config, code, test, doc, git
  - `description: str` - What this task does
  - `dependencies: List[str]` - Task IDs that must finish first
  - `files_to_create: List[str]` - Expected outputs
  - `status: TaskStatus` - pending, running, success, failed

**Key Insight**: PlannerAgent doesn't need SafetyCheck output - it only needs the original Idea. SafetyGuard is a gate, not a transformer.

**Error Handling**:
- Validate that all `dependencies` reference valid task IDs
- Ensure no circular dependencies
- Check that at least one task exists

---

### 3. PlannerAgent → ArchitectAgent

**Input**: Idea + TaskList metadata
**Output**: ProjectSpec
**Purpose**: Design technical architecture

```python
from code_factory.agents.architect import ArchitectAgent, ArchitectInput

# Using outputs from previous stages
architect = ArchitectAgent()

# Option 1: Pass Idea directly
spec = architect.execute(idea)

# Option 2: Include task metadata (preferred)
arch_input = ArchitectInput(
    idea=idea,
    task_count=len(task_list.tasks)
)
spec = architect.execute(arch_input)

print(f"Project: {spec.name}")
print(f"Stack: {spec.tech_stack}")
print(f"Entry: {spec.entry_point}")
```

**Data Transformation**:
- `Idea` + `task_count` → `ProjectSpec` (technical blueprint)
- ProjectSpec contains:
  - `name: str` - Project identifier
  - `description: str` - One-line summary
  - `tech_stack: Dict[str, str]` - Technology choices
  - `folder_structure: Dict[str, List[str]]` - File organization
  - `dependencies: List[str]` - Package requirements
  - `entry_point: str` - Main file to run
  - `user_profile: str` - Target user (from Idea)
  - `environment: str` - Operating context (from Idea)

**Why TaskList metadata?**: Future versions of ArchitectAgent will use `task_count` to estimate project complexity and adjust architecture accordingly (more tasks = more structured folders).

**Error Handling**:
- Validate that `name` is URL-friendly (lowercase, hyphens only)
- Ensure `tech_stack` has at least `language` key
- Verify `folder_structure` has valid paths
- Check `entry_point` exists in `folder_structure`

---

## Data Models Reference

### Core Models

```python
# Input: Human idea
class Idea(BaseModel):
    description: str                    # Required: what to build
    target_users: List[str] = []        # Who will use it
    environment: Optional[str] = None   # Where it will run
    features: List[str] = []            # Specific capabilities
    constraints: List[str] = []         # Limitations

# Stage 1 Output: Safety validation
class SafetyCheck(BaseModel):
    approved: bool                      # Proceed or block
    warnings: List[str] = []            # Safety concerns
    required_confirmations: List[str] = []
    blocked_keywords: List[str] = []
    metadata: Optional[SafetyCheckMetadata] = None

# Stage 2 Output: Task breakdown
class TaskList(BaseModel):
    tasks: List[Task]

class Task(BaseModel):
    id: str                             # "t1", "t2", ...
    type: TaskType                      # config, code, test, doc, git
    description: str
    dependencies: List[str] = []        # Task IDs
    files_to_create: List[str] = []
    status: TaskStatus = PENDING

# Stage 3 Output: Architecture spec
class ProjectSpec(BaseModel):
    name: str                           # project-name
    description: str                    # One-liner
    tech_stack: Dict[str, str]          # {language: python, ...}
    folder_structure: Dict[str, List[str]]  # {src/: [main.py]}
    dependencies: List[str]             # [typer, rich, ...]
    entry_point: str                    # src/main.py
    user_profile: Optional[str]
    environment: Optional[str]
```

---

## Complete Integration Examples

### Example 1: Basic Pipeline

```python
"""
Complete Wave 1 pipeline: Idea → Safety → Planning → Architecture
"""
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.core.models import Idea

def run_wave1_pipeline(idea: Idea):
    """Execute complete Wave 1 agent pipeline"""

    # Stage 1: Safety validation
    print("=" * 60)
    print("STAGE 1: SAFETY VALIDATION")
    print("=" * 60)

    safety = SafetyGuard()
    safety_check = safety.execute(idea)

    print(f"Approved: {safety_check.approved}")
    if safety_check.warnings:
        print(f"Warnings: {safety_check.warnings}")

    if not safety_check.approved:
        print("\n❌ Idea blocked by SafetyGuard")
        return None

    print("✓ Safety check passed\n")

    # Stage 2: Task planning
    print("=" * 60)
    print("STAGE 2: TASK PLANNING")
    print("=" * 60)

    planner = PlannerAgent()
    task_list = planner.execute(idea)

    print(f"Generated {len(task_list.tasks)} tasks:")
    for task in task_list.tasks:
        deps = f" (deps: {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"  [{task.type.value:6s}] {task.id}: {task.description}{deps}")

    print("\n✓ Task planning complete\n")

    # Stage 3: Architecture design
    print("=" * 60)
    print("STAGE 3: ARCHITECTURE DESIGN")
    print("=" * 60)

    architect = ArchitectAgent()
    arch_input = ArchitectInput(
        idea=idea,
        task_count=len(task_list.tasks)
    )
    spec = architect.execute(arch_input)

    print(f"Project Name: {spec.name}")
    print(f"Description: {spec.description}")
    print(f"\nTech Stack:")
    for key, value in spec.tech_stack.items():
        print(f"  {key:15s}: {value}")
    print(f"\nDependencies: {', '.join(spec.dependencies)}")
    print(f"Entry Point: {spec.entry_point}")

    print("\n✓ Architecture design complete\n")

    # Return final spec for next pipeline stage
    return spec

# Run the pipeline
if __name__ == "__main__":
    idea = Idea(
        description="Parse CSV files and generate summary statistics",
        target_users=["data analyst"],
        environment="desktop, Windows",
        features=["mean, median, mode calculations", "export to JSON"]
    )

    spec = run_wave1_pipeline(idea)

    if spec:
        print("\n" + "=" * 60)
        print("WAVE 1 COMPLETE - Ready for ImplementerAgent")
        print("=" * 60)
```

### Example 2: Marine Log Analyzer (Real-World)

```python
"""
Real-world example: Marine engine alarm log analyzer
"""
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.core.models import Idea

# Define the problem
idea = Idea(
    description="Parse marine diesel engine alarm logs and highlight critical issues",
    target_users=["marine engineer", "chief engineer"],
    environment="ship engine room, noisy, limited WiFi, tablet display",
    features=[
        "Read alarm log files (CSV format)",
        "Filter for critical alarms (high temp, low oil pressure)",
        "Color-coded output by severity",
        "Export filtered results to CSV",
        "Show timestamp ranges"
    ],
    constraints=[
        "Must work offline",
        "Large fonts for readability in bright sunlight",
        "Simple CLI - no complex commands",
        "Minimal dependencies for easy installation"
    ]
)

print("MARINE LOG ANALYZER - Wave 1 Pipeline")
print("=" * 70)

# Stage 1: Safety
safety = SafetyGuard()
check = safety.execute(idea)

print("\n[1/3] Safety Check")
print(f"  Approved: {check.approved}")
if check.warnings:
    for warning in check.warnings:
        print(f"  Warning: {warning}")

if not check.approved:
    print("\n❌ Pipeline halted - safety concerns")
    exit(1)

print("  ✓ Safe to proceed")

# Stage 2: Planning
planner = PlannerAgent()
tasks = planner.execute(idea)

print(f"\n[2/3] Task Planning ({len(tasks.tasks)} tasks)")
for i, task in enumerate(tasks.tasks, 1):
    print(f"  {i}. [{task.type.value:6s}] {task.description}")

# Stage 3: Architecture
architect = ArchitectAgent()
spec = architect.execute(ArchitectInput(
    idea=idea,
    task_count=len(tasks.tasks)
))

print(f"\n[3/3] Architecture Design")
print(f"  Project: {spec.name}")
print(f"  Language: {spec.tech_stack.get('language', 'N/A')}")
print(f"  Framework: {spec.tech_stack.get('cli_framework', 'N/A')}")
print(f"  Dependencies: {len(spec.dependencies)} packages")

print("\n" + "=" * 70)
print("✓ Wave 1 Complete - Specification ready for implementation")
print("=" * 70)

# Display final spec
print("\nFINAL SPECIFICATION:")
print(f"  Name: {spec.name}")
print(f"  Target User: {spec.user_profile}")
print(f"  Environment: {spec.environment}")
print(f"  Entry Point: {spec.entry_point}")
print("\n  Project Structure:")
for folder, files in spec.folder_structure.items():
    print(f"    {folder}")
    for file in files:
        print(f"      └── {file}")
```

### Example 3: Error Handling Pipeline

```python
"""
Demonstrates error handling and recovery in the integration pipeline
"""
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent
from code_factory.core.models import Idea
from pydantic import ValidationError

def safe_pipeline_execution(idea: Idea):
    """
    Execute pipeline with comprehensive error handling
    """
    try:
        # Stage 1: Safety
        print("Stage 1: Safety validation...")
        safety = SafetyGuard()
        check = safety.execute(idea)

        if not check.approved:
            print(f"❌ Safety check failed:")
            for warning in check.warnings:
                print(f"   - {warning}")
            return None

        print("✓ Safety approved")

    except ValidationError as e:
        print(f"❌ Invalid idea format: {e}")
        return None
    except Exception as e:
        print(f"❌ Safety check error: {e}")
        return None

    try:
        # Stage 2: Planning
        print("Stage 2: Task planning...")
        planner = PlannerAgent()
        tasks = planner.execute(idea)

        if not tasks.tasks:
            print("⚠️  Warning: No tasks generated")
            return None

        print(f"✓ Generated {len(tasks.tasks)} tasks")

    except Exception as e:
        print(f"❌ Planning error: {e}")
        # Could return partial spec if needed
        return None

    try:
        # Stage 3: Architecture
        print("Stage 3: Architecture design...")
        architect = ArchitectAgent()
        spec = architect.execute(idea)

        # Validation
        if not spec.name or not spec.entry_point:
            print("⚠️  Warning: Incomplete specification")
            return None

        print(f"✓ Architecture designed: {spec.name}")
        return spec

    except ValidationError as e:
        print(f"❌ Invalid specification: {e}")
        return None
    except Exception as e:
        print(f"❌ Architecture design error: {e}")
        return None

# Test with valid idea
print("Test 1: Valid Idea")
print("-" * 50)
valid_idea = Idea(description="Build a CSV parser")
result = safe_pipeline_execution(valid_idea)
print(f"Result: {'Success' if result else 'Failed'}\n")

# Test with invalid idea (safety violation)
print("Test 2: Safety Violation")
print("-" * 50)
dangerous_idea = Idea(description="Control valve positions remotely")
result = safe_pipeline_execution(dangerous_idea)
print(f"Result: {'Success' if result else 'Failed (expected)'}\n")

# Test with empty description (validation error)
print("Test 3: Validation Error")
print("-" * 50)
try:
    invalid_idea = Idea(description="")  # Will raise ValidationError
except ValidationError as e:
    print(f"Caught validation error: {e.errors()[0]['msg']}")
```

---

## Pipeline Best Practices

### 1. Always Validate Safety First

```python
# ✓ CORRECT: Check safety before any other processing
check = safety_guard.execute(idea)
if not check.approved:
    return  # Stop immediately

# ❌ WRONG: Processing before safety check
tasks = planner.execute(idea)  # Don't do this first!
check = safety_guard.execute(idea)
```

### 2. Preserve Original Idea Through Pipeline

```python
# The Idea object flows through all stages unchanged
# Don't modify it!

# ✓ CORRECT
original_idea = Idea(description="...")
check = safety.execute(original_idea)
tasks = planner.execute(original_idea)  # Same object
spec = architect.execute(original_idea)  # Same object

# ❌ WRONG
original_idea = Idea(description="...")
modified_idea = modify_somehow(original_idea)
tasks = planner.execute(modified_idea)  # Different from input!
```

### 3. Check Each Stage's Output

```python
# Validate outputs before passing to next stage

check = safety.execute(idea)
if not check.approved:  # ✓ Check before continuing
    handle_rejection()

tasks = planner.execute(idea)
if not tasks.tasks:  # ✓ Verify task list not empty
    handle_no_tasks()

spec = architect.execute(idea)
if not spec.name or not spec.entry_point:  # ✓ Validate critical fields
    handle_incomplete_spec()
```

### 4. Log All Stage Transitions

```python
import logging

logger = logging.getLogger(__name__)

def run_pipeline(idea: Idea):
    logger.info(f"Pipeline started for: {idea.description}")

    # Stage 1
    logger.info("Stage 1: Safety validation")
    check = safety.execute(idea)
    logger.info(f"Safety result: approved={check.approved}")

    # Stage 2
    logger.info("Stage 2: Task planning")
    tasks = planner.execute(idea)
    logger.info(f"Generated {len(tasks.tasks)} tasks")

    # Stage 3
    logger.info("Stage 3: Architecture design")
    spec = architect.execute(idea)
    logger.info(f"Architecture complete: {spec.name}")

    return spec
```

### 5. Handle Partial Failures Gracefully

```python
def robust_pipeline(idea: Idea):
    """Pipeline that handles failures and provides useful feedback"""

    results = {
        "safety_check": None,
        "task_list": None,
        "project_spec": None,
        "errors": []
    }

    # Safety
    try:
        results["safety_check"] = safety.execute(idea)
        if not results["safety_check"].approved:
            results["errors"].append("Safety validation failed")
            return results  # Can't continue
    except Exception as e:
        results["errors"].append(f"Safety stage error: {e}")
        return results

    # Planning
    try:
        results["task_list"] = planner.execute(idea)
    except Exception as e:
        results["errors"].append(f"Planning stage error: {e}")
        # Continue anyway - architecture might still work

    # Architecture
    try:
        results["project_spec"] = architect.execute(idea)
    except Exception as e:
        results["errors"].append(f"Architecture stage error: {e}")

    return results
```

---

## Testing Integration

### Integration Test Example

```python
"""
tests/integration/test_wave1_pipeline.py
"""
import pytest
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.core.models import Idea

def test_complete_wave1_pipeline():
    """Test full Wave 1 integration"""

    # Setup
    idea = Idea(
        description="Build a temperature logger CLI",
        target_users=["technician"],
        environment="factory floor"
    )

    # Stage 1: Safety
    safety = SafetyGuard()
    check = safety.execute(idea)
    assert check.approved, "Safe idea should be approved"

    # Stage 2: Planning
    planner = PlannerAgent()
    tasks = planner.execute(idea)
    assert len(tasks.tasks) > 0, "Should generate tasks"
    assert all(t.id for t in tasks.tasks), "All tasks should have IDs"

    # Stage 3: Architecture
    architect = ArchitectAgent()
    spec = architect.execute(ArchitectInput(
        idea=idea,
        task_count=len(tasks.tasks)
    ))
    assert spec.name, "Should have project name"
    assert "language" in spec.tech_stack, "Should specify language"
    assert spec.entry_point, "Should have entry point"

    # Verify data consistency
    assert spec.user_profile == idea.target_users[0]
    assert spec.environment == idea.environment

def test_pipeline_rejects_dangerous_idea():
    """Test that dangerous ideas are blocked early"""

    dangerous_idea = Idea(
        description="Control industrial equipment remotely"
    )

    # Safety should block
    safety = SafetyGuard()
    check = safety.execute(dangerous_idea)
    assert not check.approved, "Dangerous idea should be blocked"
    assert len(check.warnings) > 0, "Should have warnings"

    # Pipeline should stop here - don't continue to planning

def test_pipeline_handles_minimal_idea():
    """Test pipeline with minimal valid input"""

    minimal_idea = Idea(description="Log parser")

    # Should work with just description
    safety = SafetyGuard()
    check = safety.execute(minimal_idea)
    assert check.approved

    planner = PlannerAgent()
    tasks = planner.execute(minimal_idea)
    assert len(tasks.tasks) > 0

    architect = ArchitectAgent()
    spec = architect.execute(minimal_idea)
    assert spec.name == "log-parser"
```

---

## Troubleshooting

### Common Integration Issues

#### Issue 1: TypeError when passing data between agents

**Symptom**: `TypeError: execute() takes 2 positional arguments but 3 were given`

**Cause**: Passing wrong data type to agent

**Solution**: Check agent's expected input type
```python
# PlannerAgent expects Idea
planner.execute(idea)  # ✓ Correct

# ArchitectAgent accepts Idea OR ArchitectInput
architect.execute(idea)  # ✓ Correct
architect.execute(ArchitectInput(idea=idea, task_count=4))  # ✓ Also correct
```

#### Issue 2: ValidationError in pipeline

**Symptom**: `pydantic.ValidationError: 1 validation error for Idea`

**Cause**: Missing required field or invalid data

**Solution**: Ensure Idea has valid `description`
```python
# ❌ Wrong
idea = Idea()  # Missing description

# ✓ Correct
idea = Idea(description="Valid description")
```

#### Issue 3: Pipeline continues after safety rejection

**Symptom**: Dangerous idea gets planned and architected

**Cause**: Not checking `approved` field

**Solution**: Always check and exit
```python
check = safety.execute(idea)
if not check.approved:
    print(f"Blocked: {check.warnings}")
    return  # MUST exit here
```

---

## Performance Metrics

### Typical Pipeline Timing (Wave 1)

| Stage | Agent | Avg Time | Notes |
|-------|-------|----------|-------|
| 1 | SafetyGuard | 10-50ms | Regex + normalization |
| 2 | PlannerAgent | 50-100ms | Template-based |
| 3 | ArchitectAgent | 30-50ms | Template-based |
| **Total** | **Wave 1** | **100-200ms** | **Sub-second** |

Future LLM-based versions:
- PlannerAgent: 1-3 seconds (LLM call)
- ArchitectAgent: 1-2 seconds (LLM call)
- Total: 2-5 seconds

### Memory Usage

- SafetyGuard: < 1 MB
- PlannerAgent: < 1 MB
- ArchitectAgent: < 1 MB
- Pipeline total: < 5 MB (minimal overhead)

---

## Related Documentation

- [Architecture Overview](./architecture.md) - Overall system design
- [Agent Roles](./agent_roles.md) - All agents and their purposes
- [PlannerAgent Documentation](./agents/planner_agent.md) - Task planning details
- [ArchitectAgent Documentation](./agents/architect_agent.md) - Architecture design details
- [Safety Guidelines](./safety.md) - SafetyGuard implementation

---

## Next Steps

After completing Wave 1 integration, you'll have:
- ✅ Safety-validated idea
- ✅ Task breakdown with dependencies
- ✅ Complete technical specification

Ready for **Wave 2**:
- ImplementerAgent: Generate code files from ProjectSpec
- TesterAgent: Create and run tests
- DocWriterAgent: Generate documentation
- GitOpsAgent: Initialize repository and push to GitHub

---

## Changelog

### Version 1.0.0 (2025-01-15)
- Initial Wave 1 integration guide
- SafetyGuard → PlannerAgent → ArchitectAgent pipeline
- Complete examples and error handling
- Integration tests
- Performance benchmarks

### Version 2.0.0 (Planned - Q1 2025)
- Wave 2 integration (Implementer, Tester, DocWriter, GitOps)
- Parallel agent execution
- Streaming progress updates
- Enhanced error recovery
