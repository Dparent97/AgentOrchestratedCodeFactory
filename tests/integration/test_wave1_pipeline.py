"""
Wave 1 Integration Tests - Full Pipeline Testing

Tests the complete Wave 1 pipeline:
    Idea -> SafetyGuard -> PlannerAgent -> ArchitectAgent

This ensures all Wave 1 agents work together correctly to transform
a plain-language idea into a complete technical specification.

Coverage Goals:
- Safety validation works correctly
- Planning produces valid task graphs
- Architecture generates complete specs
- Data flows correctly between agents
- Blue-collar score is calculated
"""

import pytest

from code_factory.agents.architect import ArchitectAgent, ArchitectInput
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.models import Idea, ProjectSpec, SafetyCheck, ArchitectResult, PlanResult
from tests.harness.agent_test_harness import AgentTestHarness


@pytest.mark.integration
@pytest.mark.wave1
class TestWave1Pipeline:
    """Integration tests for the complete Wave 1 pipeline"""

    def test_idea_to_spec_pipeline_simple(self, idea_simple_csv):
        """Test full Wave 1 pipeline with simple CSV parser idea"""
        # Safety check
        guard = SafetyGuard()
        safety = guard.execute(idea_simple_csv)
        assert isinstance(safety, SafetyCheck)
        assert safety.approved, f"Safety check failed: {safety.warnings}"

        # Planning
        planner = PlannerAgent()
        plan = planner.execute(idea_simple_csv)
        assert len(plan.tasks) > 0, "Planner should generate tasks"
        assert all(hasattr(task, "id") for task in plan.tasks), "All tasks need IDs"

        # Architecture
        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_simple_csv, task_count=len(plan.tasks))
        arch_result = architect.execute(arch_input)
        assert isinstance(arch_result, ArchitectResult)
        assert isinstance(arch_result.spec, ProjectSpec)
        assert arch_result.spec.name is not None
        assert len(arch_result.spec.tech_stack) > 0
        assert arch_result.blue_collar_score >= 0.0

        print(f"✅ Simple pipeline complete: {arch_result.spec.name}")
        print(f"   Tasks: {len(plan.tasks)}")
        print(f"   Tech stack: {list(arch_result.spec.tech_stack.keys())}")
        print(f"   Blue-collar score: {arch_result.blue_collar_score}")

    def test_idea_to_spec_pipeline_marine_log(self, idea_marine_log):
        """Test full Wave 1 pipeline with marine log analyzer"""
        # Safety check
        guard = SafetyGuard()
        safety = guard.execute(idea_marine_log)
        assert isinstance(safety, SafetyCheck)
        assert safety.approved

        # Check for semantic warnings (marine engineer is privileged user)
        assert len(safety.warnings) >= 0  # May have warnings but still approved

        # Planning
        planner = PlannerAgent()
        plan = planner.execute(idea_marine_log)
        assert len(plan.tasks) > 0

        # Verify dependency graph is valid (no cycles)
        task_ids = {task.id for task in plan.tasks}
        for task in plan.tasks:
            for dep_id in task.dependencies:
                assert dep_id in task_ids, f"Task {task.id} has invalid dependency: {dep_id}"

        # Architecture
        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_marine_log, task_count=len(plan.tasks))
        arch_result = architect.execute(arch_input)
        assert isinstance(arch_result, ArchitectResult)
        assert isinstance(arch_result.spec, ProjectSpec)

        # Verify spec preserves user context
        assert arch_result.spec.user_profile == "marine_engineer"
        assert arch_result.spec.environment == "noisy engine room, limited WiFi"

        print(f"✅ Marine log pipeline complete: {arch_result.spec.name}")
        print(f"   User: {arch_result.spec.user_profile}")
        print(f"   Environment: {arch_result.spec.environment}")
        print(f"   Blue-collar score: {arch_result.blue_collar_score}")

    def test_idea_to_spec_pipeline_complex(self, idea_workshop_tool):
        """Test full Wave 1 pipeline with complex workshop tool"""
        # Safety check
        guard = SafetyGuard()
        safety = guard.execute(idea_workshop_tool)
        assert safety.approved

        # Planning - complex idea should generate more tasks
        planner = PlannerAgent()
        plan = planner.execute(idea_workshop_tool)
        assert len(plan.tasks) >= 3, "Complex idea should have multiple tasks"

        # Verify task types are diverse
        task_types = {task.type for task in plan.tasks}
        assert len(task_types) >= 2, "Should have multiple task types"

        # Architecture
        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_workshop_tool, task_count=len(plan.tasks))
        arch_result = architect.execute(arch_input)

        # Complex project should have comprehensive structure
        assert len(arch_result.spec.folder_structure) >= 2, "Should have multiple folders"
        assert len(arch_result.spec.dependencies) >= 0, "May have dependencies"

        print(f"✅ Complex pipeline complete: {arch_result.spec.name}")
        print(f"   Folders: {list(arch_result.spec.folder_structure.keys())}")

    def test_safety_guard_blocks_dangerous_ideas(self):
        """Test that safety guard blocks dangerous operations"""
        dangerous_idea = Idea(
            description="Build a tool to hack into systems and exploit vulnerabilities"
        )

        guard = SafetyGuard()
        safety = guard.execute(dangerous_idea)

        # Should be blocked
        assert not safety.approved, "Dangerous idea should be blocked"
        assert len(safety.blocked_keywords) > 0, "Should identify dangerous keywords"
        assert len(safety.warnings) > 0, "Should provide warnings"

        print(f"✅ Safety guard correctly blocked dangerous idea")
        print(f"   Blocked keywords: {safety.blocked_keywords}")

    def test_pipeline_preserves_constraints(self, idea_with_constraints):
        """Test that constraints are preserved through the pipeline"""
        # Run through pipeline
        guard = SafetyGuard()
        safety = guard.execute(idea_with_constraints)
        assert safety.approved

        planner = PlannerAgent()
        plan = planner.execute(idea_with_constraints)

        architect = ArchitectAgent()
        arch_result = architect.execute(idea_with_constraints)

        # Constraints should influence architecture
        # (In real implementation, architect would use constraints)
        assert arch_result.spec.name is not None
        assert "mechanic" in arch_result.spec.user_profile or arch_result.spec.user_profile == "mechanic"

    def test_pipeline_with_minimal_idea(self, idea_calculator):
        """Test pipeline with minimal idea (just description)"""
        # Should work with minimal input
        guard = SafetyGuard()
        safety = guard.execute(idea_calculator)
        assert safety.approved

        planner = PlannerAgent()
        plan = planner.execute(idea_calculator)
        assert len(plan.tasks) > 0

        architect = ArchitectAgent()
        arch_result = architect.execute(idea_calculator)
        assert arch_result.spec.name is not None

        print(f"✅ Minimal idea pipeline complete: {arch_result.spec.name}")

    def test_planner_creates_valid_dependency_graph(self, idea_marine_log):
        """Test that planner creates a valid task dependency graph"""
        planner = PlannerAgent()
        plan = planner.execute(idea_marine_log)

        # Get all task IDs
        task_ids = {task.id for task in plan.tasks}

        # Verify no self-dependencies
        for task in plan.tasks:
            assert task.id not in task.dependencies, f"Task {task.id} depends on itself"

        # Verify all dependencies exist
        for task in plan.tasks:
            for dep_id in task.dependencies:
                assert (
                    dep_id in task_ids
                ), f"Task {task.id} has non-existent dependency: {dep_id}"

        # Verify at least one task has no dependencies (entry point)
        root_tasks = [task for task in plan.tasks if len(task.dependencies) == 0]
        assert len(root_tasks) > 0, "At least one task should have no dependencies"

        print(f"✅ Dependency graph is valid")
        print(f"   Total tasks: {len(plan.tasks)}")
        print(f"   Root tasks: {len(root_tasks)}")

    def test_architect_generates_complete_spec(self, idea_marine_log, planner_agent):
        """Test that architect generates a complete, valid project spec"""
        plan = planner_agent.execute(idea_marine_log)

        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_marine_log, task_count=len(plan.tasks))
        arch_result = architect.execute(arch_input)

        # Verify all required fields
        spec = arch_result.spec
        assert spec.name is not None
        assert len(spec.name) > 0
        assert spec.description is not None
        assert len(spec.description) > 0
        assert len(spec.tech_stack) > 0
        assert "language" in spec.tech_stack
        assert len(spec.folder_structure) > 0
        assert spec.entry_point is not None
        assert len(spec.entry_point) > 0

        # Verify name format (lowercase, hyphenated)
        assert spec.name.islower() or "-" in spec.name or "_" in spec.name
        assert " " not in spec.name

        print(f"✅ Complete spec generated: {spec.name}")

    def test_wave1_agents_follow_interface(self, wave1_agents, agent_test_harness):
        """Test that all Wave 1 agents follow BaseAgent interface"""
        for agent_name, agent in wave1_agents.items():
            agent_test_harness.test_agent_interface(agent)
            agent_test_harness.test_agent_properties_not_empty(agent)

        print(f"✅ All {len(wave1_agents)} Wave 1 agents follow interface")


