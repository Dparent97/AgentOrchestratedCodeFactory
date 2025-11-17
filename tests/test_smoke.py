"""
Smoke tests for the Code Factory

Basic tests to verify core modules can be imported and basic
functionality works.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_imports():
    """Test that all core modules can be imported"""
    from code_factory import __version__
    from code_factory.core import models, orchestrator, agent_runtime
    from code_factory.agents import (
        planner, architect, implementer, tester,
        doc_writer, git_ops, blue_collar_advisor, safety_guard
    )
    
    assert __version__ == "0.1.0"


def test_runtime_initialization():
    """Test that AgentRuntime can be created and agents registered"""
    from code_factory.core.agent_runtime import AgentRuntime
    from code_factory.agents.planner import PlannerAgent
    
    runtime = AgentRuntime()
    planner = PlannerAgent()
    
    runtime.register_agent(planner)
    
    agents = runtime.list_agents()
    assert "planner" in agents
    assert agents["planner"] == planner.description


def test_safety_guard():
    """Test that SafetyGuard rejects dangerous operations"""
    from code_factory.core.models import Idea
    from code_factory.agents.safety_guard import SafetyGuard
    
    # Safe idea
    safe_idea = Idea(description="Build a log file parser CLI tool")
    guard = SafetyGuard()
    result = guard.execute(safe_idea)
    
    assert result.approved is True
    assert len(result.blocked_keywords) == 0
    
    # Dangerous idea
    dangerous_idea = Idea(description="Control equipment and bypass interlock safety systems")
    result = guard.execute(dangerous_idea)
    
    assert result.approved is False
    assert len(result.blocked_keywords) > 0


def test_planner_agent():
    """Test that PlannerAgent generates tasks"""
    from code_factory.core.models import Idea
    from code_factory.agents.planner import PlannerAgent
    
    idea = Idea(description="Build a simple calculator CLI")
    planner = PlannerAgent()
    
    result = planner.execute(idea)
    
    assert hasattr(result, "tasks")
    assert len(result.tasks) > 0
    assert result.tasks[0].id == "t1"


def test_cli_exists():
    """Test that CLI module exists and has required commands"""
    from code_factory.cli import main
    
    assert hasattr(main, "app")
    assert hasattr(main, "init")
    assert hasattr(main, "status")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
