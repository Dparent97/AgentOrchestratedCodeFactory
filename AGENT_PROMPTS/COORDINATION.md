# Agent Coordination & Integration Points

**Project:** Agent-Orchestrated Code Factory
**Iteration:** 2 - Agent Implementation
**Purpose:** Define how agents work together and integrate their outputs

---

## 🔗 Integration Architecture

```
User Idea (text)
      ↓
 SafetyGuard ✅ (validation)
      ↓
 PlannerAgent (tasks)
      ↓
 ArchitectAgent (project spec)
      ↓
 ImplementerAgent (code)
      ↓
 TesterAgent (tests)
      ↓
 DocWriterAgent (docs)
      ↓
 GitOpsAgent (repo + commit)
      ↓
 BlueCollarAdvisor ✅ (review)
      ↓
Complete Project Repository
```

---

## 📊 Wave 1 Integration Points

### 1. SafetyGuard → PlannerAgent

**Status:** ✅ SafetyGuard Complete (Phase 5)

**Interface:**
```python
# INPUT
from code_factory.core.models import Idea

idea = Idea(
    description="Build a marine equipment log analyzer",
    features=["Parse CSV logs", "Filter by date", "Generate summaries"]
)

# SAFETY CHECK
from code_factory.agents.safety_guard import SafetyGuard
guard = SafetyGuard()
safety_result = guard.execute(idea)

if not safety_result.approved:
    raise SecurityError(f"Blocked: {safety_result.blocked_keywords}")

# OUTPUT → PlannerAgent
# safety_result.approved = True
# safety_result.warnings = []
# idea is safe to proceed
```

**Location:** `src/code_factory/agents/safety_guard.py`
**Tests:** `tests/unit/test_safety_guard.py`
**Documentation:** `docs/safety.md`

---

### 2. PlannerAgent → ArchitectAgent

**Status:** 🔄 Wave 1 - In Progress

**Owner:** Agent Foundation Developer

**Interface:**
```python
# INPUT
from code_factory.core.models import Idea

idea = Idea(
    description="Build a marine equipment log analyzer",
    features=["Parse CSV logs", "Filter by date", "Generate summaries"]
)

# PLANNER EXECUTION
from code_factory.agents.planner import PlannerAgent
planner = PlannerAgent()
plan_result = planner.execute(idea)

# OUTPUT
from code_factory.core.models import Task

tasks: List[Task] = plan_result.tasks
# Example tasks:
# [
#   Task(id="1", type="code", description="Create CSV parser", ...),
#   Task(id="2", type="code", description="Add date filtering", ...),
#   Task(id="3", type="test", description="Test parser", ...),
# ]
```

**Required Implementation:**
- **File:** `src/code_factory/agents/planner.py`
- **Input Model:** `Idea` (already exists in `core/models.py`)
- **Output Model:** `PlanResult` with `List[Task]` (need to create)
- **Method:** `execute(idea: Idea) -> PlanResult`

**Success Criteria:**
- [ ] Breaks idea into 5-15 actionable tasks
- [ ] Creates dependency graph (task.dependencies)
- [ ] Categorizes tasks (code, test, doc, config)
- [ ] Returns valid PlanResult model
- [ ] Has 80%+ test coverage

**Tests Required:**
- Simple idea → task breakdown
- Complex idea → proper decomposition
- Edge cases (vague idea, missing features)
- Dependency graph correctness

**Output → ArchitectAgent:**
```python
# The Architect needs both Idea and Tasks
architect_input = {
    "idea": idea,
    "tasks": tasks
}
```

---

### 3. ArchitectAgent Design

**Status:** 🔄 Wave 1 - In Progress

**Owner:** Agent Foundation Developer

