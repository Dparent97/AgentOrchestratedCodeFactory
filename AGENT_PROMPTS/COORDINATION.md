# Agent Coordination & Integration Points

**Project**: Agent-Orchestrated Code Factory
**Last Updated**: 2025-11-17

---

## Overview

This document defines how the 5 agents work together, their dependencies, and integration APIs.

---

## Team Structure & Dependencies

```
┌─────────────────────────────────────────────┐
│         Agent-Orchestrated Code Factory     │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Agent 1    │ │   Agent 2    │ │   Agent 3    │
│   Backend    │→│   Agents     │→│     CLI      │
│Infrastructure│ │Implementation│ │  Interface   │
└──────────────┘ └──────────────┘ └──────────────┘
        │           │           │
        └───────────┼───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐         ┌──────────────┐
│   Agent 4    │         │   Agent 5    │
│   QA/Tests   │         │     Docs     │
└──────────────┘         └──────────────┘
```

---

## Integration Points

### Agent 1 → Agent 2
**What**: Core infrastructure APIs for agent implementation

**Provided by Agent 1**:
```python
# Base class for all agents
from code_factory.core.agent_runtime import BaseAgent, AgentRuntime

# Data models
from code_factory.core.models import (
    Idea, ProjectSpec, Task, TaskGraph,
    AgentRun, ProjectResult
)

# File utilities
from code_factory.core.file_utils import (
    validate_project_path,
    create_project_structure,
    write_code_files
)

# Orchestrator
from code_factory.core.orchestrator import Orchestrator
```

**Status**: 🔄 In Progress (Agent 1 working on this)
**Location**: `src/code_factory/core/`
**ETA**: 2025-11-17 (today)

---

### Agent 2 → Agent 3
**What**: Fully implemented agents for CLI to invoke

**Provided by Agent 2**:
```python
# All 8 agents fully implemented:
from code_factory.agents import (
    SafetyGuard,
    PlannerAgent,
    ArchitectAgent,
    BlueCollarAdvisor,
    ImplementerAgent,
    TesterAgent,
    DocWriterAgent,
    GitOpsAgent
)

# Each agent ready to use via AgentRuntime
runtime = AgentRuntime()
runtime.register_agent(SafetyGuard())
runtime.register_agent(PlannerAgent())
# etc.
```

**Status**: ⏸️ Blocked - Waiting for Agent 1
**Location**: `src/code_factory/agents/`
**ETA**: TBD (after Agent 1 completes)

---

### Agent 1 + Agent 2 → Agent 3
**What**: Complete orchestration system for CLI commands

**Provided by Agents 1 & 2**:
```python
# CLI will use this pattern:
from code_factory.core.orchestrator import Orchestrator
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.models import Idea
from code_factory.agents import all_agents

@app.command()
def create(description: str):
    # Initialize runtime
    runtime = AgentRuntime()

    # Register all agents (Agent 2's work)
    for agent in all_agents():
        runtime.register_agent(agent)

    # Create orchestrator (Agent 1's work)
    orchestrator = Orchestrator(runtime)

    # Execute factory
    idea = Idea(description=description)
    result = orchestrator.run_factory(idea)

    # Display results
    console.print(result)
```

**Status**: ⏸️ Blocked - Waiting for Agents 1 & 2
**Location**: `src/code_factory/cli/main.py`
**ETA**: TBD

---

### All → Agent 4 (QA)
**What**: All code must be testable and have proper interfaces

**Requirements for Agent 4**:
- All modules must have docstrings
- All functions must have type hints
- All public APIs must be documented
- Test fixtures available in `tests/conftest.py`

**Shared Test Fixtures** (Agent 4 will create):
```python
# tests/conftest.py
import pytest
from code_factory.core.models import Idea, ProjectSpec

@pytest.fixture
def sample_idea():
    return Idea(
        description="A simple CSV analyzer",
        target_users=["marine engineer"],
        environment="offline, limited screen"
    )

@pytest.fixture
def sample_project_spec():
    return ProjectSpec(
        name="csv-analyzer",
        description="Analyze CSV files",
        tech_stack={"language": "python"},
        folder_structure={"src/": ["main.py"]},
        entry_point="src/main.py"
    )

@pytest.fixture
def mock_agent_runtime():
    # Mock runtime for testing
    pass
```

**Status**: ⏸️ Blocked - Waiting for implementations
**Location**: `tests/`
**ETA**: TBD

---

### All → Agent 5 (Docs)
**What**: All features must be documented before merge

**Documentation Requirements**:
- Update docs before merging to main
- API reference for all public functions
- Usage examples for CLI commands
- Update CHANGELOG.md

**Agent 5 will maintain**:
```
docs/
├── architecture.md      # System design (already exists)
├── api_reference.md     # API docs (Agent 5 creates)
├── user_guide.md        # User guide (Agent 5 creates)
├── developer_guide.md   # Contributing guide (Agent 5 creates)
└── examples/            # Example projects (Agent 5 creates)
```

**Status**: ⏸️ Blocked - Waiting for working features
**Location**: `docs/`
**ETA**: TBD

---

## Current Phase: Phase 1 - Backend Infrastructure

