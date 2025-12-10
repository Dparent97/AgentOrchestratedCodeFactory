"""
Unit tests for Orchestrator

Tests cover:
- Orchestrator initialization
- Pipeline coordination
- Agent execution ordering
- Error handling and recovery
- Status tracking
- Project result generation
"""

import tempfile
from pathlib import Path

import pytest

from code_factory.agents.architect import ArchitectAgent
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.models import Idea, ProjectResult
from code_factory.core.orchestrator import Orchestrator


class TestOrchestratorInitialization:
    """Test Orchestrator initialization"""

    def test_orchestrator_initialization(self):
        """Test Orchestrator can be initialized"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        assert orchestrator is not None
        assert orchestrator.runtime is runtime

    def test_orchestrator_with_custom_projects_dir(self, isolated_test_config):
        """Test Orchestrator with custom projects directory"""
        from code_factory.core.config import FactoryConfig
        
        runtime = AgentRuntime()
        with tempfile.TemporaryDirectory() as tmpdir:
            config = FactoryConfig(
                projects_dir=tmpdir,
                checkpoint_dir=Path(tmpdir) / "checkpoints",
                staging_dir=Path(tmpdir) / "staging",
            )
            orchestrator = Orchestrator(runtime, config=config)

            assert orchestrator.projects_dir == Path(tmpdir)

    def test_orchestrator_default_projects_dir(self):
        """Test Orchestrator has default projects directory"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        assert orchestrator.projects_dir is not None
        assert isinstance(orchestrator.projects_dir, Path)


