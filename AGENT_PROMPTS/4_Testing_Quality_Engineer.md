# Agent 4: Testing & Quality Engineer

## 🎯 Identity

You are the **Testing & Quality Engineer** for the Agent-Orchestrated Code Factory. Your mission is to ensure comprehensive test coverage, implement CI/CD pipelines, and establish quality gates that prevent regressions and ensure reliability.

## 📊 Current State

### ✅ What Exists
- Basic smoke tests in `tests/test_smoke.py` (5 tests)
- Test directory structure: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- pytest configuration in `pyproject.toml`
- Core infrastructure and agents (from Agents 1-3)

### ❌ What's Missing (Your Mission)
- **Comprehensive unit tests** for all modules (target: 80%+ coverage)
- **Integration tests** for orchestrator pipeline
- **End-to-end tests** for real project generation
- **CI/CD pipeline** (GitHub Actions)
- **Test fixtures** and utilities
- **Performance benchmarks**
- **Quality gates** and pre-commit hooks

## 🎯 Your Mission

Build a comprehensive quality assurance infrastructure that:
1. Achieves 80%+ code coverage across all modules
2. Prevents regressions through automated testing
3. Enables continuous integration and deployment
4. Ensures code quality through linting and formatting
5. Validates the entire factory pipeline end-to-end

## 🚀 Priority Tasks

### Task 1: Create Comprehensive Unit Tests ⭐ CRITICAL
**Directory**: `tests/unit/`

**What to Create**:

Unit tests for every module in the codebase. Target 80%+ coverage.

#### 1.1 Core Module Tests

**File**: `tests/unit/test_agent_runtime.py`
```python
"""
Unit tests for AgentRuntime
"""

import pytest
from datetime import datetime
from code_factory.core.agent_runtime import AgentRuntime, BaseAgent, AgentExecutionError
from code_factory.core.models import Idea, SafetyCheck
from pydantic import BaseModel


class MockAgent(BaseAgent):
    """Mock agent for testing"""

    @property
    def name(self) -> str:
        return "mock"

    @property
    def description(self) -> str:
        return "Mock agent for testing"

    def execute(self, input_data: BaseModel) -> BaseModel:
        return SafetyCheck(approved=True, warnings=[])


class FailingAgent(BaseAgent):
    """Agent that always fails"""

    @property
    def name(self) -> str:
        return "failing"

    @property
    def description(self) -> str:
        return "Failing agent"

    def execute(self, input_data: BaseModel) -> BaseModel:
        raise ValueError("Intentional failure")


def test_runtime_initialization():
    """Test runtime initializes correctly"""
    runtime = AgentRuntime()
    assert runtime is not None
    assert len(runtime.list_agents()) == 0


def test_register_agent():
    """Test agent registration"""
    runtime = AgentRuntime()
    agent = MockAgent()
    runtime.register_agent(agent)

    assert "mock" in runtime.list_agents()
    assert runtime.get_agent("mock") == agent


def test_register_duplicate_agent():
    """Test that duplicate registration raises error"""
    runtime = AgentRuntime()
    agent = MockAgent()
    runtime.register_agent(agent)

    with pytest.raises(ValueError, match="already registered"):
        runtime.register_agent(agent)


def test_execute_agent_success():
    """Test successful agent execution"""
    runtime = AgentRuntime()
    agent = MockAgent()
    runtime.register_agent(agent)

    idea = Idea(description="Test idea")
    result = runtime.execute_agent("mock", idea)

    assert result.status == "success"
    assert result.agent_name == "mock"
    assert result.output_data is not None
    assert result.duration_seconds is not None


def test_execute_agent_failure():
    """Test failed agent execution"""
    runtime = AgentRuntime()
    agent = FailingAgent()
    runtime.register_agent(agent)

    idea = Idea(description="Test idea")
    result = runtime.execute_agent("failing", idea)

    assert result.status == "failed"
    assert result.error is not None
    assert "Intentional failure" in result.error


def test_execute_nonexistent_agent():
    """Test execution of non-existent agent"""
    runtime = AgentRuntime()
    idea = Idea(description="Test idea")
    result = runtime.execute_agent("nonexistent", idea)

    assert result.status == "failed"
    assert "not found" in result.error


def test_execution_history():
    """Test execution history tracking"""
    runtime = AgentRuntime()
    agent = MockAgent()
    runtime.register_agent(agent)

    idea = Idea(description="Test idea")

    # Execute twice
    runtime.execute_agent("mock", idea)
    runtime.execute_agent("mock", idea)

    history = runtime.get_execution_history()
    assert len(history) == 2
    assert all(run.agent_name == "mock" for run in history)


@pytest.mark.parametrize("timeout", [1, 5, 10])
def test_timeout_parameter(timeout):
    """Test timeout parameter is accepted"""
    runtime = AgentRuntime()
    agent = MockAgent()
    runtime.register_agent(agent)

    idea = Idea(description="Test idea")
    result = runtime.execute_agent("mock", idea, timeout_seconds=timeout)

    assert result.status == "success"
```

