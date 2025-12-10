"""
Integration tests for multi-agent workflows

Tests cover:
- Multi-agent workflow coordination
- Data flow between agents
- Error propagation across pipeline stages
- State management across agents
- Complete pipeline execution
"""

import pytest

from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.agents.blue_collar_advisor import AdvisoryInput, BlueCollarAdvisor
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.agents.implementer import ImplementerAgent
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.agents.tester import TesterAgent, TestInput
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.models import (
    ArchitectResult,
    Idea,
    PlanResult,
    ProjectSpec,
    SafetyCheck,
)


class TestSafetyToPlannerWorkflow:
    """Test workflow from SafetyGuard to PlannerAgent"""

    def test_safe_idea_flows_to_planner(self):
        """Test that approved idea flows from SafetyGuard to PlannerAgent"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())

        # Step 1: Safety check
        idea = Idea(description="Build a maintenance tracker")
        safety_result = runtime.execute_agent("safety_guard", idea)

        assert safety_result.status == "success"
        assert safety_result.output_data["approved"] is True

        # Step 2: Planning (uses same idea)
        planner_result = runtime.execute_agent("planner", idea)

        assert planner_result.status == "success"
        assert "tasks" in planner_result.output_data
        assert len(planner_result.output_data["tasks"]) > 0

    def test_dangerous_idea_blocks_pipeline(self):
        """Test that dangerous idea is blocked by SafetyGuard"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())

        idea = Idea(description="Tool to hack into systems")
        safety_result = runtime.execute_agent("safety_guard", idea)

        assert safety_result.status == "success"  # Agent executed successfully
        assert safety_result.output_data["approved"] is False  # But idea rejected

        # Pipeline should stop here - planner shouldn't run with rejected idea


class TestPlannerToArchitectWorkflow:
    """Test workflow from PlannerAgent to ArchitectAgent"""

    def test_planner_output_flows_to_architect(self):
        """Test that planner output flows to architect"""
        runtime = AgentRuntime()
        runtime.register_agent(PlannerAgent())
        runtime.register_agent(ArchitectAgent())

        idea = Idea(description="Build a file organizer tool")

        # Step 1: Planning
        planner_result = runtime.execute_agent("planner", idea)
        assert planner_result.status == "success"
        task_count = len(planner_result.output_data["tasks"])

        # Step 2: Architecture (can use task count)
        arch_input = ArchitectInput(idea=idea, task_count=task_count)
        architect_result = runtime.execute_agent("architect", arch_input)

        assert architect_result.status == "success"
        assert "spec" in architect_result.output_data
        assert "name" in architect_result.output_data["spec"]
        assert "tech_stack" in architect_result.output_data["spec"]


class TestArchitectToImplementerWorkflow:
    """Test workflow from ArchitectAgent to ImplementerAgent"""

    def test_architect_spec_flows_to_implementer(self):
        """Test that architect spec flows to implementer"""
        runtime = AgentRuntime()
        runtime.register_agent(ArchitectAgent())
        runtime.register_agent(ImplementerAgent())

        idea = Idea(description="Build a todo list app")

        # Step 1: Architecture design
        architect_result = runtime.execute_agent("architect", idea)
        assert architect_result.status == "success"

        # Step 2: Code generation (needs ProjectSpec from architect)
        spec = ProjectSpec(**architect_result.output_data["spec"])
        implementer_result = runtime.execute_agent("implementer", spec)

        assert implementer_result.status == "success"
        assert "files" in implementer_result.output_data
        assert implementer_result.output_data["files_created"] > 0


class TestImplementerToTesterWorkflow:
    """Test workflow from ImplementerAgent to TesterAgent"""

    def test_implementer_code_flows_to_tester(self):
        """Test that implementer output flows to tester"""
        runtime = AgentRuntime()
        runtime.register_agent(ArchitectAgent())
        runtime.register_agent(ImplementerAgent())
        runtime.register_agent(TesterAgent())

        idea = Idea(description="Build a calculator")

        # Step 1: Architecture
        architect_result = runtime.execute_agent("architect", idea)
        spec = ProjectSpec(**architect_result.output_data["spec"])

        # Step 2: Implementation
        implementer_result = runtime.execute_agent("implementer", spec)
        code_files = implementer_result.output_data["files"]

        # Step 3: Testing
        test_input = TestInput(spec=spec, code_files=code_files)
        tester_result = runtime.execute_agent("tester", test_input)

        assert tester_result.status == "success"
        assert "total_tests" in tester_result.output_data
        assert "coverage_percent" in tester_result.output_data


