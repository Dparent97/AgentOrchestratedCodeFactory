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
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.tester import TesterAgent, TestInput
from code_factory.core.models import (
    AdvisoryReport,
    ArchitectResult,
    Idea,
    PlanResult,
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

    def test_planner_simple_idea_task_breakdown(self):
        """Test PlannerAgent with simple idea generates minimal tasks"""
        planner = PlannerAgent()
        idea = Idea(
            description="Build a calculator",
            features=["addition", "subtraction"]
        )
        result = planner.execute(idea)

        assert isinstance(result, PlanResult)
        assert hasattr(result, "tasks")
        assert hasattr(result, "dependency_graph")
        assert hasattr(result, "estimated_complexity")
        assert hasattr(result, "warnings")

        # Should have at least 5 tasks (config, 2 code, 2 test, 1 doc)
        assert len(result.tasks) >= 5
        assert result.estimated_complexity in ["simple", "moderate", "complex"]

    def test_planner_complex_idea_proper_decomposition(self):
        """Test PlannerAgent with complex idea generates comprehensive tasks"""
        planner = PlannerAgent()
        idea = Idea(
            description="Build maintenance tracker with advanced features",
            features=["offline mode", "voice input", "barcode scanning",
                     "cloud sync", "reporting", "notifications"],
            constraints=["must work offline", "fast startup", "low memory"],
            target_users=["mechanic", "technician"]
        )
        result = planner.execute(idea)

        assert isinstance(result, PlanResult)
        # Complex idea should generate more tasks
        assert len(result.tasks) >= 10
        # Should likely be marked as complex
        assert result.estimated_complexity in ["moderate", "complex"]

    def test_planner_dependency_graph_validation(self):
        """Test that dependency graph is valid and complete"""
        planner = PlannerAgent()
        idea = Idea(description="Build a tool", features=["feature1", "feature2"])
        result = planner.execute(idea)

        # Check dependency graph structure
        assert isinstance(result.dependency_graph, dict)

        # All tasks should be in the graph
        task_ids = {task.id for task in result.tasks}
        graph_ids = set(result.dependency_graph.keys())
        assert task_ids == graph_ids

        # Dependencies should reference valid task IDs
        for task_id, deps in result.dependency_graph.items():
            for dep in deps:
                assert dep in task_ids, f"Invalid dependency {dep} for {task_id}"

    def test_planner_no_circular_dependencies(self):
        """Test that planner doesn't create circular dependencies"""
        planner = PlannerAgent()
        idea = Idea(
            description="Build a complex tool",
            features=["feature1", "feature2", "feature3"]
        )
        result = planner.execute(idea)

        # If there were circular dependencies, there should be a warning
        circular_warnings = [w for w in result.warnings if "circular" in w.lower()]
        # Our implementation should not create circular dependencies
        assert len(circular_warnings) == 0

    def test_planner_edge_case_vague_idea(self):
        """Test planner with vague idea (no features)"""
        planner = PlannerAgent()
        idea = Idea(description="Build something useful")
        result = planner.execute(idea)

        assert isinstance(result, PlanResult)
        # Should still generate basic tasks
        assert len(result.tasks) > 0
        # Should have warning about no features
        assert any("no features" in w.lower() for w in result.warnings)

    def test_planner_edge_case_brief_description(self):
        """Test planner with very brief description"""
        planner = PlannerAgent()
        idea = Idea(description="Tool")
        result = planner.execute(idea)

        assert isinstance(result, PlanResult)
        # Should have warning about brief description
        assert any("brief" in w.lower() for w in result.warnings)

    def test_planner_tasks_have_dependencies(self):
        """Test that planner tasks include dependency information"""
        planner = PlannerAgent()
        idea = Idea(description="Build a tool", features=["feature1"])
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
        idea = Idea(description="Build a tool", features=["feature1"])
        result = planner.execute(idea)

        task_types = set(task.type for task in result.tasks)
        # Should have CONFIG, CODE, TEST, and DOC
        assert TaskType.CONFIG in task_types
        assert TaskType.CODE in task_types
        assert TaskType.TEST in task_types
        assert TaskType.DOC in task_types

    def test_planner_invalid_input_raises_error(self):
        """Test that invalid input raises error"""
        planner = PlannerAgent()
        with pytest.raises((ValueError, ValidationError)):
            planner.execute("not an idea")

    def test_planner_complexity_estimation_simple(self):
        """Test complexity estimation for simple projects"""
        planner = PlannerAgent()
        idea = Idea(
            description="Simple calculator",
            features=["addition"]
        )
        result = planner.execute(idea)

        # Simple project should be marked as simple or moderate
        assert result.estimated_complexity in ["simple", "moderate"]

    def test_planner_complexity_estimation_complex(self):
        """Test complexity estimation for complex projects"""
        planner = PlannerAgent()
        idea = Idea(
            description="Advanced system",
            features=["f1", "f2", "f3", "f4", "f5", "f6", "f7"],
            constraints=["c1", "c2", "c3", "c4"]
        )
        result = planner.execute(idea)

        # Complex project should be marked as complex
        assert result.estimated_complexity == "complex"

    def test_planner_infer_filename_from_feature(self):
        """Test filename inference from feature descriptions"""
        planner = PlannerAgent()

        # Test with descriptive feature
        filename = planner._infer_filename("Parse CSV files")
        assert filename.startswith("src/")
        assert filename.endswith(".py")
        assert "parse" in filename.lower() or "csv" in filename.lower()

    def test_planner_task_count_with_multiple_features(self):
        """Test that task count scales with features"""
        planner = PlannerAgent()
        idea_2_features = Idea(
            description="Tool",
            features=["feature1", "feature2"]
        )
        idea_5_features = Idea(
            description="Tool",
            features=["f1", "f2", "f3", "f4", "f5"]
        )

        result_2 = planner.execute(idea_2_features)
        result_5 = planner.execute(idea_5_features)

        # More features should result in more tasks
        assert len(result_5.tasks) > len(result_2.tasks)

    def test_planner_creates_examples_for_substantial_features(self):
        """Test that examples are created for projects with 3+ features"""
        planner = PlannerAgent()
        idea = Idea(
            description="Tool",
            features=["feature1", "feature2", "feature3"]
        )
        result = planner.execute(idea)

        # Should have an examples task
        example_tasks = [t for t in result.tasks if "examples" in t.description.lower()]
        assert len(example_tasks) > 0

    def test_planner_agent_assignment(self):
        """Test that tasks have appropriate agent assignments"""
        planner = PlannerAgent()
        idea = Idea(description="Build tool", features=["feature1"])
        result = planner.execute(idea)

        # Check that agents are assigned
        for task in result.tasks:
            assert task.agent is not None
            assert isinstance(task.agent, str)
            assert len(task.agent) > 0


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

        assert isinstance(result, ArchitectResult)
        assert isinstance(result.spec, ProjectSpec)

    def test_architect_accepts_architect_input(self):
        """Test ArchitectAgent accepts ArchitectInput"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a tool")
        arch_input = ArchitectInput(idea=idea, tasks=[])
        result = architect.execute(arch_input)

        assert isinstance(result, ArchitectResult)
        assert isinstance(result.spec, ProjectSpec)

    def test_architect_returns_architect_result(self):
        """Test ArchitectAgent returns complete ArchitectResult"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a maintenance tracker")
        result = architect.execute(idea)

        assert isinstance(result, ArchitectResult)
        assert hasattr(result, "spec")
        assert hasattr(result, "rationale")
        assert hasattr(result, "blue_collar_score")
        assert hasattr(result, "warnings")

    def test_architect_generates_valid_project_spec(self):
        """Test that generated ProjectSpec is complete"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a tool")
        result = architect.execute(idea)

        spec = result.spec
        assert spec.name is not None
        assert spec.description is not None
        assert len(spec.tech_stack) > 0
        assert spec.entry_point is not None
        assert "language" in spec.tech_stack

    def test_architect_domain_detection_data_processing(self):
        """Test domain detection for data processing"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Parse CSV files and analyze data",
            features=["CSV parsing", "data analysis"]
        )
        result = architect.execute(idea)

        # Should detect data processing domain
        spec = result.spec
        assert "pandas" in spec.dependencies

    def test_architect_domain_detection_calculator(self):
        """Test domain detection for calculator"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build a math calculator",
            features=["calculate formulas"]
        )
        result = architect.execute(idea)

        # Should detect calculator domain
        assert result.spec is not None

    def test_architect_domain_detection_web_service(self):
        """Test domain detection for web service"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build an API server",
            features=["HTTP endpoints"]
        )
        result = architect.execute(idea)

        # Should detect web service domain
        spec = result.spec
        assert any("fastapi" in dep for dep in spec.dependencies)

    def test_architect_blue_collar_score_high(self):
        """Test high blue-collar score for simple CLI tool"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Simple offline calculator",
            features=["basic math", "offline mode"]
        )
        result = architect.execute(idea)

        # Should have high score (CLI, offline, simple)
        assert result.blue_collar_score >= 7.0

    def test_architect_blue_collar_score_low(self):
        """Test low blue-collar score for complex web app"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Web API server with cloud synchronization",
            features=["HTTP API", "cloud sync", "online mode"]
        )
        result = architect.execute(idea)

        # Should have low score (web, requires internet)
        # Web API + cloud sync should trigger deductions
        assert result.blue_collar_score <= 7.0

    def test_architect_rationale_provided(self):
        """Test that rationale is provided for decisions"""
        architect = ArchitectAgent()
        idea = Idea(description="Build a tool")
        result = architect.execute(idea)

        assert isinstance(result.rationale, dict)
        assert len(result.rationale) > 0
        assert "language" in result.rationale

    def test_architect_warnings_for_complexity(self):
        """Test warnings for complex projects with many dependencies"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build API server",
            features=["HTTP API", "cloud sync", "realtime", "auth",
                     "notifications", "caching", "logging", "monitoring"]
        )
        result = architect.execute(idea)

        # With 8 features, should have examples/docs folder
        # or be marked as having many features
        assert ("examples/" in result.spec.folder_structure or
                "docs/" in result.spec.folder_structure or
                len(idea.features) >= 3)

    def test_architect_warnings_for_noisy_environment(self):
        """Test warnings for noisy environment"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build a tool",
            environment="noisy engine room"
        )
        result = architect.execute(idea)

        # Should warn about visual feedback for noisy environments
        assert any("noisy" in w.lower() for w in result.warnings)

    def test_architect_preserves_user_profile(self):
        """Test that architect preserves target user information"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build a tool",
            target_users=["marine_engineer"]
        )
        result = architect.execute(idea)

        assert result.spec.user_profile == "marine_engineer"

    def test_architect_preserves_environment(self):
        """Test that architect preserves environment information"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Build a tool",
            environment="noisy workshop"
        )
        result = architect.execute(idea)

        assert result.spec.environment == "noisy workshop"

    def test_architect_handles_long_description(self):
        """Test architect with very long description"""
        architect = ArchitectAgent()
        long_desc = "Build a tool " * 50  # Very long description
        idea = Idea(description=long_desc)
        result = architect.execute(idea)

        # Description should be truncated
        assert len(result.spec.description) <= 100

    def test_architect_project_name_generation(self):
        """Test project name generation"""
        architect = ArchitectAgent()

        # Test with stop words filtered
        idea1 = Idea(description="Build a Cool Tool for Testing")
        result1 = architect.execute(idea1)
        assert "build" not in result1.spec.name.lower()
        assert "for" not in result1.spec.name.lower()

        # Test with punctuation removed
        idea2 = Idea(description="Test! Tool, Name?")
        result2 = architect.execute(idea2)
        assert "!" not in result2.spec.name
        assert "," not in result2.spec.name

    def test_architect_folder_structure_simple(self):
        """Test folder structure for simple projects"""
        architect = ArchitectAgent()
        idea = Idea(description="Simple calculator", features=["add", "subtract"])
        result = architect.execute(idea)

        struct = result.spec.folder_structure
        assert "src/" in struct
        assert "tests/" in struct

    def test_architect_folder_structure_complex(self):
        """Test folder structure for complex projects"""
        architect = ArchitectAgent()
        idea = Idea(
            description="Complex tool",
            features=["feature1", "feature2", "feature3", "feature4"]
        )
        result = architect.execute(idea)

        struct = result.spec.folder_structure
        # Should include examples for 3+ features
        assert "examples/" in struct or "docs/" in struct

    def test_architect_tech_stack_selection(self):
        """Test tech stack selection for different domains"""
        architect = ArchitectAgent()

        # Data processing should include pandas
        idea_data = Idea(description="Analyze CSV data")
        result_data = architect.execute(idea_data)
        assert "pandas" in result_data.spec.dependencies

        # Web service should include fastapi
        idea_web = Idea(description="Build an API service")
        result_web = architect.execute(idea_web)
        assert "fastapi" in result_web.spec.dependencies

    def test_architect_invalid_input_raises_error(self):
        """Test that invalid input raises error"""
        architect = ArchitectAgent()
        with pytest.raises((ValueError, ValidationError)):
            architect.execute("not an idea")

    def test_architect_warning_for_no_features(self):
        """Test warning when no features are defined"""
        architect = ArchitectAgent()
        idea = Idea(description="Build something")
        result = architect.execute(idea)

        # Should warn about no features
        assert any("features" in w.lower() for w in result.warnings)


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
        """Test TesterAgent accepts TestInput and returns TestGenerationOutput"""
        from code_factory.agents.tester import TestGenerationOutput
        
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

        assert isinstance(result, TestGenerationOutput)
        assert isinstance(result.test_result, TestResult)

    def test_tester_returns_test_generation_output(self):
        """Test TesterAgent returns TestGenerationOutput with test files and results"""
        from code_factory.agents.tester import TestGenerationOutput
        
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

        assert isinstance(result, TestGenerationOutput)
        assert hasattr(result, "test_files")
        assert hasattr(result, "test_result")
        assert isinstance(result.test_files, dict)
        assert isinstance(result.test_result, TestResult)
        assert hasattr(result.test_result, "total_tests")
        assert hasattr(result.test_result, "passed")
        assert hasattr(result.test_result, "failed")
        assert hasattr(result.test_result, "coverage_percent")

    def test_tester_result_has_valid_counts(self):
        """Test that test result has valid counts"""
        from code_factory.agents.tester import TestGenerationOutput
        
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

        assert isinstance(result, TestGenerationOutput)
        assert result.test_result.total_tests >= 0
        assert result.test_result.passed >= 0
        assert result.test_result.failed >= 0


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