**Interface:**
```python
# INPUT (from PlannerAgent)
from code_factory.core.models import Idea, ProjectSpec
from code_factory.agents.architect import ArchitectAgent

architect = ArchitectAgent()
spec_result = architect.execute(idea, tasks)

# OUTPUT
project_spec: ProjectSpec = spec_result.spec
# ProjectSpec contains:
# - name: str (project name)
# - tech_stack: Dict[str, str] (language, framework, etc.)
# - folder_structure: Dict[str, List[str]]
# - dependencies: List[str]
# - entry_point: str
# - environment: str (for blue-collar context)
```

**Required Implementation:**
- **File:** `src/code_factory/agents/architect.py`
- **Input Model:** `Idea` + `List[Task]` (both exist)
- **Output Model:** `ArchitectResult` with `ProjectSpec` (ProjectSpec exists, need Result wrapper)
- **Method:** `execute(idea: Idea, tasks: List[Task]) -> ArchitectResult`

**Success Criteria:**
- [ ] Selects appropriate tech stack for idea
- [ ] Creates logical folder structure
- [ ] Identifies all dependencies needed
- [ ] Considers blue-collar context (CLI, offline, simple)
- [ ] Returns valid ProjectSpec

**Blue-Collar Considerations:**
- Prefer CLI over web UI
- Prefer Python/shell scripts over complex frameworks
- Prefer simple file formats (CSV, JSON) over databases
- Consider offline operation
- Keep dependencies minimal

**Tests Required:**
- Marine log analyzer → CLI tool design
- HVAC calculator → Appropriate tech choices
- Different complexity levels
- Blue-collar preferences enforced

**Output → ImplementerAgent (Wave 2):**
```python
# Wave 2 will use this
implementer_input = {
    "spec": project_spec,
    "tasks": tasks
}
```

---

## 🧪 Wave 1 Testing Infrastructure

### QA Engineer Responsibilities

**Owner:** QA Engineer (Wave 1)

#### 1. Agent Test Harness

**Purpose:** Standardized way to test all agents

**Implementation:** `tests/harness/agent_test_harness.py`

```python
class AgentTestHarness:
    """Test harness for verifying agent behavior"""

    def test_agent_interface(self, agent: BaseAgent):
        """Verify agent implements required interface"""
        assert hasattr(agent, 'execute')
        assert hasattr(agent, 'name')
        assert hasattr(agent, 'description')

    def test_agent_execution(self, agent: BaseAgent, input_data, expected_output_type):
        """Test agent execution with sample data"""
        result = agent.execute(input_data)
        assert isinstance(result, expected_output_type)

    def test_agent_error_handling(self, agent: BaseAgent, invalid_input):
        """Test agent handles errors gracefully"""
        # Should not crash, should return error result
```

**Status:** 🔄 In Progress
**ETA:** End of Wave 1

#### 2. Integration Test: Idea → Tasks → Spec

**Purpose:** Verify Wave 1 agents work together

**Implementation:** `tests/integration/test_wave1_pipeline.py`

```python
def test_idea_to_spec_pipeline():
    """Test full Wave 1 pipeline"""

    # Step 1: Safety check
    idea = Idea(description="Build a CSV log parser")
    guard = SafetyGuard()
    safety = guard.execute(idea)
    assert safety.approved

    # Step 2: Planning
    planner = PlannerAgent()
    plan = planner.execute(idea)
    assert len(plan.tasks) > 0

    # Step 3: Architecture
    architect = ArchitectAgent()
    spec = architect.execute(idea, plan.tasks)
    assert spec.spec.name is not None
    assert spec.spec.tech_stack is not None

    # Step 4: Verify integration
    assert spec.spec.entry_point is not None
    print(f"✅ Wave 1 Pipeline Complete: {spec.spec.name}")
```

**Status:** ❌ Not Started
**ETA:** End of Wave 1
**Blocker:** Needs PlannerAgent + ArchitectAgent implemented

#### 3. Test Data Fixtures

**Purpose:** Shared test data for all agents

**Implementation:** `tests/conftest.py` (add to existing file)

