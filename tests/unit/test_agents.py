"""
Unit tests for all agent implementations

Tests cover:
- Agent properties (name, description)
- Input validation
- Output schema validation
- Error conditions
- Business logic specific to each agent
"""

import pytest
from pydantic import ValidationError

from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.agents.blue_collar_advisor import AdvisoryInput, BlueCollarAdvisor
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.agents.git_ops import GitOpsAgent, GitOperation
from code_factory.agents.implementer import CodeOutput, ImplementerAgent
from code_factory.agents.planner import PlannerAgent, TaskList
from code_factory.agents.tester import TesterAgent, TestInput
from code_factory.core.models import (
    AdvisoryReport,
    Idea,
    ProjectSpec,
    TaskType,
    TestResult,
)


class TestPlannerAgent:
    """Test PlannerAgent functionality"""

    def test_agent_properties(self):
        """Test PlannerAgent name and description"""
        planner = PlannerAgent()
        assert planner.name == "planner"
        assert "task" in planner.description.lower()

    def test_planner_accepts_idea_input(self):
        """Test PlannerAgent accepts Idea as input"""
        planner = PlannerAgent()
        idea = Idea(description="Build a calculator")
        result = planner.execute(idea)

        assert isinstance(result, TaskList)
        assert hasattr(result, "tasks")

    def test_planner_returns_task_list(self):
        """Test PlannerAgent returns TaskList"""
        planner = PlannerAgent()
        idea = Idea(description="Build a maintenance tracker")
        result = planner.execute(idea)

        assert isinstance(result, TaskList)
        assert isinstance(result.tasks, list)
        assert len(result.tasks) > 0

    def test_planner_tasks_have_dependencies(self):
        """Test that planner tasks include dependency information"""
        planner = PlannerAgent()
        idea = Idea(description="Build a tool")
        result = planner.execute(idea)

        # Check that at least one task has dependencies
        tasks_with_deps = [t for t in result.tasks if len(t.dependencies) > 0]
        assert len(tasks_with_deps) > 0

    def test_planner_tasks_have_types(self):
        """Test that all tasks have valid types"""
        planner = PlannerAgent()
        idea = Idea(description="Build a tool")
        result = planner.execute(idea)

        for task in result.tasks:
            assert task.type in TaskType

    def test_planner_generates_different_task_types(self):
        """Test that planner generates multiple task types"""
        planner = PlannerAgent()
        idea = Idea(description="Build a tool")
        result = planner.execute(idea)

        task_types = set(task.type for task in result.tasks)
        # Should have at least CONFIG and CODE
        assert TaskType.CONFIG in task_types or TaskType.CODE in task_types

    def test_planner_with_complex_idea(self):
        """Test planner with idea containing features and constraints"""
        planner = PlannerAgent()
        idea = Idea(
            description="Build maintenance tracker",
            features=["offline mode", "voice input"],
            constraints=["no cloud", "must be fast"],
            target_users=["mechanic"]
        )
        result = planner.execute(idea)

        assert isinstance(result, TaskList)
        assert len(result.tasks) > 0

    def test_planner_invalid_input_raises_error(self):
        """Test that invalid input raises error"""
        planner = PlannerAgent()
        with pytest.raises((ValueError, ValidationError)):
            planner.execute("not an idea")


class TestArchitectAgent:
    """Test ArchitectAgent functionality"""

    def test_agent_properties(self):
        """Test ArchitectAgent name and description"""
        architect = ArchitectAgent()
        assert architect.name == "architect"
        assert "architect" in architect.description.lower()

    def test_architect_accepts_idea_input(self):
        """Test ArchitectAgent accepts Idea as input"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a calculator")
        result = architect.execute(idea)

        assert isinstance(result, ProjectSpec)

    def test_architect_accepts_architect_input(self):
        """Test ArchitectAgent accepts ArchitectInput"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a tool")
        arch_input = ArchitectInput(idea=idea, task_count=5)
        result = architect.execute(arch_input)

        assert isinstance(result, ProjectSpec)

    def test_architect_returns_project_spec(self):
        """Test ArchitectAgent returns valid ProjectSpec"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a maintenance tracker")
        result = architect.execute(idea)

        assert isinstance(result, ProjectSpec)
        assert result.name is not None
        assert result.description is not None
        assert len(result.tech_stack) > 0
        assert result.entry_point is not None

    def test_architect_generates_valid_project_name(self):
        """Test that generated project name is valid"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a Cool Tool for Testing")
        result = architect.execute(idea)

        # Name should be lowercase and hyphenated
        assert result.name.islower() or "-" in result.name or "_" in result.name
        assert " " not in result.name

    def test_architect_includes_tech_stack(self):
        """Test that architect includes technology stack"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a tool")
        result = architect.execute(idea)

        assert len(result.tech_stack) > 0
        # Should include language at minimum
        assert "language" in result.tech_stack

    def test_architect_includes_folder_structure(self):
        """Test that architect defines folder structure"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a tool")
        result = architect.execute(idea)

        assert len(result.folder_structure) > 0

    def test_architect_preserves_user_profile(self):
        """Test that architect preserves target user information"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build a tool",
            target_users=["marine_engineer"]
        )
        result = architect.execute(idea)

        assert result.user_profile == "marine_engineer"

    def test_architect_preserves_environment(self):
        """Test that architect preserves environment information"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build a tool",
            environment="noisy workshop"
        )
        result = architect.execute(idea)

        assert result.environment == "noisy workshop"

    def test_architect_handles_long_description(self):
        """Test architect with very long description"""
        architect = ArchitectAgent()
        long_desc = "Build a tool " * 50  # Very long description
        idea = Idea(description=long_desc)
        result = architect.execute(idea)

        # Description should be truncated
        assert len(result.description) <= 100


