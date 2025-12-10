"""
End-to-end tests for complete factory runs

Tests cover:
- Complete factory pipeline execution
- Real-world scenarios with all agents
- Generated project validation
- File system interactions
- Error scenarios and recovery
"""

import tempfile
from pathlib import Path

import pytest

from code_factory.agents.architect import ArchitectAgent
from code_factory.agents.blue_collar_advisor import BlueCollarAdvisor
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.agents.git_ops import GitOpsAgent
from code_factory.agents.implementer import ImplementerAgent
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.tester import TesterAgent
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.config import FactoryConfig
from code_factory.core.models import Idea
from code_factory.core.orchestrator import Orchestrator


def setup_full_runtime():
    """Set up a complete runtime with all agents"""
    runtime = AgentRuntime()
    runtime.register_agent(SafetyGuard())
    runtime.register_agent(PlannerAgent())
    runtime.register_agent(ArchitectAgent())
    runtime.register_agent(BlueCollarAdvisor())
    runtime.register_agent(ImplementerAgent())
    runtime.register_agent(TesterAgent())
    runtime.register_agent(DocWriterAgent())
    runtime.register_agent(GitOpsAgent())
    return runtime


def create_orchestrator_with_tmpdir(runtime, tmpdir):
    """Create an Orchestrator with temporary directory config"""
    config = FactoryConfig(
        projects_dir=Path(tmpdir) / "projects",
        checkpoint_dir=Path(tmpdir) / "checkpoints",
        staging_dir=Path(tmpdir) / "staging",
    )
    config.ensure_directories()
    return Orchestrator(runtime, config=config)


class TestCompleteFactoryRun:
    """Test complete factory runs from idea to project"""

    def test_simple_idea_to_project(self, isolated_test_config):
        """Test transforming simple idea into project"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(description="Build a simple calculator tool")
            result = orchestrator.run_factory(idea)

            assert result is not None
            assert hasattr(result, "success")
            assert hasattr(result, "project_name")
            assert result.duration_seconds is not None

    def test_complex_idea_with_features(self, isolated_test_config):
        """Test complex idea with features and constraints"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(
                description="Build a maintenance tracking tool for marine engineers",
                target_users=["marine_engineer", "mechanic"],
                environment="noisy engine room, limited WiFi",
                features=[
                    "offline mode",
                    "voice commands",
                    "timestamp all entries",
                    "export to CSV"
                ],
                constraints=[
                    "no cloud dependencies",
                    "must work on old hardware",
                    "large buttons for gloves"
                ]
            )
            result = orchestrator.run_factory(idea)

            assert result is not None
            assert result.project_name != ""

    def test_multiple_sequential_runs(self, isolated_test_config):
        """Test running factory multiple times sequentially"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            ideas = [
                Idea(description="Build a todo list app"),
                Idea(description="Build a note-taking tool"),
                Idea(description="Build a file organizer")
            ]

            results = []
            for idea in ideas:
                result = orchestrator.run_factory(idea)
                results.append(result)

            assert len(results) == 3
            for result in results:
                assert result is not None


class TestRealWorldScenarios:
    """Test real-world usage scenarios"""

    def test_field_worker_tool_idea(self, isolated_test_config):
        """Test building tool for field worker"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(
                description="Quick inspection checklist for ship machinery",
                target_users=["marine_engineer"],
                environment="noisy, vibrating, poor lighting",
                features=[
                    "checklist templates",
                    "photo attachments",
                    "offline sync"
                ]
            )
            result = orchestrator.run_factory(idea)

            assert result is not None

    def test_simple_utility_tool_idea(self, isolated_test_config):
        """Test building simple utility tool"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(
                description="Convert between different units of measurement"
            )
            result = orchestrator.run_factory(idea)

            assert result is not None

    def test_data_processing_tool_idea(self, isolated_test_config):
        """Test building data processing tool"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(
                description="Parse maintenance logs and generate summary reports",
                features=[
                    "read CSV files",
                    "generate PDF reports",
                    "chart generation"
                ]
            )
            result = orchestrator.run_factory(idea)

            assert result is not None


