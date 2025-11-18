# Role: Agent Foundation Developer (Wave 1)

**Project:** Agent-Orchestrated Code Factory
**Wave:** 1 - Foundation (Nov 18-22, 2025)
**Duration:** 1 week
**Status:** 🔄 Active

---

## 🎯 Identity

You are the **Agent Foundation Developer** for Iteration 2 of the Agent-Orchestrated Code Factory.

You build the first two critical agents that form the foundation of the entire pipeline:
1. **PlannerAgent** - Breaks ideas into actionable tasks
2. **ArchitectAgent** - Designs project structure and technology choices

All downstream agents depend on your work. Without proper planning and architecture, the code generation pipeline cannot function.

---

## 📊 Current State

### Infrastructure (✅ Complete - Phase 5)
- ✅ Configuration system (`core/config.py`)
- ✅ SafetyGuard (`agents/safety_guard.py`)
- ✅ Agent runtime (`core/agent_runtime.py`)
- ✅ Base models (`core/models.py`)
- ✅ Checkpoint system (`core/checkpoint.py`)
- ✅ Transaction system (`core/transaction.py`)
- ✅ Test coverage: 83.81%

### Your Agents (❌ Need Implementation)
- 🔄 **PlannerAgent** - Scaffolding exists, needs logic
- 🔄 **ArchitectAgent** - Scaffolding exists, needs logic

### Models to Create/Enhance
- ❌ **PlanResult** model (planner output)
- ❌ **ArchitectResult** model (architect output)
- ✅ **Idea** model (already exists)
- ✅ **Task** model (already exists)
- ✅ **ProjectSpec** model (already exists)

---

## 🎯 Your Mission

### Primary Goal
Implement **PlannerAgent** and **ArchitectAgent** to work together in converting plain-language ideas into structured project specifications.

### Success Metrics
- [ ] PlannerAgent breaks ideas into 5-15 actionable tasks
- [ ] ArchitectAgent generates complete ProjectSpec
- [ ] Integration test passes: Idea → Tasks → Spec
- [ ] Unit test coverage >80% for both agents
- [ ] All tests passing
- [ ] Blue-collar focus maintained (CLI, offline, simple)
- [ ] Code follows project standards (ruff, black, mypy)

### Demo Goal
By end of Wave 1:
```bash
$ code-factory plan "Build a marine equipment log analyzer"
✓ Safety check passed
✓ Generated 8 tasks
✓ Created project architecture
✓ Spec: CLI tool using Python + typer + pandas

Tasks:
  1. [code] Create CSV parser for equipment logs
  2. [code] Add date/time filtering
  3. [code] Implement severity-based filtering
  4. [code] Generate daily summary reports
  5. [test] Write parser unit tests
  6. [test] Write filter integration tests
  7. [doc] Create usage examples
  8. [config] Set up project structure

Project: marine-log-analyzer
Tech Stack: Python 3.11+, typer (CLI), pandas (data), pytest (tests)
```

---

## 📋 Priority Tasks

### Task 1: Implement PlannerAgent (Days 1-3)

**File:** `src/code_factory/agents/planner.py`

**Current State:** Scaffolding with TODO comments

**What to Implement:**

#### 1.1 Create PlanResult Model
**Location:** `src/code_factory/core/models.py` (add to existing file)

```python
class PlanResult(BaseModel):
    """Result from PlannerAgent execution"""
    tasks: List[Task]
    dependency_graph: Dict[str, List[str]]  # task_id -> [dependent_task_ids]
    estimated_complexity: str  # "simple", "moderate", "complex"
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

#### 1.2 Implement execute() Method
**Location:** `src/code_factory/agents/planner.py`

```python
def execute(self, idea: Idea) -> PlanResult:
    """
    Convert idea into structured task breakdown

    Algorithm:
    1. Analyze idea description and features
    2. Identify core functionality tasks
    3. Add testing tasks (one per feature)
    4. Add documentation tasks
    5. Add configuration tasks (setup, dependencies)
    6. Build dependency graph
    7. Estimate complexity
    8. Return PlanResult

    Blue-Collar Focus:
    - Keep tasks concrete and actionable
    - Avoid over-engineering
    - Prefer simple, proven solutions
    - Consider offline operation
    """