### Active Work
- **Agent 1** (Backend Engineer): Implementing core orchestration
  - Task 1.1: Orchestrator.run_factory() implementation
  - Task 1.2: File system utilities
  - Task 1.3: Logging configuration
  - Task 1.4: Error recovery

### Blocked Work
- **Agent 2**: Waiting for AgentRuntime and Orchestrator APIs
- **Agent 3**: Waiting for complete orchestration logic
- **Agent 4**: Waiting for implementations to test
- **Agent 5**: Waiting for features to document

---

## Phase Gates

### Phase 1: Foundation Complete
**Criteria**:
- [ ] Agent 1: Orchestrator.run_factory() works end-to-end
- [ ] Agent 1: File utilities created and tested
- [ ] Agent 1: Error handling implemented
- [ ] Agent 1: Unit tests pass (80%+ coverage)
- [ ] Agent 1: Code committed and pushed

**Demo**:
```bash
# This should execute without errors (even with placeholder agents):
code-factory create "A simple test project"
```

### Phase 2: Agents Implemented
**Criteria**:
- [ ] Agent 2: All 8 agents fully implemented
- [ ] Agent 2: Agents generate real code (not placeholders)
- [ ] Agent 2: Unit tests for each agent
- [ ] Agent 4: Integration tests pass

**Demo**:
```bash
# This should create a real, working project:
code-factory create "CSV analyzer for marine engineers"
cd ../MarineCSVAnalyzer
python src/main.py --help
```

### Phase 3: Complete System
**Criteria**:
- [ ] Agent 3: All CLI commands implemented
- [ ] Agent 4: E2E tests pass
- [ ] Agent 5: Documentation complete
- [ ] All agents: Code review done

**Demo**:
```bash
# Full workflow:
code-factory create "Log analyzer for HVAC systems"
code-factory list
code-factory show hvac-log-analyzer
# Project is complete, tested, documented, and ready to use
```

---

## Communication Protocols

### Daily Progress Logs
**Location**: `AGENT_PROMPTS/daily_logs/YYYY-MM-DD.md`

**Format**:
```markdown
## [Agent Name] - [Date]

### Completed Today
- Specific accomplishments with file references

### In Progress
- Current tasks with % completion

### Blockers
- What's blocking progress, who can unblock

### Next Steps
- What will be done next session
```

### Questions & Answers
**Location**: `AGENT_PROMPTS/questions.md`

**Format**:
```markdown
## [Agent Name] - [Date] - [OPEN/RESOLVED]
**Question**: [Clear, specific question]
**Context**: [Why this matters, what depends on it]
**Blocking**: [Yes/No - is work blocked?]

---
**Answer** (by [Other Agent]):
[Clear answer with examples or references]
```

### Issues & Decisions
**Location**: `AGENT_PROMPTS/issues/[issue-number].md`

For significant technical decisions or problems that need discussion.

---

## File Ownership

### Agent 1 Owns:
- `src/code_factory/core/orchestrator.py`
- `src/code_factory/core/agent_runtime.py`
- `src/code_factory/core/models.py`
- `src/code_factory/core/file_utils.py` (will create)
- `src/code_factory/core/logging_config.py` (will create)
- `tests/unit/test_orchestrator.py` (will create)
- `tests/unit/test_agent_runtime.py` (will create)

### Agent 2 Owns:
- `src/code_factory/agents/*.py` (all 8 agents)
- `tests/unit/test_agents/*.py`

### Agent 3 Owns:
- `src/code_factory/cli/main.py`
- `src/code_factory/cli/commands/*.py` (new)
- `tests/unit/test_cli.py`

### Agent 4 Owns:
- `tests/integration/`
- `tests/e2e/`
- `tests/conftest.py`
- `.github/workflows/` (CI/CD)

### Agent 5 Owns:
- `docs/` (all documentation)
- `README.md`
- `CHANGELOG.md`
- `examples/`

**Rule**: Agents should NOT edit files they don't own without coordination!

---

## Version Control Strategy

### Branch Structure
```
main (protected)
└── claude/backend-infrastructure-setup-019sQjcXLBdXcRx854o6WQo4 (Agent 1)
```

### Merge Requirements
- [ ] All tests must pass
- [ ] Code review by coordinator
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Follows code style guidelines

### Commit Message Format
```
<type>: <short description>

<detailed description if needed>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

---

## Status Dashboard

| Agent | Status | Current Task | Blocked By | ETA |
|-------|--------|-------------|------------|-----|
| Agent 1 (Backend) | 🔄 Active | Orchestrator implementation | None | Today |
| Agent 2 (Agents) | ⏸️ Waiting | Agent implementations | Agent 1 | TBD |
| Agent 3 (CLI) | ⏸️ Waiting | CLI commands | Agent 1+2 | TBD |
| Agent 4 (QA) | ⏸️ Waiting | Tests | Agent 1+2 | TBD |
| Agent 5 (Docs) | ⏸️ Waiting | Documentation | Agent 1+2+3 | TBD |

**Last Updated**: 2025-11-17 22:00 UTC

---

## Next Coordination Check

**When**: After Agent 1 completes Phase 1
**What**: Review progress, unblock Agent 2, adjust timelines
**Who**: All agents (async via logs)

---

*This is a living document. Update as the project progresses.*