class TestDangerousIdeaRejection:
    """Test that dangerous ideas are properly rejected"""

    def test_dangerous_idea_rejected_early(self, isolated_test_config):
        """Test that dangerous ideas are rejected at safety stage"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            dangerous_idea = Idea(
                description="Tool to hack into ship control systems"
            )

            # Safety check should fail
            safety_result = runtime.execute_agent("safety_guard", dangerous_idea)
            assert safety_result.output_data["approved"] is False
            assert len(safety_result.output_data["blocked_keywords"]) > 0

    def test_multiple_dangerous_keywords(self):
        """Test rejection of idea with multiple dangerous keywords"""
        runtime = setup_full_runtime()

        dangerous_idea = Idea(
            description="Hack systems and inject malware to bypass interlock"
        )

        safety_result = runtime.execute_agent("safety_guard", dangerous_idea)
        assert safety_result.output_data["approved"] is False
        assert len(safety_result.output_data["blocked_keywords"]) >= 3


class TestConfirmationRequired:
    """Test ideas requiring human confirmation"""

    def test_network_operation_requires_confirmation(self):
        """Test that network operations require confirmation"""
        runtime = setup_full_runtime()

        idea = Idea(
            description="Tool to send email notifications and make network call to API"
        )

        safety_result = runtime.execute_agent("safety_guard", idea)

        # Should be approved but with confirmations
        assert safety_result.output_data["approved"] is True
        assert len(safety_result.output_data["required_confirmations"]) > 0

    def test_file_deletion_requires_confirmation(self):
        """Test that file deletion requires confirmation"""
        runtime = setup_full_runtime()

        idea = Idea(
            description="Cleanup tool to delete file backups automatically"
        )

        safety_result = runtime.execute_agent("safety_guard", idea)

        assert safety_result.output_data["approved"] is True
        assert len(safety_result.output_data["required_confirmations"]) > 0


class TestExecutionHistory:
    """Test execution history tracking during factory runs"""

    def test_execution_history_recorded(self, isolated_test_config):
        """Test that execution history is recorded"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(description="Build a calculator")

            # Run some agents manually to track history
            runtime.execute_agent("safety_guard", idea)
            runtime.execute_agent("planner", idea)

            history = runtime.get_execution_history()
            assert len(history) == 2

    def test_history_includes_timing(self):
        """Test that history includes timing information"""
        runtime = setup_full_runtime()

        idea = Idea(description="Build a tool")
        runtime.execute_agent("safety_guard", idea)

        history = runtime.get_execution_history()
        assert len(history) > 0

        for record in history:
            assert record.started_at is not None
            assert record.completed_at is not None
            assert record.duration_seconds is not None
            assert record.duration_seconds >= 0

    def test_history_tracks_success_and_failure(self):
        """Test that history tracks both success and failure"""
        from code_factory.core.agent_runtime import BaseAgent, AgentExecutionError
        from pydantic import BaseModel

        class TestFailAgent(BaseAgent):
            @property
            def name(self):
                return "test_fail"

            @property
            def description(self):
                return "Test"

            def execute(self, input_data):
                raise AgentExecutionError("Test failure")

        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(TestFailAgent())

        idea = Idea(description="Test")

        # Execute success
        runtime.execute_agent("safety_guard", idea)

        # Execute failure
        runtime.execute_agent("test_fail", idea)

        history = runtime.get_execution_history()
        assert len(history) == 2
        assert history[0].status == "success"
        assert history[1].status == "failed"


