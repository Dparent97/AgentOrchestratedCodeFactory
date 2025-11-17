"""
Data models for the Code Factory

Defines all core data structures used throughout the system using Pydantic
for validation and serialization.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class TaskType(str, Enum):
    """Types of tasks that can be executed"""
    CONFIG = "config"
    CODE = "code"
    TEST = "test"
    DOC = "doc"
    GIT = "git"


class TaskStatus(str, Enum):
    """Status of a task"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class Idea(BaseModel):
    """
    Represents a human's plain-language idea for a project
    
    This is the input to the entire factory process. It captures what
    the user wants to build, who it's for, and the environment it will
    be used in.
    """
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
    
    @field_validator("description")
    @classmethod
    def description_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")
        return v.strip()


class ProjectSpec(BaseModel):
    """
    Technical specification for a project
    
    Output of the ArchitectAgent. Defines all architectural decisions
    needed to implement the idea.
    """
    name: str = Field(..., description="Project name (lowercase, hyphen-separated)")
    description: str = Field(..., description="One-line project description")
    tech_stack: Dict[str, str] = Field(
        ...,
        description="Technology choices (e.g., {'language': 'python', 'cli': 'typer'})"
    )
    folder_structure: Dict[str, List[str]] = Field(
        ...,
        description="Directory structure (e.g., {'src/': ['main.py', 'utils.py']})"
    )
    dependencies: List[str] = Field(
        default_factory=list,
        description="Package dependencies"
    )
    entry_point: str = Field(..., description="Main entry point file")
    user_profile: Optional[str] = Field(
        None,
        description="Target user profile (e.g., 'marine_engineer')"
    )
    environment: Optional[str] = Field(
        None,
        description="Target operating environment"
    )
    
    @field_validator("name")
    @classmethod
    def name_valid_format(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        # Basic validation: lowercase, hyphens, underscores
        if not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError("Name must contain only alphanumeric characters, hyphens, and underscores")
        return v.strip().lower()


class Task(BaseModel):
    """
    A single unit of work in the project build process
    
    Output of the PlannerAgent. Represents an atomic task with
    dependencies and execution requirements.
    """
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
    agent: Optional[str] = Field(
        None,
        description="Which agent should execute this task"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current status"
    )


class AgentRun(BaseModel):
    """
    Record of an agent execution
    
    Tracks the execution of a single agent, including timing,
    status, and any errors.
    """
    agent_name: str = Field(..., description="Name of the agent")
    input_data: Dict[str, Any] = Field(..., description="Input provided to agent")
    output_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Output produced by agent"
    )
    status: str = Field(default="pending", description="Execution status")
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error: Optional[str] = Field(None, description="Error message if failed")
    duration_seconds: Optional[float] = None


class SafetyCheck(BaseModel):
    """
    Result of safety validation
    
    Output of SafetyGuard agent indicating whether an idea is safe
    to proceed with, and any warnings or confirmations needed.
    """
    approved: bool = Field(..., description="Whether idea is approved to proceed")
    warnings: List[str] = Field(
        default_factory=list,
        description="Safety warnings or concerns"
    )
    required_confirmations: List[str] = Field(
        default_factory=list,
        description="Actions requiring explicit human confirmation"
    )
    blocked_keywords: List[str] = Field(
        default_factory=list,
        description="Dangerous keywords found in idea"
    )


class AdvisoryReport(BaseModel):
    """
    Blue-collar usability advisory
    
    Output of BlueCollarAdvisor agent with recommendations for
    making the tool more practical for field use.
    """
    recommendations: List[str] = Field(
        default_factory=list,
        description="Suggested improvements"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="Potential usability issues"
    )
    environment_fit: str = Field(
        default="unknown",
        description="How well the solution fits the target environment"
    )
    accessibility_score: Optional[int] = Field(
        None,
        ge=0,
        le=10,
        description="Usability score (0-10)"
    )


class TestResult(BaseModel):
    """
    Results from test execution
    
    Output of TesterAgent indicating test success/failure and coverage.
    """
    total_tests: int = Field(default=0, ge=0)
    passed: int = Field(default=0, ge=0)
    failed: int = Field(default=0, ge=0)
    skipped: int = Field(default=0, ge=0)
    coverage_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    error_messages: List[str] = Field(default_factory=list)
    success: bool = Field(default=False)


class ProjectResult(BaseModel):
    """
    Final result of factory execution
    
    Contains the path to the generated project and metadata about
    the build process.
    """
    success: bool = Field(..., description="Whether build succeeded")
    project_path: Optional[str] = Field(None, description="Path to generated project")
    project_name: str = Field(..., description="Name of the generated project")
    agent_runs: List[AgentRun] = Field(
        default_factory=list,
        description="Record of all agent executions"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="Errors encountered during build"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    duration_seconds: Optional[float] = None
    git_repo_url: Optional[str] = Field(None, description="GitHub repository URL if created")