```python
@pytest.fixture
def sample_idea_simple():
    """Simple idea for testing"""
    return Idea(
        description="Build a CSV parser",
        features=["Read CSV", "Filter rows"]
    )

@pytest.fixture
def sample_idea_marine():
    """Marine engineering use case"""
    return Idea(
        description="Marine equipment log analyzer",
        features=[
            "Parse alarm logs",
            "Filter by severity",
            "Generate daily summaries"
        ]
    )

@pytest.fixture
def sample_idea_hvac():
    """HVAC technician use case"""
    return Idea(
        description="HVAC load calculator",
        features=[
            "Input room dimensions",
            "Calculate BTU requirements",
            "Generate equipment specs"
        ]
    )
```

**Status:** 🔄 In Progress
**ETA:** Early Wave 1

---

## 📚 Wave 1 Documentation Framework

### Technical Writer Responsibilities

**Owner:** Technical Writer (Wave 1)

#### 1. Agent API Documentation Template

**Purpose:** Consistent documentation for all agents

**Location:** `docs/agents/TEMPLATE.md`

**Structure:**
```markdown
# [AgentName] - [Purpose]

## Overview
[What this agent does]

## Input/Output

### Input
[Pydantic model specification]

### Output
[Pydantic model specification]

## Usage Example
[Code example]

## Implementation Notes
[Design decisions, algorithms used]

## Testing
[How to test this agent]

## Blue-Collar Considerations
[Specific design choices for field workers]
```

**Status:** 🔄 In Progress
**ETA:** Early Wave 1

#### 2. Agent Documentation (Per Agent)

**Locations:**
- `docs/agents/planner_agent.md` - PlannerAgent API
- `docs/agents/architect_agent.md` - ArchitectAgent API
- `docs/agents/implementer_agent.md` - ImplementerAgent API (Wave 2)
- `docs/agents/tester_agent.md` - TesterAgent API (Wave 2)
- `docs/agents/doc_writer_agent.md` - DocWriterAgent API (Wave 2)
- `docs/agents/git_ops_agent.md` - GitOpsAgent API (Wave 2)
- `docs/agents/blue_collar_advisor.md` - BlueCollarAdvisor API (Wave 3)

**Status:** ❌ Not Started
**Dependencies:** Wait for agent implementations

#### 3. Integration Guide

**Purpose:** Explain how agents work together

**Location:** `docs/agent_integration.md`

**Contents:**
- Pipeline flow diagram
- Data models passed between agents
- Error handling across agents
- Example end-to-end workflows

**Status:** ❌ Not Started
**ETA:** End of Wave 1

---

## 🚨 Known Dependencies & Blockers

### Wave 1 Dependencies

| Agent/Component | Depends On | Status | Blocker |
|----------------|------------|--------|---------|
| PlannerAgent | SafetyGuard (idea validation) | ✅ Ready | None |
| ArchitectAgent | PlannerAgent (tasks) | ⚠️ Waiting | PlannerAgent must complete first |
| QA Test Harness | Agent interface spec | ✅ Ready | None |
| Integration Tests | PlannerAgent + ArchitectAgent | ⚠️ Waiting | Both agents needed |
| Agent Docs | Agent implementations | ⚠️ Waiting | Agents must exist to document |

### Wave 2 Dependencies (Preview)

| Agent/Component | Depends On | Status |
|----------------|------------|--------|
| ImplementerAgent | ProjectSpec from Architect | ⚠️ Wave 1 |
| TesterAgent | Generated code from Implementer | ⚠️ Wave 2 |
| DocWriterAgent | ProjectSpec + Code | ⚠️ Wave 2 |

---

## 📁 File Ownership (Wave 1)

### Agent Foundation Developer Owns:
- `src/code_factory/agents/planner.py` - Full implementation
- `src/code_factory/agents/architect.py` - Full implementation
- `src/code_factory/core/models.py` - Add PlanResult, ArchitectResult models
- `tests/unit/test_planner.py` - Unit tests
- `tests/unit/test_architect.py` - Unit tests

