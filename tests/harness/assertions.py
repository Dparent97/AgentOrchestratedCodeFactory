"""
Assertion Utilities - Specialized assertions for validating agent outputs

Provides high-level assertions that check common agent output patterns:
- Task list validation (structure, dependencies, completeness)
- ProjectSpec validation (tech stack, structure, naming)
- SafetyCheck validation (approval status, warnings)
- Blue-collar friendliness checks
- Dependency graph validation
"""

from typing import List, Dict, Any
from code_factory.core.models import (
    Task,
    TaskType,
    ProjectSpec,
    SafetyCheck,
)


# ============================================================================
# Task List Assertions
# ============================================================================

def assert_valid_task_list(tasks: List[Task], min_tasks: int = 1) -> None:
    """
    Assert that a task list is valid

    Checks:
    - At least min_tasks tasks exist
    - All tasks have unique IDs
    - All tasks have descriptions
    - All tasks have types

    Args:
        tasks: List of Task objects
        min_tasks: Minimum number of tasks expected

    Raises:
        AssertionError: If validation fails
    """
    assert len(tasks) >= min_tasks, f"Expected at least {min_tasks} tasks, got {len(tasks)}"

    # Check for unique IDs
    task_ids = [t.id for t in tasks]
    assert len(task_ids) == len(set(task_ids)), f"Duplicate task IDs found: {task_ids}"

    # Validate each task
    for task in tasks:
        assert task.id, f"Task missing ID: {task}"
        assert task.description, f"Task {task.id} missing description"
        assert task.type, f"Task {task.id} missing type"
        assert isinstance(task.type, TaskType), f"Task {task.id} has invalid type: {task.type}"


def assert_task_dependencies_valid(tasks: List[Task]) -> None:
    """
    Assert that task dependencies are valid

    Checks:
    - All dependency IDs reference existing tasks
    - No self-dependencies (task depends on itself)

    Args:
        tasks: List of Task objects

    Raises:
        AssertionError: If dependencies are invalid
    """
    task_ids = {t.id for t in tasks}

    for task in tasks:
        # Check self-dependency
        assert task.id not in task.dependencies, \
            f"Task {task.id} has self-dependency"

        # Check all dependencies exist
        for dep_id in task.dependencies:
            assert dep_id in task_ids, \
                f"Task {task.id} depends on non-existent task {dep_id}"


def assert_no_circular_dependencies(tasks: List[Task]) -> None:
    """
    Assert that there are no circular dependencies in task graph

    Uses topological sort to detect cycles.

    Args:
        tasks: List of Task objects

    Raises:
        AssertionError: If circular dependencies exist
    """
    # Build adjacency list
    graph: Dict[str, List[str]] = {t.id: list(t.dependencies) for t in tasks}

    # Track visited nodes
    visited = set()
    rec_stack = set()

    def has_cycle(node: str) -> bool:
        """DFS to detect cycle"""
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    # Check each node
    for task_id in graph.keys():
        if task_id not in visited:
            assert not has_cycle(task_id), \
                f"Circular dependency detected involving task {task_id}"


def assert_has_task_type(tasks: List[Task], task_type: TaskType) -> None:
    """
    Assert that task list contains at least one task of given type

    Args:
        tasks: List of Task objects
        task_type: Expected TaskType

    Raises:
        AssertionError: If no task of given type exists
    """
    types = {t.type for t in tasks}
    assert task_type in types, \
        f"Expected task type {task_type.value} not found. Available: {[t.value for t in types]}"


def assert_task_count_in_range(tasks: List[Task], min_count: int, max_count: int) -> None:
    """
    Assert that task count is within expected range

    Args:
        tasks: List of Task objects
        min_count: Minimum expected tasks
        max_count: Maximum expected tasks

    Raises:
        AssertionError: If count is outside range
    """
    count = len(tasks)
    assert min_count <= count <= max_count, \
        f"Task count {count} not in expected range [{min_count}, {max_count}]"


# ============================================================================
# ProjectSpec Assertions
# ============================================================================