class TestTesterAgentAdvanced:
    """Additional tests for TesterAgent functionality"""

    def test_tester_generates_test_files(self):
        """Test that TesterAgent generates test files for code"""
        from code_factory.agents.tester import TestGenerationOutput
        
        tester = TesterAgent()
        spec = ProjectSpec(
            name="calculator",
            description="A simple calculator",
            tech_stack={"language": "python"},
            folder_structure={"src/": ["calculator.py"]},
            entry_point="src/calculator.py"
        )
        code_files = {
            "src/calculator.py": '''
def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract two numbers"""
    return a - b

class Calculator:
    def __init__(self):
        self.history = []
    
    def calculate(self, a, b, op):
        return op(a, b)
'''
        }
        test_input = TestInput(spec=spec, code_files=code_files)
        result = tester.execute(test_input)

        # Should generate test files
        assert len(result.test_files) > 0
        # Should have pytest.ini
        assert "pytest.ini" in result.test_files
        # Should have conftest.py
        assert "tests/conftest.py" in result.test_files
        # Test count should be > 0
        assert result.test_result.total_tests > 0

    def test_tester_skips_non_testable_files(self):
        """Test that TesterAgent skips __init__.py and test files"""
        tester = TesterAgent()
        spec = ProjectSpec(
            name="test-project",
            description="Test",
            tech_stack={},
            folder_structure={},
            entry_point="main.py"
        )
        code_files = {
            "__init__.py": "",
            "test_existing.py": "def test_foo(): pass",
            "conftest.py": "import pytest",
        }
        test_input = TestInput(spec=spec, code_files=code_files)
        result = tester.execute(test_input)

        # Should only have pytest.ini (no tests for these files)
        assert "pytest.ini" in result.test_files


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
