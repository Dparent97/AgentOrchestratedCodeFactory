"""
Pytest configuration and shared fixtures

Provides reusable test fixtures for all test modules.
These fixtures create standard test data and agent instances.
"""

import pytest

from code_factory.agents.architect import ArchitectAgent
from code_factory.agents.blue_collar_advisor import BlueCollarAdvisor
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.agents.git_ops import GitOpsAgent
from code_factory.agents.implementer import ImplementerAgent
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.tester import TesterAgent
from code_factory.core.models import Idea, ProjectSpec, Task, TaskType


# ============================================================================
# Idea Fixtures - Test input data
# ============================================================================


@pytest.fixture
def idea_simple_csv():
    """Simple CSV parser idea - minimal complexity"""
    return Idea(
        description="CSV parser for reading equipment data",
        features=["Read CSV files", "Parse columns", "Handle errors"],
    )


@pytest.fixture
def idea_marine_log():
    """Marine equipment log analyzer - medium complexity"""
    return Idea(
        description="Marine equipment log analyzer for ship maintenance tracking",
        features=[
            "Parse engine log files",
            "Filter by date range",
            "Generate maintenance reports",
            "Track equipment hours",
        ],
        constraints=["Must work offline", "Simple text output", "No cloud services"],
        target_users=["marine_engineer"],
        environment="noisy engine room, limited WiFi",
    )


@pytest.fixture
def idea_workshop_tool():
    """Workshop inventory tool - high complexity"""
    return Idea(
        description="Workshop inventory and tool tracking system",
        features=[
            "Barcode scanning",
            "Inventory management",
            "Tool checkout tracking",
            "Maintenance scheduling",
            "Parts ordering",
            "Usage analytics",
        ],
        constraints=[
            "Must work in dusty environment",
            "Touch-screen friendly",
            "No internet required",
        ],
        target_users=["mechanic", "workshop_manager"],
        environment="noisy workshop, dusty, poor lighting",
    )


@pytest.fixture
def idea_calculator():
    """Simple calculator - minimal test case"""
    return Idea(description="Basic calculator for marine calculations")


@pytest.fixture
def idea_with_constraints():
    """Idea with various constraints"""
    return Idea(
        description="Build a maintenance tracker",
        features=["offline mode", "voice input"],
        constraints=["no cloud", "must be fast", "simple UI"],
        target_users=["mechanic"],
    )


@pytest.fixture
def idea_complex():
    """Complex idea with many features"""
    return Idea(
        description="Build comprehensive maintenance management system",
        features=[
            "equipment tracking",
            "maintenance scheduling",
            "parts inventory",
            "work order management",
            "reporting dashboard",
        ],
        constraints=["offline-first", "mobile-friendly", "low bandwidth"],
        target_users=["maintenance_supervisor", "technician"],
        environment="industrial facility, variable connectivity",
    )


# ============================================================================
# Agent Fixtures - Reusable agent instances
# ============================================================================


@pytest.fixture
def planner_agent():
    """PlannerAgent instance"""
    return PlannerAgent()


@pytest.fixture
def architect_agent():
    """ArchitectAgent instance"""
    return ArchitectAgent()


@pytest.fixture
def implementer_agent():
    """ImplementerAgent instance"""
    return ImplementerAgent()


@pytest.fixture
def tester_agent():
    """TesterAgent instance"""
    return TesterAgent()


@pytest.fixture
def doc_writer_agent():
    """DocWriterAgent instance"""
    return DocWriterAgent()


@pytest.fixture
def blue_collar_advisor():
    """BlueCollarAdvisor instance"""
    return BlueCollarAdvisor()


@pytest.fixture
def git_ops_agent():
    """GitOpsAgent instance"""
    return GitOpsAgent()


@pytest.fixture
def safety_guard():
    """SafetyGuard instance"""
    return SafetyGuard()


# ============================================================================
# ProjectSpec Fixtures - Test architecture data
# ============================================================================


@pytest.fixture
def spec_simple():
    """Simple project spec for testing"""
    return ProjectSpec(
        name="test-tool",
        description="Test tool for unit tests",
        tech_stack={"language": "python", "cli": "typer"},
        folder_structure={"src/": ["main.py", "utils.py"], "tests/": ["test_main.py"]},
        entry_point="src/main.py",
    )


@pytest.fixture
def spec_marine_log():
    """Project spec for marine log analyzer"""
    return ProjectSpec(
        name="marine-log-analyzer",
        description="Marine equipment log analyzer",
        tech_stack={
            "language": "python",
            "cli": "typer",
            "parsing": "csv",
            "output": "rich",
        },
        folder_structure={
            "src/": ["main.py", "parser.py", "analyzer.py", "reporter.py"],
            "tests/": ["test_parser.py", "test_analyzer.py"],
            "docs/": ["README.md", "usage.md"],
        },
        dependencies=["typer", "rich", "python-dateutil"],
        entry_point="src/main.py",
        user_profile="marine_engineer",
        environment="noisy engine room, limited WiFi",
    )


# ============================================================================
# Task Fixtures - Test planning data
# ============================================================================


@pytest.fixture
def task_config():
    """Sample CONFIG task"""
    return Task(
        id="t1",
        type=TaskType.CONFIG,
        description="Initialize project structure",
        dependencies=[],
        files_to_create=["README.md", "pyproject.toml"],
    )


@pytest.fixture
def task_code():
    """Sample CODE task"""
    return Task(
        id="t2",
        type=TaskType.CODE,
        description="Implement core functionality",
        dependencies=["t1"],
        files_to_create=["src/main.py"],
    )


@pytest.fixture
def task_test():
    """Sample TEST task"""
    return Task(
        id="t3",
        type=TaskType.TEST,
        description="Create unit tests",
        dependencies=["t2"],
        files_to_create=["tests/test_main.py"],
    )


@pytest.fixture
def task_list_simple():
    """Simple list of tasks with dependencies"""
    return [
        Task(
            id="t1",
            type=TaskType.CONFIG,
            description="Initialize project",
            dependencies=[],
            files_to_create=["README.md"],
        ),
        Task(
            id="t2",
            type=TaskType.CODE,
            description="Write code",
            dependencies=["t1"],
            files_to_create=["src/main.py"],
        ),
        Task(
            id="t3",
            type=TaskType.TEST,
            description="Write tests",
            dependencies=["t2"],
            files_to_create=["tests/test_main.py"],
        ),
    ]


# ============================================================================
# Test Harness Fixtures
# ============================================================================


@pytest.fixture
def agent_test_harness():
    """AgentTestHarness instance for standardized testing"""
    from tests.harness.agent_test_harness import AgentTestHarness

    return AgentTestHarness()


@pytest.fixture
def performance_harness():
    """AgentPerformanceHarness instance for performance testing"""
    from tests.harness.agent_test_harness import AgentPerformanceHarness

    return AgentPerformanceHarness()


# ============================================================================
# Wave 1 Agent Collection
# ============================================================================


@pytest.fixture
def wave1_agents():
    """Collection of all Wave 1 agents for batch testing"""
    return {
        "planner": PlannerAgent(),
        "architect": ArchitectAgent(),
        "safety_guard": SafetyGuard(),
    }


# ============================================================================
# Pytest Configuration
# ============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow tests (>1s)")
    config.addinivalue_line("markers", "wave1: Wave 1 agent tests")
    config.addinivalue_line("markers", "wave2: Wave 2 agent tests")