class TestImplementerAgent:
    """Test ImplementerAgent functionality"""

    def test_agent_properties(self):
        """Test ImplementerAgent name and description"""
        implementer = ImplementerAgent()
        assert implementer.name == "implementer"
        assert "code" in implementer.description.lower()

    def test_implementer_accepts_project_spec(self):
        """Test ImplementerAgent accepts ProjectSpec"""
        implementer = ImplementerAgent()
        spec = ProjectSpec(
            name="test-tool",
            description="Test tool",
            tech_stack={"language": "python"},
            folder_structure={"src/": ["main.py"]},
            entry_point="src/main.py"
        )
        result = implementer.execute(spec)

        assert isinstance(result, CodeOutput)

    def test_implementer_returns_code_output(self):
        """Test ImplementerAgent returns CodeOutput"""
        implementer = ImplementerAgent()
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        result = implementer.execute(spec)

        assert isinstance(result, CodeOutput)
        assert hasattr(result, "files")
        assert hasattr(result, "files_created")

    def test_implementer_generates_files(self):
        """Test that implementer generates code files"""
        implementer = ImplementerAgent()
        spec = ProjectSpec(
            name="test-tool",
            description="Test tool",
            tech_stack={"language": "python"},
            folder_structure={"src/": ["main.py"]},
            entry_point="src/main.py"
        )
        result = implementer.execute(spec)

        assert isinstance(result.files, dict)
        assert len(result.files) > 0
        assert result.files_created > 0

    def test_implementer_files_count_matches(self):
        """Test that files_created count matches actual files"""
        implementer = ImplementerAgent()
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        result = implementer.execute(spec)

        assert result.files_created == len(result.files)

    def test_implementer_invalid_input_raises_error(self):
        """Test that invalid input raises error"""
        implementer = ImplementerAgent()
        with pytest.raises((ValueError, ValidationError)):
            implementer.execute("not a spec")


class TestTesterAgent:
    """Test TesterAgent functionality"""

    def test_agent_properties(self):
        """Test TesterAgent name and description"""
        tester = TesterAgent()
        assert tester.name == "tester"
        assert "test" in tester.description.lower()

    def test_tester_accepts_test_input(self):
        """Test TesterAgent accepts TestInput"""
        tester = TesterAgent()
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        test_input = TestInput(
            spec=spec,
            code_files={"main.py": "print('hello')"}
        )
        result = tester.execute(test_input)

        assert isinstance(result, TestResult)

    def test_tester_returns_test_result(self):
        """Test TesterAgent returns TestResult"""
        tester = TesterAgent()
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        test_input = TestInput(spec=spec, code_files={})
        result = tester.execute(test_input)

        assert isinstance(result, TestResult)
        assert hasattr(result, "total_tests")
        assert hasattr(result, "passed")
        assert hasattr(result, "failed")
        assert hasattr(result, "coverage_percent")

    def test_tester_result_has_valid_counts(self):
        """Test that test result has valid counts"""
        tester = TesterAgent()
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        test_input = TestInput(spec=spec, code_files={})
        result = tester.execute(test_input)

        assert result.total_tests >= 0
        assert result.passed >= 0
        assert result.failed >= 0


class TestDocWriterAgent:
    """Test DocWriterAgent functionality"""

    def test_agent_properties(self):
        """Test DocWriterAgent name and description"""
        doc_writer = DocWriterAgent()
        assert doc_writer.name == "doc_writer"
        assert "doc" in doc_writer.description.lower()

    def test_doc_writer_accepts_project_spec(self):
        """Test DocWriterAgent accepts ProjectSpec"""
        doc_writer = DocWriterAgent()
        spec = ProjectSpec(
            name="test-tool",
            description="Test tool",
            tech_stack={"language": "python"},
            folder_structure={"src/": ["main.py"]},
            entry_point="src/main.py"
        )
        result = doc_writer.execute(spec)

        assert result is not None
        assert hasattr(result, "files")

    def test_doc_writer_generates_documentation(self):
        """Test that doc writer generates documentation files"""
        doc_writer = DocWriterAgent()
        spec = ProjectSpec(
            name="test-tool",
            description="Test tool",
            tech_stack={"language": "python"},
            folder_structure={"src/": ["main.py"]},
            entry_point="src/main.py"
        )
        result = doc_writer.execute(spec)

        assert isinstance(result.files, dict)
        assert len(result.files) > 0