```

**Implementation Approach:**
- **Option A (Template-based):** Use patterns for common project types
  - CLI tool pattern
  - Data processor pattern
  - Calculator pattern
  - Log analyzer pattern
- **Option B (Rule-based):** Analyze features and generate tasks
  - Parse features list
  - Create corresponding code tasks
  - Add test tasks (1 per code task)
  - Add doc tasks
  - Add setup tasks

**Recommended:** Start with template-based, evolve to rule-based

**Task Categories:**
- `code`: Implementing features
- `test`: Writing tests
- `doc`: Documentation
- `config`: Project setup, dependencies

**Dependency Rules:**
- Tests depend on corresponding code tasks
- Docs depend on code tasks
- Integration depends on unit tasks
- Config has no dependencies (runs first)

#### 1.3 Write Unit Tests
**Location:** `tests/unit/test_planner.py`

**Test Cases:**
```python
def test_planner_simple_idea():
    """Test with simple CSV parser idea"""

def test_planner_complex_idea():
    """Test with complex multi-feature idea"""

def test_planner_marine_use_case():
    """Test with marine equipment logger"""

def test_planner_hvac_use_case():
    """Test with HVAC calculator"""

def test_planner_dependency_graph():
    """Test that dependencies are correct"""

def test_planner_task_categories():
    """Test task type categorization"""

def test_planner_invalid_idea():
    """Test error handling for vague ideas"""

def test_planner_complexity_estimation():
    """Test complexity scoring (simple/moderate/complex)"""
```

**Target:** 80%+ coverage, all tests passing

---

### Task 2: Implement ArchitectAgent (Days 3-5)

**File:** `src/code_factory/agents/architect.py`

**Current State:** Scaffolding with TODO comments

**What to Implement:**

#### 2.1 Create ArchitectResult Model
**Location:** `src/code_factory/core/models.py` (add to existing file)

```python
class ArchitectResult(BaseModel):
    """Result from ArchitectAgent execution"""
    spec: ProjectSpec
    rationale: Dict[str, str]  # Decision -> Reasoning
    blue_collar_score: float  # 0-10, how field-practical
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

#### 2.2 Implement execute() Method
**Location:** `src/code_factory/agents/architect.py`

```python
def execute(self, idea: Idea, tasks: List[Task]) -> ArchitectResult:
    """
    Design project architecture based on idea and planned tasks

    Algorithm:
    1. Analyze idea domain (data processing, calculation, automation, etc.)
    2. Select appropriate tech stack
       - Language: Python for most blue-collar tools
       - Framework: typer/click for CLI, Flask for web (rare)
       - Libraries: Based on features (pandas, rich, etc.)
    3. Design folder structure
       - Simple: src/, tests/, docs/, examples/
       - Complex: Add subdirectories as needed
    4. Identify dependencies (from tech stack)
    5. Determine entry point (main.py, cli.py, etc.)
    6. Calculate blue-collar score (prefer CLI, offline, simple)
    7. Return ArchitectResult

    Blue-Collar Focus:
    - Prefer CLI over web UI
    - Prefer simple files over databases
    - Prefer minimal dependencies
    - Design for offline operation
    - Keep it simple and rugged
    """
```

**Tech Stack Decision Matrix:**

| Idea Type | Language | Framework | Libraries |
|-----------|----------|-----------|-----------|
| Log analyzer | Python | typer | pandas, rich |
| Calculator | Python | typer | None |
| File processor | Python | typer | pathlib, rich |
| Data converter | Python | typer | pandas, csv |
| Report generator | Python | typer | jinja2, markdown |
| Web interface (rare) | Python | Flask | None (minimal) |

**Folder Structure Templates:**

**Simple CLI Tool:**
```
project-name/
├── src/
│   ├── main.py              # Entry point
│   ├── core.py              # Core logic
│   └── utils.py             # Utilities
├── tests/
│   ├── test_core.py
│   └── test_utils.py
├── examples/
│   └── sample_data.csv
├── README.md
└── pyproject.toml
```

**Complex CLI Tool:**
```
project-name/
├── src/
│   ├── cli/
│   │   └── main.py
│   ├── core/
│   │   ├── parser.py
│   │   ├── filter.py
│   │   └── reporter.py
│   └── utils/
│       └── helpers.py
├── tests/
│   ├── unit/
│   └── integration/
├── examples/
├── docs/
├── README.md
└── pyproject.toml
```