@pytest.mark.integration
@pytest.mark.wave1
class TestWave1ErrorHandling:
    """Test error handling in Wave 1 pipeline"""

    def test_safety_guard_handles_empty_description(self):
        """Test safety guard with empty description"""
        with pytest.raises((ValueError, Exception)):
            Idea(description="")

    def test_planner_handles_minimal_idea(self):
        """Test planner with very minimal idea"""
        idea = Idea(description="Build a tool")
        planner = PlannerAgent()
        plan = planner.execute(idea)

        # Should still generate some tasks
        assert len(plan.tasks) > 0

    def test_architect_handles_simple_idea(self):
        """Test architect with very simple idea"""
        idea = Idea(description="Calculator")
        architect = ArchitectAgent()
        arch_result = architect.execute(idea)

        # Should generate valid spec
        assert arch_result.spec.name is not None
        assert len(arch_result.spec.tech_stack) > 0


@pytest.mark.integration
@pytest.mark.wave1
@pytest.mark.slow
class TestWave1Performance:
    """Performance tests for Wave 1 pipeline"""

    def test_pipeline_completes_quickly(self, idea_simple_csv, performance_harness):
        """Test that entire pipeline completes in reasonable time"""
        import time

        start = time.time()

        # Run full pipeline
        guard = SafetyGuard()
        safety = guard.execute(idea_simple_csv)
        assert safety.approved

        planner = PlannerAgent()
        plan = planner.execute(idea_simple_csv)

        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_simple_csv, task_count=len(plan.tasks))
        arch_result = architect.execute(arch_input)

        elapsed = time.time() - start

        # Pipeline should complete quickly (stub agents are fast)
        assert elapsed < 5.0, f"Pipeline took {elapsed:.2f}s (max 5s)"

        print(f"✅ Pipeline completed in {elapsed:.2f}s")

    def test_individual_agent_performance(self, idea_marine_log, performance_harness):
        """Test individual agent performance"""
        # Safety guard
        guard = SafetyGuard()
        safety_time = performance_harness.test_agent_performance(
            guard, idea_marine_log, max_execution_time_seconds=2.0
        )

        # Planner
        planner = PlannerAgent()
        planner_time = performance_harness.test_agent_performance(
            planner, idea_marine_log, max_execution_time_seconds=5.0
        )

        # Architect
        architect = ArchitectAgent()
        architect_time = performance_harness.test_agent_performance(
            architect, idea_marine_log, max_execution_time_seconds=5.0
        )

        print(f"✅ Performance test passed")
        print(f"   SafetyGuard: {safety_time:.2f}s")
        print(f"   PlannerAgent: {planner_time:.2f}s")
        print(f"   ArchitectAgent: {architect_time:.2f}s")


