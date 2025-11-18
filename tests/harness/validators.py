"""
Result Validators - Comprehensive validation functions for agent outputs

Provides validation functions that return detailed results rather than assertions:
- Task structure validation
- ProjectSpec structure validation
- Pipeline flow validation
- Output completeness checks
"""

from typing import List, Dict, Any, Tuple
from code_factory.core.models import (
    Idea,
    Task,
    TaskType,
    ProjectSpec,
    SafetyCheck,
)


class ValidationResult:
    """Result of a validation check"""

    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def add_error(self, message: str):
        """Add an error (marks validation as failed)"""
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str):
        """Add a warning (doesn't fail validation)"""
        self.warnings.append(message)

    def add_info(self, message: str):
        """Add informational message"""
        self.info.append(message)

    def __bool__(self):
        """Allow use in if statements"""
        return self.is_valid

    def __str__(self):
        """Human-readable summary"""
        lines = []
        if self.is_valid:
            lines.append("✓ Validation passed")
        else:
            lines.append("✗ Validation failed")

        if self.errors:
            lines.append(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.append(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        if self.info:
            lines.append(f"\nInfo ({len(self.info)}):")
            for info in self.info:
                lines.append(f"  - {info}")

        return "\n".join(lines)


# ============================================================================
# Agent Output Validation
# ============================================================================

def validate_agent_output(output: Any, expected_type: type) -> ValidationResult:
    """
    Validate that agent output is the correct type

    Args:
        output: Output from agent.execute()
        expected_type: Expected type of output

    Returns:
        ValidationResult with check details
    """
    result = ValidationResult()

    if not isinstance(output, expected_type):
        result.add_error(
            f"Output type mismatch: expected {expected_type.__name__}, "
            f"got {type(output).__name__}"
        )
    else:
        result.add_info(f"Output type is correct: {expected_type.__name__}")

    return result


# ============================================================================
# Task Structure Validation
# ============================================================================

def validate_task_structure(tasks: List[Task]) -> ValidationResult:
    """
    Comprehensive validation of task list structure

    Checks:
    - Task count is reasonable
    - All tasks have required fields
    - IDs are unique
    - Dependencies are valid
    - No circular dependencies
    - Appropriate task types

    Args:
        tasks: List of Task objects

    Returns:
        ValidationResult with all check details
    """
    result = ValidationResult()

    # Check task count
    if len(tasks) == 0:
        result.add_error("Task list is empty")
        return result  # Can't continue validation

    if len(tasks) > 50:
        result.add_warning(f"Very large task count ({len(tasks)}) - might be overly complex")
    else:
        result.add_info(f"Task count: {len(tasks)}")

    # Check for unique IDs
    task_ids = [t.id for t in tasks]
    if len(task_ids) != len(set(task_ids)):
        duplicates = [tid for tid in task_ids if task_ids.count(tid) > 1]
        result.add_error(f"Duplicate task IDs found: {set(duplicates)}")

    # Validate each task
    task_ids_set = set(task_ids)
    for task in tasks:
        # Check required fields
        if not task.id:
            result.add_error("Task missing ID")

        if not task.description:
            result.add_error(f"Task {task.id} missing description")

        if not task.type:
            result.add_error(f"Task {task.id} missing type")

        # Check dependencies
        if task.id in task.dependencies:
            result.add_error(f"Task {task.id} has self-dependency")

        for dep_id in task.dependencies:
            if dep_id not in task_ids_set:
                result.add_error(
                    f"Task {task.id} depends on non-existent task {dep_id}"
                )

    # Check for circular dependencies
    if not _has_circular_dependencies(tasks):
        result.add_info("No circular dependencies detected")
    else:
        result.add_error("Circular dependencies detected in task graph")

    # Check task type distribution
    type_counts = {}
    for task in tasks:
        type_counts[task.type] = type_counts.get(task.type, 0) + 1

    if TaskType.CODE not in type_counts:
        result.add_warning("No CODE tasks found - project may not generate any code")

    if TaskType.TEST not in type_counts:
        result.add_warning("No TEST tasks found - project will lack tests")

    result.add_info(f"Task type distribution: {dict(type_counts)}")

    return result


def _has_circular_dependencies(tasks: List[Task]) -> bool:
    """Check for circular dependencies using DFS"""
    graph: Dict[str, List[str]] = {t.id: list(t.dependencies) for t in tasks}

    visited = set()
    rec_stack = set()

    def has_cycle(node: str) -> bool:
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

    for task_id in graph.keys():
        if task_id not in visited:
            if has_cycle(task_id):
                return True

    return False


# ============================================================================
# ProjectSpec Validation
# ============================================================================

def validate_spec_structure(spec: ProjectSpec) -> ValidationResult:
    """
    Comprehensive validation of ProjectSpec structure

    Checks:
    - All required fields present
    - Name follows conventions
    - Tech stack is reasonable
    - Folder structure is valid
    - Dependencies are specified
    - Entry point exists

    Args:
        spec: ProjectSpec object

    Returns:
        ValidationResult with all check details
    """
    result = ValidationResult()

    # Name validation
    if not spec.name:
        result.add_error("Project name is missing")
    elif not spec.name.islower():
        if not ('-' in spec.name or '_' in spec.name):
            result.add_warning(
                f"Project name '{spec.name}' should be lowercase with hyphens/underscores"
            )

    result.add_info(f"Project name: {spec.name}")

    # Description
    if not spec.description:
        result.add_error("Project description is missing")
    elif len(spec.description) > 200:
        result.add_warning("Description is very long (>200 chars)")

    # Tech stack validation
    if not spec.tech_stack:
        result.add_error("Tech stack is empty")
    else:
        if "language" not in spec.tech_stack:
            result.add_error("Tech stack must specify 'language'")

        result.add_info(f"Tech stack: {spec.tech_stack}")

        # Check for reasonable technology choices
        language = spec.tech_stack.get("language", "").lower()
        if language not in ["python", "javascript", "typescript", "go", "rust", "java"]:
            result.add_warning(f"Unusual language choice: {language}")

    # Folder structure validation
    if not spec.folder_structure:
        result.add_error("Folder structure is empty")
    else:
        # Check for common folders
        folders = set(spec.folder_structure.keys())

        if not any("src" in f for f in folders):
            result.add_warning("No 'src/' folder found")

        if not any("test" in f for f in folders):
            result.add_warning("No 'tests/' folder found")

        result.add_info(f"Folder structure: {len(spec.folder_structure)} directories")

    # Dependencies
    if not spec.dependencies:
        result.add_warning("No dependencies specified")
    elif len(spec.dependencies) > 20:
        result.add_warning(f"Many dependencies ({len(spec.dependencies)}) - may be complex")

    result.add_info(f"Dependencies: {len(spec.dependencies)} packages")

    # Entry point
    if not spec.entry_point:
        result.add_error("Entry point is missing")
    else:
        result.add_info(f"Entry point: {spec.entry_point}")

    return result


# ============================================================================
# Pipeline Flow Validation
# ============================================================================

def validate_pipeline_flow(
    idea: Idea,
    safety_check: SafetyCheck,
    tasks: List[Task],
    spec: ProjectSpec,
) -> ValidationResult:
    """
    Validate complete pipeline flow from idea to spec

    Checks:
    - Safety check was performed
    - Tasks were generated from idea
    - Spec matches idea intent
    - Data consistency across pipeline

    Args:
        idea: Original input
        safety_check: Safety validation result
        tasks: Generated tasks
        spec: Architecture specification

    Returns:
        ValidationResult with pipeline consistency checks
    """
    result = ValidationResult()

    # Safety check
    if not safety_check.approved:
        result.add_error("Safety check did not approve idea")
        result.add_info(f"Warnings: {safety_check.warnings}")
        return result  # Can't continue if not safe

    result.add_info("Safety check passed")

    # Tasks generated
    if len(tasks) == 0:
        result.add_error("No tasks were generated from idea")

    result.add_info(f"Generated {len(tasks)} tasks")

    # Spec consistency with idea
    if spec.user_profile and spec.user_profile not in idea.target_users:
        result.add_warning(
            f"Spec user_profile '{spec.user_profile}' not in idea.target_users {idea.target_users}"
        )

    if spec.environment and spec.environment != idea.environment:
        result.add_warning(
            f"Spec environment '{spec.environment}' doesn't match idea environment"
        )

    # Check for blue-collar considerations
    if idea.target_users and any(
        role in ["marine engineer", "mechanic", "technician"]
        for role in idea.target_users
    ):
        # Should prefer CLI
        tech_stack_str = str(spec.tech_stack).lower()
        if "cli" not in tech_stack_str and "typer" not in tech_stack_str:
            result.add_warning("Blue-collar users typically need CLI tools")

        # Should have minimal dependencies
        if len(spec.dependencies) > 10:
            result.add_warning(
                f"Blue-collar tools should be simple - {len(spec.dependencies)} dependencies may be too many"
            )

    # Check offline requirement
    if idea.constraints and any("offline" in c.lower() for c in idea.constraints):
        # Check dependencies for cloud services
        deps_str = " ".join(spec.dependencies).lower()
        cloud_keywords = ["aws", "gcp", "azure", "firebase"]
        for keyword in cloud_keywords:
            if keyword in deps_str:
                result.add_warning(
                    f"Offline constraint but dependency on cloud service: {keyword}"
                )

    result.add_info("Pipeline flow validation complete")

    return result


# ============================================================================
# Completeness Validation
# ============================================================================

def validate_output_completeness(output: Any) -> ValidationResult:
    """
    Check if agent output is complete (no missing required fields)

    Args:
        output: Any agent output object

    Returns:
        ValidationResult with completeness checks
    """
    result = ValidationResult()

    # Get all fields from the Pydantic model
    if hasattr(output, "model_fields"):
        fields = output.model_fields
        for field_name, field_info in fields.items():
            value = getattr(output, field_name, None)

            # Check required fields
            if field_info.is_required() and value is None:
                result.add_error(f"Required field '{field_name}' is None")

            # Check empty collections
            if isinstance(value, (list, dict)) and len(value) == 0:
                if field_info.is_required():
                    result.add_warning(f"Required field '{field_name}' is empty")

    else:
        result.add_warning("Output is not a Pydantic model - limited validation")

    return result


# ============================================================================
# Helper Functions
# ============================================================================

def get_validation_summary(result: ValidationResult) -> Dict[str, Any]:
    """
    Get a dictionary summary of validation result

    Args:
        result: ValidationResult object

    Returns:
        Dictionary with summary stats
    """
    return {
        "is_valid": result.is_valid,
        "error_count": len(result.errors),
        "warning_count": len(result.warnings),
        "info_count": len(result.info),
        "errors": result.errors,
        "warnings": result.warnings,
        "info": result.info,
    }