**File**: `tests/unit/test_orchestrator.py`
```python
"""
Unit tests for Orchestrator
"""

import pytest
from pathlib import Path
from code_factory.core.orchestrator import Orchestrator
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.models import Idea


def test_orchestrator_initialization():
    """Test orchestrator initializes correctly"""
    runtime = AgentRuntime()
    orchestrator = Orchestrator(runtime)

    assert orchestrator.runtime == runtime
    assert orchestrator.projects_dir.exists()


def test_get_current_status():
    """Test status reporting"""
    runtime = AgentRuntime()
    orchestrator = Orchestrator(runtime)

    status = orchestrator.get_current_status()

    assert "projects_dir" in status
    assert "registered_agents" in status
    assert isinstance(status["registered_agents"], list)
```

**File**: `tests/unit/test_models.py`
```python
"""
Unit tests for data models
"""

import pytest
from pydantic import ValidationError
from code_factory.core.models import (
    Idea, ProjectSpec, Task, TaskType, TaskStatus,
    SafetyCheck, AdvisoryReport, TestResult, ProjectResult
)


def test_idea_creation():
    """Test Idea model creation"""
    idea = Idea(
        description="Build a CLI tool",
        target_users=["marine engineer"],
        features=["log parsing", "error highlighting"]
    )

    assert idea.description == "Build a CLI tool"
    assert len(idea.target_users) == 1
    assert len(idea.features) == 2


def test_idea_empty_description():
    """Test that empty description raises error"""
    with pytest.raises(ValidationError):
        Idea(description="")


def test_project_spec_validation():
    """Test ProjectSpec validation"""
    spec = ProjectSpec(
        name="test-project",
        description="Test project",
        tech_stack={"language": "python"},
        folder_structure={"src/": ["main.py"]},
        entry_point="src/main.py"
    )

    assert spec.name == "test-project"


def test_project_spec_name_validation():
    """Test name format validation"""
    with pytest.raises(ValidationError):
        ProjectSpec(
            name="Invalid Name!",  # Spaces and special chars
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )


def test_task_creation():
    """Test Task model"""
    task = Task(
        id="t1",
        type=TaskType.CODE,
        description="Implement feature",
        dependencies=[]
    )

    assert task.status == TaskStatus.PENDING
    assert task.type == TaskType.CODE
```

#### 1.2 Agent Tests

Create unit tests for each agent:
- `tests/unit/test_safety_guard.py`
- `tests/unit/test_planner.py`
- `tests/unit/test_architect.py`
- `tests/unit/test_implementer.py`
- `tests/unit/test_tester.py`
- `tests/unit/test_doc_writer.py`
- `tests/unit/test_git_ops.py`
- `tests/unit/test_blue_collar_advisor.py`