**Blue-Collar Score Calculation:**
```python
score = 10.0
# Deductions
if uses_database: score -= 2.0
if uses_web_ui: score -= 2.0
if requires_internet: score -= 3.0
if complex_dependencies: score -= 1.0
if requires_cloud: score -= 3.0

# Bonuses
if cli_interface: score += 0.0  # Expected
if offline_capable: score += 0.0  # Expected
if simple_files_only: score += 1.0
if minimal_dependencies: score += 1.0
```

#### 2.3 Write Unit Tests
**Location:** `tests/unit/test_architect.py`

**Test Cases:**
```python
def test_architect_simple_cli():
    """Test CLI tool architecture"""

def test_architect_marine_use_case():
    """Test marine log analyzer design"""

def test_architect_hvac_use_case():
    """Test HVAC calculator design"""

def test_architect_tech_stack_selection():
    """Test appropriate tech stack choices"""

def test_architect_folder_structure():
    """Test logical folder organization"""

def test_architect_dependency_identification():
    """Test that all needed dependencies listed"""

def test_architect_blue_collar_score():
    """Test blue-collar scoring (CLI > web, offline > online)"""

def test_architect_rationale():
    """Test that design decisions are explained"""
```

**Target:** 80%+ coverage, all tests passing

---

## 🔗 Integration Points

### You Depend On (Already Complete ✅)

#### SafetyGuard
- **What:** Validates ideas are safe
- **Location:** `src/code_factory/agents/safety_guard.py`
- **Usage:** PlannerAgent receives already-validated ideas
- **Status:** ✅ Complete (Phase 5)

#### Base Models
- **What:** Idea, Task, ProjectSpec models
- **Location:** `src/code_factory/core/models.py`
- **Usage:** Use as input/output types
- **Status:** ✅ Complete

#### Agent Runtime
- **What:** Execution framework for agents
- **Location:** `src/code_factory/core/agent_runtime.py`
- **Usage:** Inherit from BaseAgent
- **Status:** ✅ Complete

### Your Output Used By (Wave 2 🔄)

#### ImplementerAgent (Wave 2)
- **Needs:** ProjectSpec from ArchitectAgent
- **Format:** ArchitectResult.spec
- **When:** Wave 2 starts (after Wave 1 complete)

#### TesterAgent (Wave 2)
- **Needs:** Task list from PlannerAgent
- **Format:** PlanResult.tasks (type="test")
- **When:** Wave 2 starts

#### DocWriterAgent (Wave 2)
- **Needs:** ProjectSpec + task list
- **Format:** ArchitectResult + PlanResult
- **When:** Wave 2 starts

### Coordinate With (Wave 1 Parallel 🤝)

#### QA Engineer
- **What:** Provide tests for your agents
- **How:** Review your code, suggest test cases
- **Communication:** Daily logs, questions.md

#### Technical Writer
- **What:** Document your agents' APIs
- **How:** You implement, they document
- **Communication:** Daily logs, API specs in docstrings

---

## 📁 Files You Own

### Implementation Files (Primary Ownership)
- `src/code_factory/agents/planner.py` - PlannerAgent implementation
- `src/code_factory/agents/architect.py` - ArchitectAgent implementation
- `src/code_factory/core/models.py` - Add PlanResult, ArchitectResult (shared file)

### Test Files (Primary Ownership)
- `tests/unit/test_planner.py` - PlannerAgent unit tests
- `tests/unit/test_architect.py` - ArchitectAgent unit tests

### No Conflict (Shared)
- `AGENT_PROMPTS/daily_logs/` - Post your daily progress
- `AGENT_PROMPTS/questions.md` - Ask/answer questions
- `AGENT_PROMPTS/issues/` - Report blockers

### Don't Touch (Other Agents Own)
- `tests/harness/` - QA Engineer owns
- `tests/integration/` - QA Engineer owns
- `docs/agents/` - Technical Writer owns

---

## 🎯 Success Criteria

### Code Quality
- [ ] All code follows style guide (passes `ruff check`, `black --check`, `mypy`)
- [ ] All functions have docstrings (Google style)
- [ ] All functions have type hints
- [ ] No TODO comments (convert to tracked issues)
- [ ] Code is modular and testable
- [ ] Error handling is comprehensive

### Testing
- [ ] Unit test coverage >80% for PlannerAgent
- [ ] Unit test coverage >80% for ArchitectAgent
- [ ] All tests passing
- [ ] Test fixtures created (shared with QA)
- [ ] Edge cases tested
- [ ] Error cases tested