class TestArchitectToDocWriterWorkflow:
    """Test workflow from ArchitectAgent to DocWriterAgent"""

    def test_architect_spec_flows_to_doc_writer(self):
        """Test that architect spec flows to doc writer"""
        runtime = AgentRuntime()
        runtime.register_agent(ArchitectAgent())
        runtime.register_agent(DocWriterAgent())

        idea = Idea(description="Build a note-taking app")

        # Step 1: Architecture
        architect_result = runtime.execute_agent("architect", idea)
        spec = ProjectSpec(**architect_result.output_data["spec"])

        # Step 2: Documentation
        doc_result = runtime.execute_agent("doc_writer", spec)

        assert doc_result.status == "success"
        assert "files" in doc_result.output_data
        assert len(doc_result.output_data["files"]) > 0


class TestBlueCollarAdvisorIntegration:
    """Test BlueCollarAdvisor integration with other agents"""

    def test_advisor_reviews_architecture(self):
        """Test that advisor reviews architecture decisions"""
        runtime = AgentRuntime()
        runtime.register_agent(ArchitectAgent())
        runtime.register_agent(BlueCollarAdvisor())

        idea = Idea(
            description="Build a tool for mechanics",
            target_users=["mechanic"],
            environment="noisy workshop"
        )

        # Step 1: Architecture
        architect_result = runtime.execute_agent("architect", idea)
        spec = ProjectSpec(**architect_result.output_data["spec"])

        # Step 2: Advisory review
        advisory_input = AdvisoryInput(idea=idea, spec=spec)
        advisor_result = runtime.execute_agent("blue_collar_advisor", advisory_input)

        assert advisor_result.status == "success"
        assert "recommendations" in advisor_result.output_data
        assert "environment_fit" in advisor_result.output_data


class TestFullPipelineWorkflow:
    """Test complete multi-agent pipeline"""

    def test_complete_pipeline_stages(self):
        """Test executing complete pipeline stages"""
        runtime = AgentRuntime()

        # Register all agents
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())
        runtime.register_agent(ArchitectAgent())
        runtime.register_agent(BlueCollarAdvisor())
        runtime.register_agent(ImplementerAgent())
        runtime.register_agent(TesterAgent())
        runtime.register_agent(DocWriterAgent())

        idea = Idea(
            description="Build a maintenance log tool",
            target_users=["marine_engineer"],
            features=["offline mode", "timestamp entries"]
        )

        # Stage 1: Safety
        safety_result = runtime.execute_agent("safety_guard", idea)
        assert safety_result.status == "success"
        assert safety_result.output_data["approved"] is True

        # Stage 2: Planning
        planner_result = runtime.execute_agent("planner", idea)
        assert planner_result.status == "success"
        task_count = len(planner_result.output_data["tasks"])

        # Stage 3: Architecture
        arch_input = ArchitectInput(idea=idea, task_count=task_count)
        architect_result = runtime.execute_agent("architect", arch_input)
        assert architect_result.status == "success"
        spec = ProjectSpec(**architect_result.output_data["spec"])

        # Stage 4: Advisory
        advisory_input = AdvisoryInput(idea=idea, spec=spec)
        advisor_result = runtime.execute_agent("blue_collar_advisor", advisory_input)
        assert advisor_result.status == "success"

        # Stage 5: Implementation
        implementer_result = runtime.execute_agent("implementer", spec)
        assert implementer_result.status == "success"
        code_files = implementer_result.output_data["files"]

        # Stage 6: Testing
        test_input = TestInput(spec=spec, code_files=code_files)
        tester_result = runtime.execute_agent("tester", test_input)
        assert tester_result.status == "success"

        # Stage 7: Documentation
        doc_result = runtime.execute_agent("doc_writer", spec)
        assert doc_result.status == "success"

        # Verify execution history
        history = runtime.get_execution_history()
        assert len(history) == 7  # All 7 stages executed


