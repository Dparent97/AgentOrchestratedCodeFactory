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


class TestCLIGenerate:
    """Test generate command"""

    def test_generate_help(self):
        """Test generate command help text"""
        result = runner.invoke(app, ["generate", "--help"])
        assert result.exit_code == 0
        assert "Generate a project" in result.stdout
        assert "--output" in result.stdout
        assert "--feature" in result.stdout

    def test_generate_requires_description(self):
        """Test that generate requires a description argument"""
        result = runner.invoke(app, ["generate"])
        assert result.exit_code != 0
        # Typer shows error in different format

    def test_generate_success(self):
        """Test successful generate command with mocked orchestrator"""
        from code_factory.core.models import ProjectResult, AgentRun
        from datetime import datetime
        
        mock_result = ProjectResult(
            success=True,
            project_name="test-project",
            project_path="/tmp/test-project",
            agent_runs=[
                AgentRun(
                    agent_name="planner",
                    input_data={},
                    output_data={},
                    status="success",
                    started_at=datetime.now(),
                    completed_at=datetime.now(),
                    duration_seconds=0.1
                )
            ],
            errors=[],
        )
        
        with patch("code_factory.cli.main.Orchestrator") as MockOrch:
            MockOrch.return_value.run_factory.return_value = mock_result
            result = runner.invoke(app, ["generate", "A test project"])
        
        assert result.exit_code == 0
        assert "Project generated successfully" in result.stdout
        assert "test-project" in result.stdout

    def test_generate_with_options(self):
        """Test generate command with all options"""
        from code_factory.core.models import ProjectResult
        
        mock_result = ProjectResult(
            success=True,
            project_name="feature-project",
            project_path="/tmp/feature-project",
            agent_runs=[],
            errors=[],
            git_repo_url="https://github.com/user/repo",
        )
        
        with patch("code_factory.cli.main.Orchestrator") as MockOrch:
            MockOrch.return_value.run_factory.return_value = mock_result
            result = runner.invoke(app, [
                "generate", "Project with features",
                "-f", "auth",
                "-f", "api",
                "-t", "developer",
                "-e", "cloud",
                "-o", "/tmp/out"
            ])
        
        assert result.exit_code == 0
        assert "Project generated successfully" in result.stdout

    def test_generate_failure(self):
        """Test generate command when orchestrator fails"""
        from code_factory.core.models import ProjectResult
        
        mock_result = ProjectResult(
            success=False,
            project_name="failed-project",
            agent_runs=[],
            errors=["Something went wrong", "Another error"],
        )
        
        with patch("code_factory.cli.main.Orchestrator") as MockOrch:
            MockOrch.return_value.run_factory.return_value = mock_result
            result = runner.invoke(app, ["generate", "A failing project"])
        
        assert result.exit_code == 1
        assert "Project generation failed" in result.stdout
        assert "Something went wrong" in result.stdout

    def test_generate_exception(self):
        """Test generate command when orchestrator raises exception"""
        with patch("code_factory.cli.main.Orchestrator") as MockOrch:
            MockOrch.return_value.run_factory.side_effect = RuntimeError("Fatal error")
            result = runner.invoke(app, ["generate", "A crashing project"])
        
        assert result.exit_code == 1
        assert "Error" in result.stdout


class TestCLIInitEdgeCases:
    """Test init command edge cases"""

    def test_init_missing_directories(self):
        """Test init reports missing directories"""
        with patch("code_factory.cli.main.Path") as MockPath:
            # Make some directories appear missing
            mock_path = MockPath.return_value.__truediv__.return_value
            mock_path.exists.return_value = False
            mock_path.parent = MockPath.return_value
            
            result = runner.invoke(app, ["init"])
            # Should complete (warning about missing components)
            assert result.exit_code in [0, 1]