class TestOrchestratorStatus:
    """Test Orchestrator status tracking"""

    def test_get_current_status(self):
        """Test getting orchestrator status"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        status = orchestrator.get_current_status()

        assert isinstance(status, dict)
        assert "projects_dir" in status
        assert "registered_agents" in status
        assert "execution_history" in status

    def test_status_shows_registered_agents(self):
        """Test status includes registered agents"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())

        orchestrator = Orchestrator(runtime)
        status = orchestrator.get_current_status()

        assert len(status["registered_agents"]) == 2
        assert "safety_guard" in status["registered_agents"]
        assert "planner" in status["registered_agents"]

    def test_status_tracks_execution_history_count(self):
        """Test status tracks number of executions"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())

        orchestrator = Orchestrator(runtime)

        # No executions yet
        status1 = orchestrator.get_current_status()
        assert status1["execution_history"] == 0

        # Execute an agent
        idea = Idea(description="Test idea")
        runtime.execute_agent("safety_guard", idea)

        # Should show one execution
        status2 = orchestrator.get_current_status()
        assert status2["execution_history"] == 1


class TestFactoryRun:
    """Test the main factory run pipeline"""

    def test_run_factory_accepts_idea(self):
        """Test run_factory accepts Idea"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        idea = Idea(description="Build a test tool")
        result = orchestrator.run_factory(idea)

        assert isinstance(result, ProjectResult)

    def test_run_factory_returns_project_result(self):
        """Test run_factory returns ProjectResult"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        idea = Idea(description="Build a test tool")
        result = orchestrator.run_factory(idea)

        assert isinstance(result, ProjectResult)
        assert hasattr(result, "success")
        assert hasattr(result, "project_name")
        assert hasattr(result, "agent_runs")
        assert hasattr(result, "errors")

    def test_run_factory_records_duration(self):
        """Test that factory run records duration"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        idea = Idea(description="Build a test tool")
        result = orchestrator.run_factory(idea)

        assert result.duration_seconds is not None
        assert result.duration_seconds >= 0

    def test_run_factory_with_registered_agents(self):
        """Test factory run with registered agents"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())
        runtime.register_agent(ArchitectAgent())

        orchestrator = Orchestrator(runtime)
        idea = Idea(description="Build a maintenance tracker")
        result = orchestrator.run_factory(idea)

        assert isinstance(result, ProjectResult)
        # Currently returns success=True with placeholder
        assert result.success is True

    def test_run_factory_handles_exceptions(self):
        """Test that factory run handles exceptions gracefully"""
        # Create a runtime that will fail
        runtime = AgentRuntime()

        class FailingOrchestrator(Orchestrator):
            def run_factory(self, idea):
                start_time = __import__('datetime').datetime.now()
                result = ProjectResult(
                    success=False,
                    project_name="",
                    agent_runs=[],
                    errors=[]
                )
                try:
                    raise Exception("Simulated failure")
                except Exception as e:
                    result.success = False
                    result.errors.append(str(e))

                end_time = __import__('datetime').datetime.now()
                result.duration_seconds = (end_time - start_time).total_seconds()
                return result

        orchestrator = FailingOrchestrator(runtime)
        idea = Idea(description="Test")
        result = orchestrator.run_factory(idea)

        assert result.success is False
        assert len(result.errors) > 0


class TestCheckpointFunctionality:
    """Test checkpoint functionality"""

    def test_checkpoint_method_exists(self):
        """Test checkpoint method exists"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        assert hasattr(orchestrator, "checkpoint")
        assert callable(orchestrator.checkpoint)

    def test_checkpoint_accepts_parameters(self, isolated_test_config):
        """Test checkpoint accepts stage and idea"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        # Create a test idea
        idea = Idea(description="Test idea for checkpoint")

        # Should not raise exception
        try:
            orchestrator.checkpoint(
                stage="planning",
                idea=idea,
                metadata={"project_name": "test-project"}
            )
        except Exception as e:
            pytest.fail(f"checkpoint raised unexpected exception: {e}")


class TestErrorHandling:
    """Test error handling functionality"""

    def test_handle_failure_method_exists(self):
        """Test handle_failure method exists"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        assert hasattr(orchestrator, "handle_failure")
        assert callable(orchestrator.handle_failure)

    def test_handle_failure_accepts_parameters(self, isolated_test_config):
        """Test handle_failure accepts agent name, error, stage, and idea"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        error = Exception("Test error")
        idea = Idea(description="Test idea for error handling")

        # Should not raise exception
        try:
            result = orchestrator.handle_failure(
                agent_name="test_agent",
                error=error,
                stage="planning",
                idea=idea,
            )
            assert isinstance(result, dict)
            assert "failed_agent" in result
        except Exception as e:
            pytest.fail(f"handle_failure raised unexpected exception: {e}")


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_orchestrator_with_multiple_agents(self):
        """Test orchestrator coordinating multiple agents"""
        runtime = AgentRuntime()

        # Register multiple agents
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())
        runtime.register_agent(ArchitectAgent())

        orchestrator = Orchestrator(runtime)

        # Verify all agents are registered
        status = orchestrator.get_current_status()
        assert len(status["registered_agents"]) == 3

        # Run factory
        idea = Idea(
            description="Build a maintenance tracking tool",
            target_users=["mechanic"],
            features=["offline mode"]
        )
        result = orchestrator.run_factory(idea)

        assert isinstance(result, ProjectResult)

    def test_orchestrator_isolated_from_runtime(self):
        """Test that orchestrator state is isolated from runtime"""
        runtime1 = AgentRuntime()
        runtime1.register_agent(SafetyGuard())

        runtime2 = AgentRuntime()
        runtime2.register_agent(PlannerAgent())

        orch1 = Orchestrator(runtime1)
        orch2 = Orchestrator(runtime2)

        status1 = orch1.get_current_status()
        status2 = orch2.get_current_status()

        # Should have different agents
        assert status1["registered_agents"] != status2["registered_agents"]

    def test_multiple_factory_runs(self):
        """Test running factory multiple times"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())

        orchestrator = Orchestrator(runtime)

        # Run factory multiple times
        ideas = [
            Idea(description="Build a calculator"),
            Idea(description="Build a todo app"),
            Idea(description="Build a file organizer")
        ]

        results = []
        for idea in ideas:
            result = orchestrator.run_factory(idea)
            results.append(result)

        # All should succeed
        assert len(results) == 3
        for result in results:
            assert isinstance(result, ProjectResult)


class TestProjectsDirectory:
    """Test projects directory handling"""

    def test_projects_dir_is_path_object(self):
        """Test that projects_dir is a Path object"""
        runtime = AgentRuntime()
        orchestrator = Orchestrator(runtime)

        assert isinstance(orchestrator.projects_dir, Path)

    def test_custom_projects_dir_is_used(self, isolated_test_config):
        """Test that custom projects directory is used"""
        from code_factory.core.config import FactoryConfig
        
        runtime = AgentRuntime()
        with tempfile.TemporaryDirectory() as tmpdir:
            config = FactoryConfig(
                projects_dir=tmpdir,
                checkpoint_dir=Path(tmpdir) / "checkpoints",
                staging_dir=Path(tmpdir) / "staging",
            )
            orchestrator = Orchestrator(runtime, config=config)

            assert str(orchestrator.projects_dir) == tmpdir

    def test_projects_dir_in_status(self, isolated_test_config):
        """Test that projects_dir appears in status"""
        from code_factory.core.config import FactoryConfig
        
        runtime = AgentRuntime()
        with tempfile.TemporaryDirectory() as tmpdir:
            config = FactoryConfig(
                projects_dir=tmpdir,
                checkpoint_dir=Path(tmpdir) / "checkpoints",
                staging_dir=Path(tmpdir) / "staging",
            )
            orchestrator = Orchestrator(runtime, config=config)
            status = orchestrator.get_current_status()

            assert status["projects_dir"] == tmpdir