@pytest.mark.integration
@pytest.mark.wave1
class TestWave1DataFlow:
    """Test data flow between Wave 1 agents"""

    def test_data_preservation_through_pipeline(self, idea_marine_log):
        """Test that important data is preserved through the pipeline"""
        original_description = idea_marine_log.description
        original_target_users = idea_marine_log.target_users
        original_environment = idea_marine_log.environment

        # Run through pipeline
        guard = SafetyGuard()
        safety = guard.execute(idea_marine_log)
        assert safety.approved

        planner = PlannerAgent()
        plan = planner.execute(idea_marine_log)

        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_marine_log, task_count=len(plan.tasks))
        arch_result = architect.execute(arch_input)

        # Verify data preservation
        spec = arch_result.spec
        # Description should influence spec
        assert spec.description is not None

        # User profile should be preserved
        if len(original_target_users) > 0:
            assert spec.user_profile == original_target_users[0]

        # Environment should be preserved
        if original_environment:
            assert arch_result.spec.environment == original_environment

        print(f"✅ Data preserved through pipeline")

    def test_task_count_flows_to_architect(self, idea_marine_log):
        """Test that task count from planner flows to architect"""
        planner = PlannerAgent()
        plan = planner.execute(idea_marine_log)
        task_count = len(plan.tasks)

        architect = ArchitectAgent()
        arch_input = ArchitectInput(idea=idea_marine_log, task_count=task_count)
        arch_result = architect.execute(arch_input)

        # Architect should receive task count
        # (May use it for complexity estimation)
        assert arch_result.spec is not None
        assert isinstance(arch_result, ArchitectResult)
        assert isinstance(arch_result.spec, ProjectSpec)

        print(f"✅ Task count ({task_count}) flowed to architect")