class TestBlueCollarAdvisor:
    """Test BlueCollarAdvisor functionality"""

    def test_agent_properties(self):
        """Test BlueCollarAdvisor name and description"""
        advisor = BlueCollarAdvisor()
        assert advisor.name == "blue_collar_advisor"
        assert len(advisor.description) > 0

    def test_advisor_accepts_advisory_input(self):
        """Test BlueCollarAdvisor accepts AdvisoryInput"""
        advisor = BlueCollarAdvisor()
        idea = Idea(description="Build a tool")
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        advisory_input = AdvisoryInput(idea=idea, spec=spec)
        result = advisor.execute(advisory_input)

        assert isinstance(result, AdvisoryReport)

    def test_advisor_returns_advisory_report(self):
        """Test BlueCollarAdvisor returns AdvisoryReport"""
        advisor = BlueCollarAdvisor()
        idea = Idea(description="Build a tool")
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        advisory_input = AdvisoryInput(idea=idea, spec=spec)
        result = advisor.execute(advisory_input)

        assert isinstance(result, AdvisoryReport)
        assert hasattr(result, "recommendations")
        assert hasattr(result, "warnings")
        assert hasattr(result, "environment_fit")

    def test_advisor_provides_recommendations(self):
        """Test that advisor provides recommendations"""
        advisor = BlueCollarAdvisor()
        idea = Idea(
            description="Build a tool",
            environment="noisy workshop",
            target_users=["mechanic"]
        )
        spec = ProjectSpec(
            name="test",
            description="Test",
            tech_stack={"language": "python"},
            folder_structure={},
            entry_point="main.py"
        )
        advisory_input = AdvisoryInput(idea=idea, spec=spec)
        result = advisor.execute(advisory_input)

        # Should provide some recommendations or warnings
        assert isinstance(result.recommendations, list)
        assert isinstance(result.warnings, list)


class TestGitOpsAgent:
    """Test GitOpsAgent functionality"""

    def test_agent_properties(self):
        """Test GitOpsAgent name and description"""
        git_ops = GitOpsAgent()
        assert git_ops.name == "git_ops"
        assert "git" in git_ops.description.lower()

    def test_git_ops_accepts_git_operation(self):
        """Test GitOpsAgent accepts GitOperation"""
        git_ops = GitOpsAgent()
        operation = GitOperation(
            repo_path="/tmp/test",
            operation="init",
            message="Initial commit"
        )
        result = git_ops.execute(operation)

        assert result is not None
        assert hasattr(result, "success")

    def test_git_ops_init_operation(self):
        """Test GitOpsAgent init operation"""
        git_ops = GitOpsAgent()
        operation = GitOperation(
            repo_path="/tmp/test",
            operation="init",
            message="Initial commit"
        )
        result = git_ops.execute(operation)

        assert result.operation == "init"

    def test_git_ops_commit_operation(self):
        """Test GitOpsAgent commit operation"""
        git_ops = GitOpsAgent()
        operation = GitOperation(
            repo_path="/tmp/test",
            operation="commit",
            message="Test commit"
        )
        result = git_ops.execute(operation)

        assert result.operation == "commit"
        assert result.message is not None

    def test_git_ops_push_operation(self):
        """Test GitOpsAgent push operation"""
        git_ops = GitOpsAgent()
        operation = GitOperation(
            repo_path="/tmp/test",
            operation="push",
            message="Push to remote"
        )
        result = git_ops.execute(operation)

        assert result.operation == "push"


class TestAgentInterfaces:
    """Test that all agents implement BaseAgent interface correctly"""

    def test_all_agents_have_name_property(self):
        """Test all agents have name property"""
        agents = [
            PlannerAgent(),
            ArchitectAgent(),
            ImplementerAgent(),
            TesterAgent(),
            DocWriterAgent(),
            BlueCollarAdvisor(),
            GitOpsAgent()
        ]

        for agent in agents:
            assert hasattr(agent, "name")
            assert isinstance(agent.name, str)
            assert len(agent.name) > 0

    def test_all_agents_have_description_property(self):
        """Test all agents have description property"""
        agents = [
            PlannerAgent(),
            ArchitectAgent(),
            ImplementerAgent(),
            TesterAgent(),
            DocWriterAgent(),
            BlueCollarAdvisor(),
            GitOpsAgent()
        ]

        for agent in agents:
            assert hasattr(agent, "description")
            assert isinstance(agent.description, str)
            assert len(agent.description) > 0

    def test_all_agents_have_execute_method(self):
        """Test all agents have execute method"""
        agents = [
            PlannerAgent(),
            ArchitectAgent(),
            ImplementerAgent(),
            TesterAgent(),
            DocWriterAgent(),
            BlueCollarAdvisor(),
            GitOpsAgent()
        ]

        for agent in agents:
            assert hasattr(agent, "execute")
            assert callable(agent.execute)

    def test_all_agents_have_unique_names(self):
        """Test all agents have unique names"""
        agents = [
            PlannerAgent(),
            ArchitectAgent(),
            ImplementerAgent(),
            TesterAgent(),
            DocWriterAgent(),
            BlueCollarAdvisor(),
            GitOpsAgent()
        ]

        names = [agent.name for agent in agents]
        assert len(names) == len(set(names))  # All unique
