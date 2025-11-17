"""
Unit tests for data models

Tests cover:
- Pydantic validation for all models
- Field validators
- Model serialization/deserialization
- Default values
- Edge cases and error conditions
- Enums
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from code_factory.core.models import (
    AdvisoryReport,
    AgentRun,
    Idea,
    ProjectResult,
    ProjectSpec,
    SafetyCheck,
    Task,
    TaskStatus,
    TaskType,
    TestResult,
)


class TestEnums:
    """Test enum definitions"""

    def test_task_type_values(self):
        """Test TaskType enum has expected values"""
        assert TaskType.CONFIG == "config"
        assert TaskType.CODE == "code"
        assert TaskType.TEST == "test"
        assert TaskType.DOC == "doc"
        assert TaskType.GIT == "git"

    def test_task_status_values(self):
        """Test TaskStatus enum has expected values"""
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.RUNNING == "running"
        assert TaskStatus.SUCCESS == "success"
        assert TaskStatus.FAILED == "failed"
        assert TaskStatus.SKIPPED == "skipped"

    def test_task_type_from_string(self):
        """Test TaskType can be created from string"""
        assert TaskType("config") == TaskType.CONFIG
        assert TaskType("code") == TaskType.CODE

    def test_invalid_task_type_raises_error(self):
        """Test invalid TaskType raises error"""
        with pytest.raises(ValueError):
            TaskType("invalid")


class TestIdeaModel:
    """Test Idea model validation"""

    def test_idea_with_all_fields(self):
        """Test Idea creation with all fields"""
        idea = Idea(
            description="Build a maintenance tracker",
            target_users=["mechanic", "engineer"],
            environment="noisy workshop",
            features=["offline mode", "voice input"],
            constraints=["no cloud", "must run on old hardware"]
        )

        assert idea.description == "Build a maintenance tracker"
        assert len(idea.target_users) == 2
        assert idea.environment == "noisy workshop"
        assert len(idea.features) == 2
        assert len(idea.constraints) == 2

    def test_idea_with_minimal_fields(self):
        """Test Idea with only required fields"""
        idea = Idea(description="Simple tool")

        assert idea.description == "Simple tool"
        assert idea.target_users == []
        assert idea.environment is None
        assert idea.features == []
        assert idea.constraints == []

    def test_empty_description_rejected(self):
        """Test that empty description is rejected"""
        with pytest.raises(ValidationError):
            Idea(description="")

    def test_whitespace_description_rejected(self):
        """Test that whitespace-only description is rejected"""
        with pytest.raises(ValidationError):
            Idea(description="   ")

    def test_description_is_stripped(self):
        """Test that description is stripped of whitespace"""
        idea = Idea(description="  Test description  ")
        assert idea.description == "Test description"

    def test_missing_description_rejected(self):
        """Test that missing description is rejected"""
        with pytest.raises(ValidationError):
            Idea()

    def test_idea_serialization(self):
        """Test Idea can be serialized to dict"""
        idea = Idea(
            description="Test",
            target_users=["user1"],
            features=["feature1"]
        )
        data = idea.model_dump()

        assert isinstance(data, dict)
        assert data["description"] == "Test"
        assert data["target_users"] == ["user1"]
        assert data["features"] == ["feature1"]

    def test_idea_deserialization(self):
        """Test Idea can be created from dict"""
        data = {
            "description": "Test tool",
            "target_users": ["engineer"],
            "features": ["offline"]
        }
        idea = Idea(**data)

        assert idea.description == "Test tool"
        assert idea.target_users == ["engineer"]


class TestProjectSpecModel:
    """Test ProjectSpec model validation"""

    def test_project_spec_with_all_fields(self):
        """Test ProjectSpec with all fields"""
        spec = ProjectSpec(
            name="my-tool",
            description="A maintenance tool",
            tech_stack={"language": "python", "cli": "typer"},
            folder_structure={"src/": ["main.py", "utils.py"]},
            dependencies=["typer", "pytest"],
            entry_point="src/main.py",
            user_profile="mechanic",
            environment="workshop"
        )

        assert spec.name == "my-tool"
        assert spec.description == "A maintenance tool"
        assert spec.tech_stack["language"] == "python"
        assert "src/" in spec.folder_structure
        assert len(spec.dependencies) == 2
        assert spec.entry_point == "src/main.py"

    def test_project_name_validation_lowercase(self):
        """Test that project name is converted to lowercase"""
        spec = ProjectSpec(
            name="MyTool",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        assert spec.name == "mytool"

    def test_project_name_strips_whitespace(self):
        """Test that project name with whitespace is rejected"""
        # Names with leading/trailing spaces fail validation before stripping
        with pytest.raises(ValidationError):
            ProjectSpec(
                name="  my-tool  ",
                description="Test",
                tech_stack={},
                folder_structure={},
                entry_point="main.py"
            )

    def test_empty_name_rejected(self):
        """Test that empty name is rejected"""
        with pytest.raises(ValidationError):
            ProjectSpec(
                name="",
                description="Test",
                tech_stack={},
                folder_structure={},
                entry_point="main.py"
            )

    def test_invalid_characters_in_name_rejected(self):
        """Test that invalid characters in name are rejected"""
        with pytest.raises(ValidationError):
            ProjectSpec(
                name="my tool!",
                description="Test",
                tech_stack={},
                folder_structure={},
                entry_point="main.py"
            )

    def test_name_with_hyphens_accepted(self):
        """Test that hyphens in name are accepted"""
        spec = ProjectSpec(
            name="my-cool-tool",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        assert spec.name == "my-cool-tool"

    def test_name_with_underscores_accepted(self):
        """Test that underscores in name are accepted"""
        spec = ProjectSpec(
            name="my_tool_name",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        assert spec.name == "my_tool_name"

    def test_project_spec_serialization(self):
        """Test ProjectSpec serialization"""
        spec = ProjectSpec(
            name="test",
            description="Test spec",
            tech_stack={"lang": "python"},
            folder_structure={"src/": ["main.py"]},
            entry_point="main.py"
        )
        data = spec.model_dump()

        assert isinstance(data, dict)
        assert data["name"] == "test"


class TestTaskModel:
    """Test Task model validation"""

    def test_task_with_all_fields(self):
        """Test Task with all fields"""
        task = Task(
            id="task-1",
            type=TaskType.CODE,
            description="Write main.py",
            dependencies=["task-0"],
            files_to_create=["main.py", "utils.py"],
            agent="implementer",
            status=TaskStatus.PENDING
        )

        assert task.id == "task-1"
        assert task.type == TaskType.CODE
        assert task.description == "Write main.py"
        assert len(task.dependencies) == 1
        assert len(task.files_to_create) == 2
        assert task.agent == "implementer"
        assert task.status == TaskStatus.PENDING

    def test_task_defaults(self):
        """Test Task default values"""
        task = Task(
            id="task-1",
            type=TaskType.TEST,
            description="Run tests"
        )

        assert task.dependencies == []
        assert task.files_to_create == []
        assert task.agent is None
        assert task.status == TaskStatus.PENDING

    def test_task_type_enum(self):
        """Test Task with different types"""
        for task_type in [TaskType.CONFIG, TaskType.CODE, TaskType.TEST, TaskType.DOC, TaskType.GIT]:
            task = Task(id="task", type=task_type, description="Test")
            assert task.type == task_type

    def test_task_status_enum(self):
        """Test Task with different statuses"""
        for status in TaskStatus:
            task = Task(
                id="task",
                type=TaskType.CODE,
                description="Test",
                status=status
            )
            assert task.status == status


class TestAgentRunModel:
    """Test AgentRun model validation"""

    def test_agent_run_with_all_fields(self):
        """Test AgentRun with all fields"""
        now = datetime.now()
        run = AgentRun(
            agent_name="test_agent",
            input_data={"key": "value"},
            output_data={"result": "success"},
            status="success",
            started_at=now,
            completed_at=now,
            error=None,
            duration_seconds=1.5
        )

        assert run.agent_name == "test_agent"
        assert run.input_data == {"key": "value"}
        assert run.output_data == {"result": "success"}
        assert run.status == "success"
        assert run.duration_seconds == 1.5

    def test_agent_run_defaults(self):
        """Test AgentRun default values"""
        run = AgentRun(
            agent_name="test_agent",
            input_data={}
        )

        assert run.status == "pending"
        assert run.started_at is not None
        assert run.completed_at is None
        assert run.error is None
        assert run.duration_seconds is None

    def test_agent_run_with_error(self):
        """Test AgentRun with error"""
        run = AgentRun(
            agent_name="failing_agent",
            input_data={},
            status="failed",
            error="Something went wrong"
        )

        assert run.status == "failed"
        assert run.error == "Something went wrong"


class TestSafetyCheckModel:
    """Test SafetyCheck model validation"""

    def test_safety_check_approved(self):
        """Test SafetyCheck for approved idea"""
        check = SafetyCheck(
            approved=True,
            warnings=[],
            required_confirmations=["Network access required"],
            blocked_keywords=[]
        )

        assert check.approved is True
        assert len(check.warnings) == 0
        assert len(check.required_confirmations) == 1
        assert len(check.blocked_keywords) == 0

    def test_safety_check_blocked(self):
        """Test SafetyCheck for blocked idea"""
        check = SafetyCheck(
            approved=False,
            warnings=["Dangerous operation detected"],
            required_confirmations=[],
            blocked_keywords=["hack", "exploit"]
        )

        assert check.approved is False
        assert len(check.warnings) == 1
        assert len(check.blocked_keywords) == 2

    def test_safety_check_defaults(self):
        """Test SafetyCheck default values"""
        check = SafetyCheck(approved=True)

        assert check.warnings == []
        assert check.required_confirmations == []
        assert check.blocked_keywords == []


class TestAdvisoryReportModel:
    """Test AdvisoryReport model validation"""

    def test_advisory_report_with_all_fields(self):
        """Test AdvisoryReport with all fields"""
        report = AdvisoryReport(
            recommendations=["Add offline mode", "Simplify UI"],
            warnings=["May be too complex"],
            environment_fit="good",
            accessibility_score=8
        )

        assert len(report.recommendations) == 2
        assert len(report.warnings) == 1
        assert report.environment_fit == "good"
        assert report.accessibility_score == 8

    def test_advisory_report_defaults(self):
        """Test AdvisoryReport default values"""
        report = AdvisoryReport()

        assert report.recommendations == []
        assert report.warnings == []
        assert report.environment_fit == "unknown"
        assert report.accessibility_score is None

    def test_accessibility_score_validation(self):
        """Test accessibility_score range validation"""
        # Valid scores
        for score in [0, 5, 10]:
            report = AdvisoryReport(accessibility_score=score)
            assert report.accessibility_score == score

        # Invalid scores
        with pytest.raises(ValidationError):
            AdvisoryReport(accessibility_score=-1)

        with pytest.raises(ValidationError):
            AdvisoryReport(accessibility_score=11)


class TestTestResultModel:
    """Test TestResult model validation"""

    def test_test_result_with_all_fields(self):
        """Test TestResult with all fields"""
        result = TestResult(
            total_tests=10,
            passed=8,
            failed=2,
            skipped=0,
            coverage_percent=85.5,
            error_messages=["Test 1 failed", "Test 2 failed"],
            success=False
        )

        assert result.total_tests == 10
        assert result.passed == 8
        assert result.failed == 2
        assert result.coverage_percent == 85.5
        assert len(result.error_messages) == 2
        assert result.success is False

    def test_test_result_defaults(self):
        """Test TestResult default values"""
        result = TestResult()

        assert result.total_tests == 0
        assert result.passed == 0
        assert result.failed == 0
        assert result.skipped == 0
        assert result.coverage_percent is None
        assert result.error_messages == []
        assert result.success is False

    def test_test_counts_non_negative(self):
        """Test that test counts cannot be negative"""
        with pytest.raises(ValidationError):
            TestResult(total_tests=-1)

        with pytest.raises(ValidationError):
            TestResult(passed=-1)

        with pytest.raises(ValidationError):
            TestResult(failed=-1)

    def test_coverage_percent_range(self):
        """Test coverage_percent range validation"""
        # Valid coverage
        result = TestResult(coverage_percent=0.0)
        assert result.coverage_percent == 0.0

        result = TestResult(coverage_percent=100.0)
        assert result.coverage_percent == 100.0

        # Invalid coverage
        with pytest.raises(ValidationError):
            TestResult(coverage_percent=-0.1)

        with pytest.raises(ValidationError):
            TestResult(coverage_percent=100.1)


class TestProjectResultModel:
    """Test ProjectResult model validation"""

    def test_project_result_success(self):
        """Test successful ProjectResult"""
        result = ProjectResult(
            success=True,
            project_path="/path/to/project",
            project_name="my-tool",
            agent_runs=[],
            errors=[]
        )

        assert result.success is True
        assert result.project_path == "/path/to/project"
        assert result.project_name == "my-tool"
        assert len(result.errors) == 0

    def test_project_result_failure(self):
        """Test failed ProjectResult"""
        result = ProjectResult(
            success=False,
            project_name="failed-project",
            errors=["Agent failed", "Build failed"]
        )

        assert result.success is False
        assert result.project_path is None
        assert len(result.errors) == 2

    def test_project_result_defaults(self):
        """Test ProjectResult default values"""
        result = ProjectResult(
            success=True,
            project_name="test"
        )

        assert result.project_path is None
        assert result.agent_runs == []
        assert result.errors == []
        assert result.created_at is not None
        assert result.duration_seconds is None
        assert result.git_repo_url is None

    def test_project_result_with_git_url(self):
        """Test ProjectResult with git repository URL"""
        result = ProjectResult(
            success=True,
            project_name="test",
            git_repo_url="https://github.com/user/repo"
        )

        assert result.git_repo_url == "https://github.com/user/repo"


class TestModelSerialization:
    """Test model serialization and deserialization"""

    def test_idea_round_trip(self):
        """Test Idea serialization round trip"""
        original = Idea(
            description="Test",
            target_users=["user1"],
            features=["feature1"]
        )
        data = original.model_dump()
        restored = Idea(**data)

        assert restored.description == original.description
        assert restored.target_users == original.target_users
        assert restored.features == original.features

    def test_project_spec_round_trip(self):
        """Test ProjectSpec serialization round trip"""
        original = ProjectSpec(
            name="test",
            description="Test spec",
            tech_stack={"lang": "python"},
            folder_structure={"src/": ["main.py"]},
            entry_point="main.py"
        )
        data = original.model_dump()
        restored = ProjectSpec(**data)

        assert restored.name == original.name
        assert restored.tech_stack == original.tech_stack

    def test_safety_check_round_trip(self):
        """Test SafetyCheck serialization round trip"""
        original = SafetyCheck(
            approved=True,
            warnings=["Warning 1"],
            required_confirmations=["Confirm 1"],
            blocked_keywords=[]
        )
        data = original.model_dump()
        restored = SafetyCheck(**data)

        assert restored.approved == original.approved
        assert restored.warnings == original.warnings

    def test_model_json_serialization(self):
        """Test models can be serialized to JSON"""
        idea = Idea(description="Test")
        json_str = idea.model_dump_json()

        assert isinstance(json_str, str)
        assert "Test" in json_str
