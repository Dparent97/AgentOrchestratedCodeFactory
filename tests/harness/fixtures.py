"""
Test Fixtures - Helper functions for creating test data

Provides pre-configured test objects for common scenarios:
- Generic test data (Idea, Task, ProjectSpec, etc.)
- Role-specific scenarios (marine engineer, mechanic, data analyst)
- Edge cases and boundary conditions
"""

from typing import List, Optional
from code_factory.core.models import (
    Idea,
    Task,
    TaskType,
    TaskStatus,
    ProjectSpec,
    SafetyCheck,
    SafetyCheckMetadata,
)


# ============================================================================
# Basic Test Data Fixtures
# ============================================================================

def create_test_idea(
    description: str = "Build a test tool",
    target_users: Optional[List[str]] = None,
    environment: Optional[str] = None,
    features: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
) -> Idea:
    """
    Create a basic test Idea with sensible defaults

    Args:
        description: What to build
        target_users: Who will use it
        environment: Where it will run
        features: Specific capabilities
        constraints: Known limitations

    Returns:
        Idea object ready for testing
    """
    return Idea(
        description=description,
        target_users=target_users or ["developer"],
        environment=environment or "desktop",
        features=features or [],
        constraints=constraints or [],
    )


def create_test_task(
    task_id: str = "t1",
    task_type: TaskType = TaskType.CODE,
    description: str = "Test task",
    dependencies: Optional[List[str]] = None,
    files_to_create: Optional[List[str]] = None,
    status: TaskStatus = TaskStatus.PENDING,
) -> Task:
    """
    Create a basic test Task

    Args:
        task_id: Unique identifier
        task_type: Type of task (code, test, doc, config, git)
        description: What this task does
        dependencies: Task IDs that must complete first
        files_to_create: Expected output files
        status: Current execution status

    Returns:
        Task object ready for testing
    """
    return Task(
        id=task_id,
        type=task_type,
        description=description,
        dependencies=dependencies or [],
        files_to_create=files_to_create or [],
        status=status,
    )


def create_test_project_spec(
    name: str = "test-project",
    description: str = "Test project",
    tech_stack: Optional[dict] = None,
    folder_structure: Optional[dict] = None,
    dependencies: Optional[List[str]] = None,
    entry_point: str = "src/main.py",
    user_profile: Optional[str] = None,
    environment: Optional[str] = None,
) -> ProjectSpec:
    """
    Create a basic test ProjectSpec

    Args:
        name: Project identifier
        description: One-line summary
        tech_stack: Technology choices
        folder_structure: File organization
        dependencies: Package requirements
        entry_point: Main file to run
        user_profile: Target user type
        environment: Operating context

    Returns:
        ProjectSpec object ready for testing
    """
    return ProjectSpec(
        name=name,
        description=description,
        tech_stack=tech_stack or {
            "language": "python",
            "cli_framework": "typer",
            "testing": "pytest",
        },
        folder_structure=folder_structure or {
            "src/": ["main.py"],
            "tests/": ["test_main.py"],
        },
        dependencies=dependencies or ["typer", "rich"],
        entry_point=entry_point,
        user_profile=user_profile,
        environment=environment,
    )


def create_test_safety_check(
    approved: bool = True,
    warnings: Optional[List[str]] = None,
    required_confirmations: Optional[List[str]] = None,
    blocked_keywords: Optional[List[str]] = None,
    metadata: Optional[SafetyCheckMetadata] = None,
) -> SafetyCheck:
    """
    Create a basic test SafetyCheck

    Args:
        approved: Whether to proceed
        warnings: Safety concerns
        required_confirmations: User must confirm risky operations
        blocked_keywords: Dangerous patterns found
        metadata: Audit trail

    Returns:
        SafetyCheck object ready for testing
    """
    return SafetyCheck(
        approved=approved,
        warnings=warnings or [],
        required_confirmations=required_confirmations or [],
        blocked_keywords=blocked_keywords or [],
        metadata=metadata,
    )


# ============================================================================
# Role-Specific Scenario Fixtures
# ============================================================================

def create_marine_engineer_idea(
    description: str = "Parse marine engine alarm logs and highlight critical issues",
    features: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
) -> Idea:
    """
    Create an Idea typical of marine engineering scenarios

    Includes common marine engineer context:
    - Noisy, limited connectivity environment
    - Focus on alarms and diagnostics
    - Offline-first requirements

    Args:
        description: Specific tool to build
        features: Additional capabilities
        constraints: Additional limitations

    Returns:
        Idea configured for marine engineering context
    """
    default_features = [
        "Filter for critical alarms only",
        "Color-coded severity levels",
        "Export filtered results to CSV",
        "Timestamp range filtering",
    ]

    default_constraints = [
        "Must work offline",
        "Large fonts for readability in bright sunlight",
        "Simple CLI - no complex commands",
        "Minimal dependencies for easy installation",
    ]

    return Idea(
        description=description,
        target_users=["marine engineer", "chief engineer"],
        environment="ship engine room, noisy, limited WiFi, tablet display",
        features=features or default_features,
        constraints=constraints or default_constraints,
    )


def create_data_analyst_idea(
    description: str = "Parse CSV files and generate summary statistics",
    features: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
) -> Idea:
    """
    Create an Idea typical of data analyst scenarios

    Includes common data analyst context:
    - Desktop environment with good connectivity
    - Focus on data processing and analysis
    - CSV/Excel compatibility

    Args:
        description: Specific tool to build
        features: Additional capabilities
        constraints: Additional limitations

    Returns:
        Idea configured for data analyst context
    """
    default_features = [
        "Calculate mean, median, mode",
        "Generate histograms and charts",
        "Export results to JSON",
        "Handle missing data gracefully",
    ]

    default_constraints = [
        "Should work with large files (>1GB)",
        "Output must be reproducible",
    ]

    return Idea(
        description=description,
        target_users=["data analyst", "data scientist"],
        environment="desktop, Windows/Mac, good internet",
        features=features or default_features,
        constraints=constraints or default_constraints,
    )