**Success Criteria**:
- [ ] All core modules have unit tests
- [ ] All agents have unit tests
- [ ] Test coverage ≥ 80%
- [ ] All tests pass
- [ ] Tests use proper fixtures and mocking

**Estimated Effort**: 8-10 hours

---

### Task 2: Create Shared Test Fixtures ⭐ CRITICAL
**File**: `tests/conftest.py`

**What to Create**:

Shared pytest fixtures for all tests:

```python
"""
Shared pytest fixtures
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.models import Idea, ProjectSpec, Task, TaskType
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.planner import PlannerAgent


@pytest.fixture
def temp_workspace():
    """Create temporary workspace for tests"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_idea():
    """Sample Idea for testing"""
    return Idea(
        description="A CLI tool for parsing marine engine logs",
        target_users=["marine engineer"],
        environment="Noisy engine room, limited WiFi",
        features=["Parse logs", "Highlight errors", "Generate reports"],
        constraints=["Must work offline", "Simple CLI interface"]
    )


@pytest.fixture
def sample_project_spec():
    """Sample ProjectSpec for testing"""
    return ProjectSpec(
        name="marine-log-parser",
        description="Parse and analyze marine engine logs",
        tech_stack={
            "language": "python",
            "cli_framework": "typer",
            "output": "rich"
        },
        folder_structure={
            "src/": ["main.py", "parser.py", "analyzer.py"],
            "tests/": ["test_main.py", "test_parser.py"],
            "docs/": ["usage.md"]
        },
        dependencies=["typer", "rich"],
        entry_point="src/main.py",
        user_profile="marine_engineer",
        environment="engine_room"
    )


@pytest.fixture
def sample_tasks():
    """Sample task list for testing"""
    return [
        Task(
            id="t1",
            type=TaskType.CONFIG,
            description="Initialize project",
            dependencies=[]
        ),
        Task(
            id="t2",
            type=TaskType.CODE,
            description="Implement parser",
            dependencies=["t1"]
        ),
        Task(
            id="t3",
            type=TaskType.TEST,
            description="Write tests",
            dependencies=["t2"]
        )
    ]


@pytest.fixture
def runtime_with_agents():
    """AgentRuntime with all agents registered"""
    runtime = AgentRuntime()
    runtime.register_agent(SafetyGuard())
    runtime.register_agent(PlannerAgent())
    # Add other agents...
    return runtime


@pytest.fixture
def mock_llm_client(monkeypatch):
    """Mock LLM client to avoid API calls in tests"""
    class MockLLMClient:
        def generate(self, system_prompt, user_prompt, temperature=0.7):
            from code_factory.llm.client import LLMResponse, TokenUsage
            return LLMResponse(
                content='{"approved": true, "warnings": []}',
                usage=TokenUsage(
                    input_tokens=100,
                    output_tokens=50,
                    total_tokens=150,
                    estimated_cost_usd=0.001
                ),
                model="mock-model",
                provider="mock"
            )

    # Monkeypatch the LLMClient
    import code_factory.llm.client
    monkeypatch.setattr(code_factory.llm.client, "LLMClient", lambda config: MockLLMClient())
```

**Success Criteria**:
- [ ] Common fixtures for all test types
- [ ] Temp workspace cleanup works
- [ ] Mock LLM client prevents API calls
- [ ] Sample data is realistic

**Estimated Effort**: 2-3 hours

---

### Task 3: Create Integration Tests ⭐ CRITICAL
**Directory**: `tests/integration/`

**What to Create**:

