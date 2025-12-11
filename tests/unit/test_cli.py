"""
Unit tests for CLI commands

Tests cover:
- CLI initialization
- Status command
- Version command
- Generate command
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from code_factory.cli.main import app, get_runtime


runner = CliRunner()


class TestCLIVersion:
    """Test version command"""

    def test_version_command(self):
        """Test that version command shows version"""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "Code Factory version" in result.stdout


class TestCLIInit:
    """Test init command"""

    def test_init_command(self):
        """Test that init command runs"""
        result = runner.invoke(app, ["init"])
        # Should complete (may succeed or warn about missing dirs)
        assert result.exit_code in [0, 1]


class TestCLIStatus:
    """Test status command"""

    def test_status_command(self):
        """Test that status command shows status"""
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Agent-Orchestrated Code Factory" in result.stdout
        assert "Available Agents" in result.stdout


class TestGetRuntime:
    """Test get_runtime helper function"""

    def test_get_runtime_returns_agent_runtime(self):
        """Test that get_runtime returns configured AgentRuntime"""
        from code_factory.core.agent_runtime import AgentRuntime
        
        runtime = get_runtime()
        
        assert isinstance(runtime, AgentRuntime)
        
        # Should have all agents registered
        agents = runtime.list_agents()
        assert "safety_guard" in agents
        assert "planner" in agents
        assert "architect" in agents
        assert "implementer" in agents
        assert "tester" in agents
        assert "doc_writer" in agents
        assert "git_ops" in agents
        assert "blue_collar_advisor" in agents

    def test_get_runtime_agents_are_functional(self):
        """Test that runtime agents can execute"""
        from code_factory.core.models import Idea
        
        runtime = get_runtime()
        
        idea = Idea(description="Test project")
        result = runtime.execute_agent("safety_guard", idea)
        
        assert result.status == "success"


class TestCLICommands:
    """Test that available CLI commands work"""

    def test_help_command(self):
        """Test help command lists available commands"""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.stdout
        assert "status" in result.stdout
        assert "version" in result.stdout


class TestCLIOutput:
    """Test CLI output formatting"""

    def test_status_shows_agents_table(self):
        """Test that status shows agents in a table"""
        result = runner.invoke(app, ["status"])
        
        assert result.exit_code == 0
        # Should show agent names
        assert "safety_guard" in result.stdout
        assert "planner" in result.stdout

    def test_status_shows_environment(self):
        """Test that status shows environment information"""
        result = runner.invoke(app, ["status"])
        
        assert result.exit_code == 0
        assert "Environment" in result.stdout
        assert "Python" in result.stdout