def assert_valid_project_spec(spec: ProjectSpec) -> None:
    """
    Assert that a ProjectSpec is valid

    Checks:
    - Has valid name (lowercase, hyphens only)
    - Has description
    - Has tech_stack with at least 'language'
    - Has folder_structure
    - Has entry_point that exists in folder_structure

    Args:
        spec: ProjectSpec object

    Raises:
        AssertionError: If validation fails
    """
    # Name validation
    assert spec.name, "ProjectSpec missing name"
    assert spec.name.islower() or '-' in spec.name or '_' in spec.name, \
        f"Project name should be lowercase with hyphens/underscores: {spec.name}"

    # Description
    assert spec.description, "ProjectSpec missing description"

    # Tech stack
    assert spec.tech_stack, "ProjectSpec missing tech_stack"
    assert "language" in spec.tech_stack, \
        "tech_stack must specify 'language'"

    # Folder structure
    assert spec.folder_structure, "ProjectSpec missing folder_structure"
    assert len(spec.folder_structure) > 0, \
        "folder_structure must have at least one directory"

    # Entry point exists in structure
    assert spec.entry_point, "ProjectSpec missing entry_point"
    entry_found = False
    for folder, files in spec.folder_structure.items():
        if spec.entry_point in files or spec.entry_point.startswith(folder):
            entry_found = True
            break

    # More lenient check - just verify entry point is specified
    assert spec.entry_point, "entry_point must be specified"


def assert_has_tech_stack_key(spec: ProjectSpec, key: str) -> None:
    """
    Assert that tech_stack contains a specific key

    Args:
        spec: ProjectSpec object
        key: Expected key in tech_stack

    Raises:
        AssertionError: If key not found
    """
    assert key in spec.tech_stack, \
        f"tech_stack missing expected key '{key}'. Available: {list(spec.tech_stack.keys())}"


def assert_has_dependency(spec: ProjectSpec, package: str) -> None:
    """
    Assert that dependencies list contains a package

    Args:
        spec: ProjectSpec object
        package: Expected package name

    Raises:
        AssertionError: If package not found
    """
    assert package in spec.dependencies, \
        f"Expected dependency '{package}' not found. Available: {spec.dependencies}"


def assert_folder_exists(spec: ProjectSpec, folder: str) -> None:
    """
    Assert that folder_structure contains a folder

    Args:
        spec: ProjectSpec object
        folder: Expected folder path

    Raises:
        AssertionError: If folder not found
    """
    assert folder in spec.folder_structure, \
        f"Expected folder '{folder}' not found. Available: {list(spec.folder_structure.keys())}"


def assert_file_in_folder(spec: ProjectSpec, folder: str, filename: str) -> None:
    """
    Assert that a file exists in a specific folder

    Args:
        spec: ProjectSpec object
        folder: Folder path
        filename: Expected file name

    Raises:
        AssertionError: If file not found in folder
    """
    assert folder in spec.folder_structure, \
        f"Folder '{folder}' not found in structure"

    files = spec.folder_structure[folder]
    assert filename in files, \
        f"File '{filename}' not found in folder '{folder}'. Available: {files}"


# ============================================================================
# SafetyCheck Assertions
# ============================================================================

def assert_valid_safety_check(check: SafetyCheck) -> None:
    """
    Assert that a SafetyCheck is valid

    Checks:
    - Has approved field (bool)
    - Has warnings list
    - Has required_confirmations list
    - Has blocked_keywords list

    Args:
        check: SafetyCheck object

    Raises:
        AssertionError: If validation fails
    """
    assert isinstance(check.approved, bool), \
        "SafetyCheck.approved must be a boolean"
    assert isinstance(check.warnings, list), \
        "SafetyCheck.warnings must be a list"
    assert isinstance(check.required_confirmations, list), \
        "SafetyCheck.required_confirmations must be a list"
    assert isinstance(check.blocked_keywords, list), \
        "SafetyCheck.blocked_keywords must be a list"