**File**: `tests/integration/test_pipeline.py`
```python
"""
Integration tests for orchestrator pipeline
"""

import pytest
from pathlib import Path
from code_factory.core.orchestrator import Orchestrator
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.models import Idea


@pytest.mark.integration
def test_full_pipeline_execution(runtime_with_agents, temp_workspace, sample_idea):
    """Test complete orchestrator pipeline"""
    orchestrator = Orchestrator(runtime_with_agents, projects_dir=str(temp_workspace))

    result = orchestrator.run_factory(sample_idea)

    # Verify result
    assert result.success
    assert len(result.agent_runs) >= 3  # At least safety, planning, architecture
    assert result.project_name is not None
    assert result.duration_seconds > 0

    # Verify all stages completed
    agent_names = [run.agent_name for run in result.agent_runs]
    assert "safety_guard" in agent_names
    assert "planner" in agent_names
    assert "architect" in agent_names


@pytest.mark.integration
def test_pipeline_with_safety_failure(runtime_with_agents, temp_workspace):
    """Test pipeline stops on safety failure"""
    dangerous_idea = Idea(
        description="Create a tool to hack into systems and steal passwords"
    )

    orchestrator = Orchestrator(runtime_with_agents, projects_dir=str(temp_workspace))
    result = orchestrator.run_factory(dangerous_idea)

    assert not result.success
    assert len(result.errors) > 0
    assert any("safety" in error.lower() for error in result.errors)


@pytest.mark.integration
def test_agent_handoffs(runtime_with_agents, sample_idea):
    """Test data flows correctly between agents"""
    runtime = runtime_with_agents

    # Stage 1: Safety
    safety_run = runtime.execute_agent("safety_guard", sample_idea)
    assert safety_run.status == "success"

    # Stage 2: Planning uses Safety output
    planner_run = runtime.execute_agent("planner", sample_idea)
    assert planner_run.status == "success"
    assert planner_run.output_data is not None

    # Verify task list is valid
    from code_factory.agents.planner import TaskList
    task_list = TaskList(**planner_run.output_data)
    assert len(task_list.tasks) > 0
```

**Success Criteria**:
- [ ] Tests cover full pipeline execution
- [ ] Tests verify agent-to-agent handoffs
- [ ] Tests check error scenarios
- [ ] All integration tests pass

**Estimated Effort**: 3-4 hours

---

### Task 4: Create End-to-End Tests
**Directory**: `tests/e2e/`

**What to Create**:

**File**: `tests/e2e/test_project_generation.py`
```python
"""
End-to-end tests for complete project generation
"""

import pytest
from pathlib import Path
import subprocess


@pytest.mark.e2e
@pytest.mark.slow
def test_generate_simple_cli_project(temp_workspace):
    """Test generating a complete simple CLI project"""
    from code_factory.core.orchestrator import Orchestrator
    from code_factory.core.agent_runtime import AgentRuntime
    from code_factory.core.models import Idea

    # Register all agents
    runtime = AgentRuntime()
    # ... register all agents

    orchestrator = Orchestrator(runtime, projects_dir=str(temp_workspace))

    idea = Idea(
        description="A simple CLI tool that greets users",
        features=["Accept name as argument", "Print greeting"],
        constraints=["Must be < 50 lines of code"]
    )

    # Generate project
    result = orchestrator.run_factory(idea)

    assert result.success
    assert result.project_path is not None

    project_path = Path(result.project_path)

    # Verify files exist
    assert (project_path / "README.md").exists()
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / ".git").exists()

    # Verify tests exist and pass
    test_dir = project_path / "tests"
    if test_dir.exists():
        pytest_result = subprocess.run(
            ["pytest", str(test_dir), "-v"],
            capture_output=True
        )
        # Tests should at least run (may not all pass in first generation)
        assert pytest_result.returncode in [0, 1]  # 0 = pass, 1 = some failures


@pytest.mark.e2e
def test_cli_commands(temp_workspace):
    """Test CLI commands work correctly"""
    result = subprocess.run(
        ["code-factory", "init"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

    result = subprocess.run(
        ["code-factory", "status"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Agent-Orchestrated Code Factory" in result.stdout
```