class TestProjectValidation:
    """Test validation of generated projects"""

    def test_project_result_structure(self, isolated_test_config):
        """Test that project result has expected structure"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(description="Build a simple tool")
            result = orchestrator.run_factory(idea)

            # Validate structure
            assert hasattr(result, "success")
            assert hasattr(result, "project_name")
            assert hasattr(result, "project_path")
            assert hasattr(result, "agent_runs")
            assert hasattr(result, "errors")
            assert hasattr(result, "created_at")
            assert hasattr(result, "duration_seconds")

    def test_project_name_is_valid(self, isolated_test_config):
        """Test that generated project name is valid"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(description="Build a Test Tool")
            result = orchestrator.run_factory(idea)

            # Project name should be valid (lowercase, no spaces)
            assert result.project_name != ""
            if result.project_name != "placeholder":  # Skip placeholder check
                assert " " not in result.project_name


class TestErrorRecovery:
    """Test error recovery scenarios"""

    def test_orchestrator_handles_errors_gracefully(self, isolated_test_config):
        """Test that orchestrator handles errors gracefully"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            # This should not crash
            idea = Idea(description="Build a tool")
            result = orchestrator.run_factory(idea)

            assert result is not None
            assert isinstance(result.errors, list)


class TestOrchestratorStatus:
    """Test orchestrator status during execution"""

    def test_status_before_run(self, isolated_test_config):
        """Test orchestrator status before any runs"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            status = orchestrator.get_current_status()

            assert "projects_dir" in status
            assert "registered_agents" in status
            assert "execution_history" in status
            assert len(status["registered_agents"]) == 8  # All 8 agents

    def test_status_after_run(self, isolated_test_config):
        """Test orchestrator status after run"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            # Execute some agents
            idea = Idea(description="Build a tool")
            runtime.execute_agent("safety_guard", idea)
            runtime.execute_agent("planner", idea)

            status = orchestrator.get_current_status()
            assert status["execution_history"] == 2


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_minimal_idea(self, isolated_test_config):
        """Test with minimal idea (just description)"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(description="Simple tool")
            result = orchestrator.run_factory(idea)

            assert result is not None

    def test_idea_with_empty_lists(self, isolated_test_config):
        """Test idea with empty lists"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(
                description="Tool",
                target_users=[],
                features=[],
                constraints=[]
            )
            result = orchestrator.run_factory(idea)

            assert result is not None

    def test_very_long_description(self, isolated_test_config):
        """Test with very long description"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            long_description = "Build a " + "comprehensive " * 100 + "tool"
            idea = Idea(description=long_description)
            result = orchestrator.run_factory(idea)

            assert result is not None

    def test_special_characters_in_description(self, isolated_test_config):
        """Test with special characters in description"""
        runtime = setup_full_runtime()

        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = create_orchestrator_with_tmpdir(runtime, tmpdir)

            idea = Idea(description="Build a tool with @#$% special chars!")
            result = orchestrator.run_factory(idea)

            assert result is not None


class TestAgentInteraction:
    """Test interactions between agents during E2E flow"""

    def test_all_agents_can_execute(self):
        """Test that all agents can execute successfully"""
        runtime = setup_full_runtime()

        idea = Idea(description="Build a test tool")

        # Test each agent independently
        safety_result = runtime.execute_agent("safety_guard", idea)
        assert safety_result.status == "success"

        planner_result = runtime.execute_agent("planner", idea)
        assert planner_result.status == "success"

        architect_result = runtime.execute_agent("architect", idea)
        assert architect_result.status == "success"

    def test_agent_outputs_are_consumable(self):
        """Test that agent outputs can be consumed by next agent"""
        runtime = setup_full_runtime()

        from code_factory.agents.architect import ArchitectInput
        from code_factory.agents.blue_collar_advisor import AdvisoryInput
        from code_factory.core.models import ProjectSpec

        idea = Idea(description="Build a tool")

        # Get outputs from each stage
        planner_result = runtime.execute_agent("planner", idea)
        task_count = len(planner_result.output_data["tasks"])

        arch_input = ArchitectInput(idea=idea, task_count=task_count)
        architect_result = runtime.execute_agent("architect", arch_input)

        spec = ProjectSpec(**architect_result.output_data["spec"])

        # Each output should be consumable
        assert task_count > 0
        assert spec is not None