### QA Engineer Owns:
- `tests/harness/agent_test_harness.py` - Test harness
- `tests/integration/test_wave1_pipeline.py` - Integration tests
- `tests/conftest.py` - Test fixtures (additions)
- Quality review of all PRs

### Technical Writer Owns:
- `docs/agents/TEMPLATE.md` - Documentation template
- `docs/agents/planner_agent.md` - PlannerAgent docs
- `docs/agents/architect_agent.md` - ArchitectAgent docs
- `docs/agent_integration.md` - Integration guide
- Updates to `docs/architecture.md` with agent details

### Shared/No Conflicts:
- `AGENT_PROMPTS/daily_logs/` - All agents post here
- `AGENT_PROMPTS/questions.md` - All agents read/write
- `AGENT_PROMPTS/issues/` - All agents can create issues

---

## 🤝 API Contracts (Wave 1)

### PlannerAgent API Contract

```python
class PlannerAgent(BaseAgent):
    """Breaks ideas into actionable tasks"""

    @property
    def name(self) -> str:
        return "planner"

    @property
    def description(self) -> str:
        return "Breaks project ideas into actionable tasks with dependencies"

    def execute(self, idea: Idea) -> PlanResult:
        """
        Convert idea into structured task breakdown

        Args:
            idea: The project idea to plan

        Returns:
            PlanResult with list of tasks and dependency graph

        Raises:
            ValueError: If idea is invalid or too vague
        """
        pass  # Implementation by Agent Foundation Developer
```

**PlanResult Model:**
```python
class PlanResult(BaseModel):
    """Result from PlannerAgent execution"""
    tasks: List[Task]
    dependency_graph: Dict[str, List[str]]  # task_id -> [dependent_task_ids]
    estimated_complexity: str  # "simple", "moderate", "complex"
    warnings: List[str] = []
```

### ArchitectAgent API Contract

```python
class ArchitectAgent(BaseAgent):
    """Designs project architecture and tech stack"""

    @property
    def name(self) -> str:
        return "architect"

    @property
    def description(self) -> str:
        return "Designs project structure and selects appropriate technologies"

    def execute(self, idea: Idea, tasks: List[Task]) -> ArchitectResult:
        """
        Design project architecture based on idea and planned tasks

        Args:
            idea: The original project idea
            tasks: List of tasks from PlannerAgent

        Returns:
            ArchitectResult with ProjectSpec

        Raises:
            ValueError: If tasks are invalid or incomplete
        """
        pass  # Implementation by Agent Foundation Developer
```

**ArchitectResult Model:**
```python
class ArchitectResult(BaseModel):
    """Result from ArchitectAgent execution"""
    spec: ProjectSpec
    rationale: Dict[str, str]  # Decision -> Reasoning
    blue_collar_score: float  # 0-10, how field-practical is this?
    warnings: List[str] = []
```

---

## 🔍 Integration Testing Strategy

### Level 1: Unit Tests (Per Agent)
**Responsibility:** Agent Foundation Developer + QA Engineer

Each agent has comprehensive unit tests:
- Valid inputs → Expected outputs
- Invalid inputs → Proper error handling
- Edge cases (empty data, huge data, malformed data)
- Model validation (Pydantic models)

### Level 2: Integration Tests (Agent Pairs)
**Responsibility:** QA Engineer

Test agent-to-agent communication:
- PlannerAgent output → ArchitectAgent input (valid?)
- Data models serialize/deserialize correctly
- Dependency data flows properly

### Level 3: Pipeline Tests (Full Wave)
**Responsibility:** QA Engineer

Test complete Wave 1 pipeline:
- Idea → Safety → Plan → Architect → Spec
- Multiple idea types (simple, complex, domain-specific)
- Error propagation (if Planner fails, what happens?)
- Performance (how long does pipeline take?)

### Level 4: Real-World Tests (Example Use Cases)
**Responsibility:** QA Engineer + Technical Writer