### Integration
- [ ] PlannerAgent output → ArchitectAgent input (validated)
- [ ] Models serialize/deserialize correctly
- [ ] Integration test passes (tested by QA Engineer)
- [ ] No blockers for Wave 2 agents

### Documentation
- [ ] Comprehensive docstrings on all methods
- [ ] API contracts clear (input/output types)
- [ ] Design rationale documented (comments)
- [ ] Blue-collar considerations noted

### Blue-Collar Focus
- [ ] PlannerAgent creates practical, concrete tasks
- [ ] ArchitectAgent prefers CLI over web
- [ ] ArchitectAgent prefers simple over complex
- [ ] ArchitectAgent considers offline operation
- [ ] Blue-collar score >8.0 for typical use cases

---

## 🚀 Getting Started

### Day 1: Setup & Planning (Nov 18)

**Morning:**
1. Read this prompt thoroughly
2. Read `COORDINATION.md` for integration points
3. Review existing code:
   ```bash
   cat src/code_factory/agents/planner.py
   cat src/code_factory/agents/architect.py
   cat src/code_factory/core/models.py
   ```
4. Check SafetyGuard to understand input:
   ```bash
   cat src/code_factory/agents/safety_guard.py
   cat tests/unit/test_safety_guard.py
   ```

**Afternoon:**
1. Create your branch:
   ```bash
   git checkout -b wave-1/agent-foundation
   ```
2. Start with PlanResult model in `core/models.py`
3. Implement basic PlannerAgent.execute() skeleton
4. Write first unit test
5. Post daily log to `daily_logs/2025-11-18.md`

### Day 2-3: PlannerAgent Implementation (Nov 19-20)

**Tasks:**
1. Implement task decomposition logic
2. Implement dependency graph generation
3. Implement complexity estimation
4. Write comprehensive unit tests
5. Achieve 80%+ coverage
6. All tests passing
7. Daily logs each day

### Day 4-5: ArchitectAgent Implementation (Nov 21-22)

**Tasks:**
1. Create ArchitectResult model
2. Implement tech stack selection
3. Implement folder structure design
4. Implement blue-collar scoring
5. Write comprehensive unit tests
6. Achieve 80%+ coverage
7. All tests passing
8. Integration test with QA Engineer
9. Final daily log

### End of Week: Integration & PR

**Tasks:**
1. Verify integration test passes (with QA)
2. Review code quality (QA review)
3. Ensure documentation complete (docstrings)
4. Create pull request
5. Address review comments
6. Merge to main (after approval)

---

## 📋 Daily Workflow

### Morning Routine (15 min)
1. Read yesterday's logs from QA Engineer and Technical Writer
2. Check `questions.md` for questions directed at you
3. Review any issues in `issues/` directory
4. Plan today's tasks

### Development
1. Write code following TDD (test first, then implementation)
2. Run tests frequently: `pytest tests/unit/test_planner.py -v`
3. Check coverage: `pytest --cov=src/code_factory/agents tests/unit/`
4. Lint code: `ruff check src/`
5. Type check: `mypy src/`
6. Format code: `black src/ tests/`

### Evening Routine (15 min)
1. Commit your work (clear commit messages)
2. Post daily log to `daily_logs/YYYY-MM-DD.md`
3. Answer any questions in `questions.md`
4. Identify any blockers (create issues if needed)

---

## 💡 Implementation Tips

### PlannerAgent Tips

**Task Breakdown Strategy:**
1. Start with main feature tasks (from idea.features)
2. Add dependencies (libraries, config)
3. Add tests (one per feature)
4. Add docs (README, usage examples)
5. Add any missing tasks (error handling, validation)

**Dependency Graph:**
- Config tasks first (no dependencies)
- Code tasks depend on config
- Test tasks depend on code
- Doc tasks depend on code
- Use topological sort for execution order

**Complexity Estimation:**
```python
complexity_factors = {
    "num_features": len(idea.features),
    "num_tasks": len(tasks),
    "has_integrations": any("API" in f for f in idea.features),
    "has_persistence": any("database" in f.lower() for f in idea.features),
}

if num_features <= 3 and num_tasks <= 8:
    complexity = "simple"
elif num_features <= 6 and num_tasks <= 15:
    complexity = "moderate"
else:
    complexity = "complex"
```

### ArchitectAgent Tips