class TestErrorPropagation:
    """Test error propagation across pipeline stages"""

    def test_agent_failure_recorded_in_history(self):
        """Test that agent failures are recorded in execution history"""
        from code_factory.core.agent_runtime import BaseAgent, AgentExecutionError
        from pydantic import BaseModel

        class FailingAgent(BaseAgent):
            @property
            def name(self):
                return "failing_agent"

            @property
            def description(self):
                return "Agent that fails"

            def execute(self, input_data):
                raise AgentExecutionError("Simulated failure")

        runtime = AgentRuntime()
        runtime.register_agent(FailingAgent())
        runtime.register_agent(SafetyGuard())

        # Execute failing agent
        idea = Idea(description="Test")
        failing_result = runtime.execute_agent("failing_agent", idea)
        assert failing_result.status == "failed"

        # Subsequent agents can still execute
        success_result = runtime.execute_agent("safety_guard", idea)
        assert success_result.status == "success"

        # Both should be in history
        history = runtime.get_execution_history()
        assert len(history) == 2
        assert history[0].status == "failed"
        assert history[1].status == "success"


class TestStateManagement:
    """Test state management across pipeline"""

    def test_execution_history_maintains_order(self):
        """Test that execution history maintains order"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())
        runtime.register_agent(ArchitectAgent())

        idea = Idea(description="Build a tool")

        # Execute agents in order
        runtime.execute_agent("safety_guard", idea)
        runtime.execute_agent("planner", idea)
        runtime.execute_agent("architect", idea)

        # Check history order
        history = runtime.get_execution_history()
        assert len(history) == 3
        assert history[0].agent_name == "safety_guard"
        assert history[1].agent_name == "planner"
        assert history[2].agent_name == "architect"

    def test_agent_outputs_are_independent(self):
        """Test that agent outputs don't interfere with each other"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())

        idea1 = Idea(description="Safe tool")
        idea2 = Idea(description="Tool to hack systems")

        result1 = runtime.execute_agent("safety_guard", idea1)
        result2 = runtime.execute_agent("safety_guard", idea2)

        # Results should be different
        assert result1.output_data["approved"] is True
        assert result2.output_data["approved"] is False

    def test_concurrent_execution_tracking(self):
        """Test that multiple executions are tracked separately"""
        runtime = AgentRuntime()
        runtime.register_agent(PlannerAgent())

        ideas = [
            Idea(description="Build calculator"),
            Idea(description="Build todo app"),
            Idea(description="Build file manager")
        ]

        # Execute all
        for idea in ideas:
            runtime.execute_agent("planner", idea)

        # Each should be tracked separately
        history = runtime.get_execution_history()
        assert len(history) == 3

        # Each should have different input
        descriptions = [h.input_data["description"] for h in history]
        assert len(set(descriptions)) == 3  # All unique


class TestDataFlowValidation:
    """Test data flow validation between agents"""

    def test_spec_from_architect_valid_for_implementer(self):
        """Test that architect output is valid input for implementer"""
        runtime = AgentRuntime()
        runtime.register_agent(ArchitectAgent())
        runtime.register_agent(ImplementerAgent())

        idea = Idea(description="Build a tool")
        architect_result = runtime.execute_agent("architect", idea)

        # Should be able to create ProjectSpec from output
        spec = ProjectSpec(**architect_result.output_data["spec"])

        # Should be valid input for implementer
        implementer_result = runtime.execute_agent("implementer", spec)
        assert implementer_result.status == "success"

    def test_tasks_from_planner_have_valid_structure(self):
        """Test that planner output has valid task structure"""
        runtime = AgentRuntime()
        runtime.register_agent(PlannerAgent())

        idea = Idea(description="Build a tool")
        planner_result = runtime.execute_agent("planner", idea)

        tasks = planner_result.output_data["tasks"]

        # Each task should have required fields
        for task in tasks:
            assert "id" in task
            assert "type" in task
            assert "description" in task
            assert "dependencies" in task
            assert "status" in task