Test with actual blue-collar use cases:
- Marine log analyzer
- HVAC load calculator
- Plant maintenance scheduler
- Equipment checklist generator

---

## 📞 Communication Protocols

### Daily Sync (Asynchronous via Logs)

**Format:** `daily_logs/YYYY-MM-DD.md`

```markdown
## Agent Foundation Developer - 2025-11-18

### Completed
- Implemented PlannerAgent.execute() basic logic
- Created task decomposition algorithm
- Added unit tests (15 tests, 12 passing)

### In Progress
- Debugging dependency graph generation
- Need to handle edge case: circular dependencies

### Blockers
None

### Questions
@QA-Engineer: What level of task granularity do you want for testing?
- Should I break "Create CSV parser" into sub-tasks?
- Or keep it as a single task?

### Next Steps
- Fix circular dependency detection
- Complete ArchitectAgent scaffolding
- Reach 80% test coverage by EOD tomorrow
```

### Questions Protocol

**Format:** `questions.md`

```markdown
## [Agent Name] - [Date] - [Question ID]

**Question:** [Clear, specific question]

**Context:** [Why you're asking, what you've tried]

**Blocking:** [Yes/No - is this blocking your progress?]

**Target Respondent:** [@mention specific agent or "anyone"]

---

## [Respondent Name] - [Date]

**Answer:** [Clear answer with rationale]

**Reference:** [Links to code, docs, or examples]

**Follow-up:** [Any additional context]
```

### Issue Tracking

**Format:** `issues/ISSUE_NNN.md`

```markdown
# [Issue Title]

**Created:** 2025-11-18
**Creator:** Agent Foundation Developer
**Status:** Open
**Priority:** High
**Blocking:** Yes

## Problem
[Clear description of the issue]

## Impact
[Who/what is affected]

## Proposed Solution
[Ideas for fixing]

## Who Can Help
[@mention relevant agents]

## Updates
- 2025-11-18: Issue created
- [Future updates here]
```

---

## ✅ Wave 1 Completion Checklist

### Agent Foundation Developer
- [ ] PlannerAgent.execute() implemented
- [ ] PlanResult model created
- [ ] ArchitectAgent.execute() implemented
- [ ] ArchitectResult model created
- [ ] Unit tests >80% coverage for both agents
- [ ] All tests passing
- [ ] Code follows style guide (ruff, black, mypy)
- [ ] Docstrings complete
- [ ] PR created and approved

### QA Engineer
- [ ] Agent test harness implemented
- [ ] Test fixtures created (simple, marine, HVAC ideas)
- [ ] Unit test review complete (all agents)
- [ ] Integration test implemented (Idea → Tasks → Spec)
- [ ] Integration test passing
- [ ] All PRs reviewed and approved
- [ ] Test coverage report generated
- [ ] Quality gate verification complete

### Technical Writer
- [ ] Documentation template created
- [ ] PlannerAgent documentation complete
- [ ] ArchitectAgent documentation complete
- [ ] Integration guide started
- [ ] Usage examples written
- [ ] Architecture docs updated
- [ ] All docs reviewed and published

### Integration Verification
- [ ] Wave 1 pipeline works end-to-end
- [ ] Demo: `code-factory plan "Build CSV parser"` works
- [ ] All integration points verified
- [ ] No blockers for Wave 2
- [ ] All branches merged to main
- [ ] Ready for Wave 2 launch

---

## 🎯 Wave 2 Preview (Coming Next)

**Goal:** Code generation + supporting agents

**New Integration Points:**
- ArchitectAgent → ImplementerAgent (spec → code)
- ImplementerAgent → TesterAgent (code → tests)
- ImplementerAgent → DocWriterAgent (code → docs)

**Will be detailed in COORDINATION.md after Wave 1 completion**

---

*Last Updated: November 17, 2025*
*Next Update: End of Wave 1 (November 22, 2025)*