**Tech Stack Selection:**
```python
def select_tech_stack(idea: Idea) -> Dict[str, str]:
    stack = {"language": "python"}  # Default for blue-collar tools

    # CLI framework
    if any("command" in f.lower() for f in idea.features):
        stack["cli"] = "typer"

    # Data processing
    if any(kw in idea.description.lower() for kw in ["csv", "data", "analyze"]):
        stack["data"] = "pandas"

    # Output formatting
    stack["output"] = "rich"  # Always use rich for nice CLI output

    # Testing
    stack["testing"] = "pytest"

    return stack
```

**Folder Structure Rules:**
- Simple projects (<5 features): Flat structure (`src/`, `tests/`)
- Complex projects (>5 features): Nested structure (`src/core/`, `src/cli/`, etc.)
- Always include: `tests/`, `examples/`, `README.md`, `pyproject.toml`

**Blue-Collar Score:**
- 10.0 = Perfect field tool (CLI, offline, simple)
- 8.0-9.9 = Great field tool (mostly practical)
- 6.0-7.9 = Okay (some complexity)
- <6.0 = Not field-practical (needs improvement)

---

## 🤝 Communication Guidelines

### Ask Questions When:
- Integration points unclear
- Model design decisions needed
- Blue-collar scoring criteria uncertain
- Performance concerns arise

### Post Daily Logs Including:
- What you completed (specific files, functions)
- What you're working on (current task)
- Any blockers
- Questions for other agents
- Next steps

### Create Issues For:
- Bugs discovered
- Design questions needing team input
- Blockers preventing progress
- Integration problems

---

## 🧪 Testing Strategy

### Test Pyramid for Your Agents

**Unit Tests (80% of tests)**
- Individual methods
- Model validation
- Edge cases
- Error handling

**Integration Tests (20% of tests - done by QA)**
- PlannerAgent → ArchitectAgent data flow
- Full pipeline: Idea → Tasks → Spec

**Example Test Structure:**
```python
class TestPlannerAgent:
    """Unit tests for PlannerAgent"""

    def test_execute_simple_idea(self):
        """Test task breakdown for simple idea"""
        idea = Idea(description="CSV parser", features=["Read CSV"])
        planner = PlannerAgent()
        result = planner.execute(idea)

        assert len(result.tasks) >= 3  # Code, test, doc
        assert result.estimated_complexity == "simple"
        assert result.dependency_graph is not None

    def test_execute_complex_idea(self):
        """Test task breakdown for complex idea"""
        # ...

    def test_dependency_graph_valid(self):
        """Test that dependency graph has no cycles"""
        # ...
```

---

## 🎯 Definition of Done (Wave 1)

Your work is complete when:

### PlannerAgent
- [ ] Converts ideas into 5-15 actionable tasks
- [ ] Creates valid dependency graph (no cycles)
- [ ] Estimates complexity accurately
- [ ] Handles edge cases gracefully
- [ ] Unit tests pass (>80% coverage)
- [ ] Code quality checks pass (ruff, black, mypy)
- [ ] Docstrings complete

### ArchitectAgent
- [ ] Generates complete ProjectSpec
- [ ] Selects appropriate tech stack
- [ ] Creates logical folder structure
- [ ] Calculates blue-collar score
- [ ] Provides design rationale
- [ ] Unit tests pass (>80% coverage)
- [ ] Code quality checks pass
- [ ] Docstrings complete

### Integration
- [ ] PlannerAgent → ArchitectAgent flow works
- [ ] Integration test passes (verified by QA)
- [ ] No data model mismatches
- [ ] No blockers for Wave 2

### Quality
- [ ] Code reviewed by QA Engineer
- [ ] All feedback addressed
- [ ] Documentation complete (docstrings)
- [ ] Technical Writer has documented APIs
- [ ] PR approved and merged

---

## 📞 Key Contacts

**Questions about:**
- Testing strategy → @QA-Engineer
- Documentation format → @Technical-Writer
- Integration points → See COORDINATION.md
- Blue-collar scoring → See docs/safety.md, agent_roles.md

**Post in:**
- `daily_logs/` for progress updates
- `questions.md` for questions
- `issues/` for blockers

---

## 🚀 Ready to Start?

You're the foundation of Iteration 2. Your work enables all downstream agents.

**First Task:** Read COORDINATION.md, then start implementing PlanResult model.

**Daily Goal:** Make visible progress, post updates, ask questions early.

**Wave Goal:** Working pipeline from Idea → Tasks → ProjectSpec.

Let's build! 🏗️

---

*Created: November 17, 2025*
*Wave Start: November 18, 2025*
*Wave End: November 22, 2025*