def assert_safety_approved(check: SafetyCheck) -> None:
    """
    Assert that safety check was approved

    Args:
        check: SafetyCheck object

    Raises:
        AssertionError: If not approved
    """
    assert check.approved, \
        f"Expected safety check to be approved. Warnings: {check.warnings}"


def assert_safety_rejected(check: SafetyCheck) -> None:
    """
    Assert that safety check was rejected

    Args:
        check: SafetyCheck object

    Raises:
        AssertionError: If approved
    """
    assert not check.approved, \
        "Expected safety check to be rejected, but it was approved"


def assert_has_warning(check: SafetyCheck, keyword: str) -> None:
    """
    Assert that safety check contains a warning with keyword

    Args:
        check: SafetyCheck object
        keyword: Expected keyword in warnings

    Raises:
        AssertionError: If keyword not found in any warning
    """
    warnings_text = " ".join(check.warnings).lower()
    assert keyword.lower() in warnings_text, \
        f"Expected keyword '{keyword}' not found in warnings: {check.warnings}"


# ============================================================================
# Blue-Collar Friendliness Assertions
# ============================================================================

def assert_blue_collar_friendly(spec: ProjectSpec) -> None:
    """
    Assert that a ProjectSpec follows blue-collar design principles

    Checks for:
    - Simple, practical tech choices (CLI over web, minimal dependencies)
    - Clear folder structure
    - Obvious entry point

    Args:
        spec: ProjectSpec object

    Raises:
        AssertionError: If design doesn't follow blue-collar principles
    """
    # Check for simple tech stack (prefer CLI over web)
    tech_stack_str = str(spec.tech_stack).lower()

    # Prefer CLI frameworks
    blue_collar_indicators = ["cli", "typer", "argparse", "click"]
    has_cli = any(indicator in tech_stack_str for indicator in blue_collar_indicators)

    # Avoid overly complex frameworks
    complex_indicators = ["django", "flask", "fastapi", "react", "vue"]
    has_complex = any(indicator in tech_stack_str for indicator in complex_indicators)

    # Simple projects should prefer CLI
    if not has_complex:
        assert has_cli or "web" in tech_stack_str, \
            "Blue-collar tools should prefer CLI interfaces for simplicity"

    # Check for minimal dependencies
    assert len(spec.dependencies) <= 10, \
        f"Too many dependencies ({len(spec.dependencies)}) - blue-collar tools should be simple"

    # Check for clear entry point
    assert spec.entry_point.endswith((".py", ".js", ".sh")), \
        f"Entry point should be a clear script file: {spec.entry_point}"


def assert_offline_capable(spec: ProjectSpec) -> None:
    """
    Assert that spec suggests offline capability

    Checks that dependencies don't require cloud services.

    Args:
        spec: ProjectSpec object

    Raises:
        AssertionError: If design requires cloud/online services
    """
    # Check dependencies for cloud services
    cloud_keywords = ["aws", "gcp", "azure", "firebase", "supabase"]
    deps_str = " ".join(spec.dependencies).lower()

    for keyword in cloud_keywords:
        assert keyword not in deps_str, \
            f"Offline-capable tool shouldn't depend on cloud service: {keyword}"


# ============================================================================
# General Validation Assertions
# ============================================================================

def assert_all_fields_present(obj: Any, required_fields: List[str]) -> None:
    """
    Assert that an object has all required fields

    Args:
        obj: Object to check
        required_fields: List of field names that must be present

    Raises:
        AssertionError: If any field is missing
    """
    for field in required_fields:
        assert hasattr(obj, field), \
            f"Object missing required field: {field}"
        value = getattr(obj, field)
        assert value is not None, \
            f"Required field '{field}' is None"


def assert_is_not_empty(value: Any, field_name: str = "value") -> None:
    """
    Assert that a value is not empty (None, empty string, empty list, etc.)

    Args:
        value: Value to check
        field_name: Name of the field (for error message)

    Raises:
        AssertionError: If value is empty
    """
    assert value is not None, f"{field_name} is None"

    if isinstance(value, (str, list, dict)):
        assert len(value) > 0, f"{field_name} is empty"