def create_mechanic_idea(
    description: str = "Look up torque specifications for bolts",
    features: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
) -> Idea:
    """
    Create an Idea typical of mechanic scenarios

    Includes common mechanic context:
    - Workshop/garage environment
    - Quick lookup tools
    - May be used with dirty hands/gloves

    Args:
        description: Specific tool to build
        features: Additional capabilities
        constraints: Additional limitations

    Returns:
        Idea configured for mechanic context
    """
    default_features = [
        "Search by bolt size and grade",
        "Display torque in multiple units (ft-lb, Nm)",
        "Show torque sequence diagrams",
        "Offline database of specifications",
    ]

    default_constraints = [
        "Large buttons - usable with gloves",
        "Simple interface - minimal typing",
        "No installation required",
        "Works on tablet or phone",
    ]

    return Idea(
        description=description,
        target_users=["mechanic", "automotive technician"],
        environment="garage, workshop, may have dirty hands",
        features=features or default_features,
        constraints=constraints or default_constraints,
    )


def create_simple_calculator_idea() -> Idea:
    """Create a very simple idea (minimal complexity)"""
    return Idea(
        description="Build a simple calculator CLI",
        target_users=["student"],
        environment="desktop",
        features=["Add, subtract, multiply, divide"],
        constraints=["Keep it simple - basic operations only"],
    )


def create_complex_data_pipeline_idea() -> Idea:
    """Create a complex idea (high complexity)"""
    return Idea(
        description="Build a real-time data processing pipeline with ML anomaly detection",
        target_users=["data engineer", "ML engineer"],
        environment="cloud, AWS/GCP, high availability required",
        features=[
            "Ingest data from Kafka streams",
            "Real-time anomaly detection using ML models",
            "Store results in PostgreSQL and S3",
            "Dashboard for monitoring",
            "Alert system via email/Slack",
            "Auto-scaling based on load",
        ],
        constraints=[
            "Must handle 10K events/second",
            "99.9% uptime SLA",
            "Support multiple data formats (JSON, CSV, Avro)",
            "Kubernetes deployment",
        ],
    )


# ============================================================================
# Edge Case Fixtures
# ============================================================================

def create_minimal_idea() -> Idea:
    """Minimal valid Idea (just description)"""
    return Idea(description="Build a tool")


def create_dangerous_idea() -> Idea:
    """Idea that should be blocked by SafetyGuard"""
    return Idea(
        description="Control industrial equipment remotely and override safety interlocks",
        target_users=["operator"],
        environment="factory floor",
    )


def create_ambiguous_idea() -> Idea:
    """Vague idea that's hard to plan"""
    return Idea(
        description="Make something useful",
        target_users=["user"],
        environment="somewhere",
    )


# ============================================================================
# Task List Fixtures
# ============================================================================

def create_linear_task_list() -> List[Task]:
    """Create a simple linear task dependency chain"""
    return [
        create_test_task("t1", TaskType.CONFIG, "Setup project", []),
        create_test_task("t2", TaskType.CODE, "Write code", ["t1"]),
        create_test_task("t3", TaskType.TEST, "Write tests", ["t2"]),
        create_test_task("t4", TaskType.DOC, "Write docs", ["t2"]),
    ]


def create_parallel_task_list() -> List[Task]:
    """Create tasks with parallel execution opportunities"""
    return [
        create_test_task("t1", TaskType.CONFIG, "Setup project", []),
        create_test_task("t2", TaskType.CODE, "Write module A", ["t1"]),
        create_test_task("t3", TaskType.CODE, "Write module B", ["t1"]),
        create_test_task("t4", TaskType.TEST, "Test module A", ["t2"]),
        create_test_task("t5", TaskType.TEST, "Test module B", ["t3"]),
        create_test_task("t6", TaskType.DOC, "Write docs", ["t2", "t3"]),
    ]


def create_complex_dependency_graph() -> List[Task]:
    """Create a complex task graph with multiple dependencies"""
    return [
        create_test_task("t1", TaskType.CONFIG, "Initialize project", []),
        create_test_task("t2", TaskType.CODE, "Database models", ["t1"]),
        create_test_task("t3", TaskType.CODE, "API endpoints", ["t1", "t2"]),
        create_test_task("t4", TaskType.CODE, "Business logic", ["t2"]),
        create_test_task("t5", TaskType.CODE, "Frontend UI", ["t3"]),
        create_test_task("t6", TaskType.TEST, "Unit tests", ["t2", "t4"]),
        create_test_task("t7", TaskType.TEST, "Integration tests", ["t3", "t5"]),
        create_test_task("t8", TaskType.DOC, "API documentation", ["t3"]),
        create_test_task("t9", TaskType.DOC, "User guide", ["t5"]),
    ]


# ============================================================================
# Helper Functions
# ============================================================================

def create_test_scenario(
    scenario_name: str,
    idea: Optional[Idea] = None,
    expected_task_count: Optional[int] = None,
    expected_tech_stack: Optional[dict] = None,
) -> dict:
    """
    Create a complete test scenario with expectations

    Args:
        scenario_name: Name of the scenario
        idea: The input Idea
        expected_task_count: How many tasks should be generated
        expected_tech_stack: What tech stack should be chosen

    Returns:
        Dictionary with scenario data and expectations
    """
    return {
        "name": scenario_name,
        "idea": idea or create_test_idea(),
        "expectations": {
            "task_count": expected_task_count,
            "tech_stack": expected_tech_stack,
        },
    }