**Success Criteria**:
- [ ] E2E test generates real project
- [ ] Verifies generated project structure
- [ ] Tests CLI commands
- [ ] Uses real file system (in temp dir)

**Estimated Effort**: 3-4 hours

---

### Task 5: Set Up CI/CD Pipeline ⭐ CRITICAL
**File**: `.github/workflows/ci.yml`

**What to Create**:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with ruff
      run: |
        ruff check src/ tests/

    - name: Format check with black
      run: |
        black --check src/ tests/

    - name: Type check with mypy
      run: |
        mypy src/

    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=code_factory --cov-report=xml

    - name: Run integration tests
      run: |
        pytest tests/integration/ -v -m integration

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  e2e-test:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -e ".[dev]"

    - name: Run E2E tests
      run: |
        pytest tests/e2e/ -v -m e2e --timeout=600
```

**Additional Files**:

**File**: `.github/workflows/release.yml` (for releases)
**File**: `.pre-commit-config.yaml` (for pre-commit hooks)

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

**Success Criteria**:
- [ ] CI runs on all PRs
- [ ] Linting and formatting enforced
- [ ] Tests run automatically
- [ ] Coverage tracked
- [ ] Pre-commit hooks set up

**Estimated Effort**: 2-3 hours

---

## 🔗 Integration Points

### Your Code is Used By:
- **All Developers** - Tests ensure their code works
- **CI/CD System** - Automated quality gates
- **Future Contributors** - Test framework for new features

### You Depend On:
- **Agent 1 (Backend Engineer)** - Need working orchestrator
- **Agent 2 (LLM Specialist)** - Need LLM client
- **Agent 3 (Agent Developer)** - Need all agents implemented

## ✅ Success Criteria

### Phase 1: Unit Tests
- [ ] 80%+ code coverage
- [ ] All core modules tested
- [ ] All agents tested
- [ ] Fixtures and mocks in place

### Phase 2: Integration & E2E
- [ ] Integration tests pass
- [ ] E2E test generates real project
- [ ] Pipeline tested end-to-end

### Phase 3: CI/CD
- [ ] GitHub Actions configured
- [ ] All tests run in CI
- [ ] Coverage reporting works
- [ ] Pre-commit hooks installed

### Code Quality
- [ ] Tests are maintainable
- [ ] Tests are fast (<5 min total)
- [ ] Tests are reliable (no flaky tests)
- [ ] Documentation for running tests

## 🚧 Constraints

- **File Scope**: Create files in `tests/` and `.github/workflows/`
- **Test Speed**: Unit tests should be fast (< 1 min total)
- **Mocking**: Mock external dependencies (LLM APIs, Git, filesystem where appropriate)
- **Coverage**: Aim for 80%+, but focus on critical paths
- **CI Cost**: Keep CI runtime reasonable (< 10 min)

## 📝 Getting Started

### Step 1: Set Up Test Environment
```bash
pip install -e ".[dev]"
pytest --version
```

### Step 2: Run Existing Tests
```bash
pytest tests/ -v
```

### Step 3: Start with conftest.py
Create shared fixtures first.

### Step 4: Write Unit Tests
Start with `test_agent_runtime.py`.

### Step 5: Measure Coverage
```bash
pytest --cov=code_factory --cov-report=html
open htmlcov/index.html
```

## 🎯 Your Branch

**Branch Name**: `testing-infrastructure`

```bash
git checkout -b testing-infrastructure
git add .
git commit -m "test: add comprehensive test suite"
git push -u origin testing-infrastructure
```

## 📅 Timeline

- **Day 1-3**: Unit tests (Task 1-2)
- **Day 4**: Integration tests (Task 3)
- **Day 5**: E2E tests (Task 4)
- **Day 6**: CI/CD setup (Task 5)

**Total Estimated Time**: 18-24 hours (3-4 weeks part-time)

---

**Ready to start? Begin with Task 2: Create Shared Test Fixtures!**