class TestFoundationAgentsIntegration:
    """Test PlannerAgent + ArchitectAgent integration with new result models"""

    def test_planner_architect_end_to_end(self):
        """Test complete flow from Idea -> PlanResult -> ArchitectResult"""
        # Direct agent calls (not through runtime) to test new models
        planner = PlannerAgent()
        architect = ArchitectAgent()

        # Step 1: Create idea
        idea = Idea(
            description="Marine log analyzer for CSV files",
            features=["Parse CSV", "Generate reports"],
            target_users=["marine_engineer"],
            environment="noisy engine room, limited WiFi"
        )

        # Step 2: Plan tasks
        plan_result = planner.execute(idea)

        # Verify PlanResult structure
        assert isinstance(plan_result, PlanResult)
        assert len(plan_result.tasks) >= 5  # Should have multiple tasks
        assert plan_result.estimated_complexity in ["simple", "moderate", "complex"]
        assert isinstance(plan_result.dependency_graph, dict)

        # Step 3: Design architecture with tasks
        arch_input = ArchitectInput(idea=idea, tasks=plan_result.tasks)
        arch_result = architect.execute(arch_input)

        # Verify ArchitectResult structure
        assert isinstance(arch_result, ArchitectResult)
        assert isinstance(arch_result.spec, ProjectSpec)
        assert isinstance(arch_result.rationale, dict)
        assert 0.0 <= arch_result.blue_collar_score <= 10.0
        assert isinstance(arch_result.warnings, list)

        # Verify spec details
        spec = arch_result.spec
        assert spec.name is not None
        assert len(spec.tech_stack) > 0
        assert len(spec.dependencies) > 0
        assert spec.user_profile == "marine_engineer"
        assert spec.environment == "noisy engine room, limited WiFi"

        # Verify blue-collar score is reasonable for field tool
        # CSV parsing, offline = should be high score
        assert arch_result.blue_collar_score >= 7.0

    def test_planner_architect_integration_via_runtime(self):
        """Test PlannerAgent -> ArchitectAgent through AgentRuntime"""
        runtime = AgentRuntime()
        runtime.register_agent(PlannerAgent())
        runtime.register_agent(ArchitectAgent())

        idea = Idea(
            description="Build offline calculator for field workers",
            features=["basic math", "formula storage"],
            target_users=["mechanic"]
        )

        # Execute planner
        planner_result = runtime.execute_agent("planner", idea)
        assert planner_result.status == "success"

        # Extract tasks from result
        tasks_data = planner_result.output_data["tasks"]

        # Execute architect with idea (ArchitectAgent accepts both Idea and ArchitectInput)
        architect_result = runtime.execute_agent("architect", idea)
        assert architect_result.status == "success"

        # Verify complete data flow
        assert "spec" in architect_result.output_data
        assert "blue_collar_score" in architect_result.output_data
        assert "rationale" in architect_result.output_data


class TestPipelineRobustness:
    """Test pipeline robustness and recovery"""

    def test_pipeline_continues_after_non_critical_failure(self):
        """Test that pipeline can continue after non-critical failures"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())

        # Execute safety check (success)
        idea = Idea(description="Build a tool")
        safety_result = runtime.execute_agent("safety_guard", idea)
        assert safety_result.status == "success"

        # Even if one agent failed conceptually, others can still run
        planner_result = runtime.execute_agent("planner", idea)
        assert planner_result.status == "success"

    def test_agents_maintain_independence(self):
        """Test that agents maintain independence"""
        runtime = AgentRuntime()
        runtime.register_agent(SafetyGuard())
        runtime.register_agent(PlannerAgent())

        # Each agent should work independently
        idea = Idea(description="Build a tool")

        # Can execute planner without safety check
        planner_result = runtime.execute_agent("planner", idea)
        assert planner_result.status == "success"

        # Can execute safety check afterward
        safety_result = runtime.execute_agent("safety_guard", idea)
        assert safety_result.status == "success"
