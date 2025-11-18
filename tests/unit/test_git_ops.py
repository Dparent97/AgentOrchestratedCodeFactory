"""
Unit tests for GitOpsAgent

Tests all Git operations including repository initialization,
commits, remote management, and error handling.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from git import Repo, InvalidGitRepositoryError

from code_factory.agents.git_ops import GitOpsAgent, GitOperation, GitResult


@pytest.fixture
def temp_repo_dir():
    """Create a temporary directory for test repositories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def git_agent():
    """Create a GitOpsAgent instance for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test_git.log"
        agent = GitOpsAgent(log_file=str(log_file))
        yield agent


class TestGitOpsAgent:
    """Test suite for GitOpsAgent"""

    def test_agent_properties(self, git_agent):
        """Test that agent has correct name and description"""
        assert git_agent.name == "git_ops"
        assert "Git" in git_agent.description
        assert "repositories" in git_agent.description.lower()

    def test_init_new_repository(self, git_agent, temp_repo_dir):
        """Test initializing a new Git repository"""
        repo_path = temp_repo_dir / "new_repo"

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="init"
        )

        result = git_agent.execute(operation)

        assert isinstance(result, GitResult)
        assert result.success is True
        assert result.operation == "init"
        assert repo_path.exists()
        assert (repo_path / ".git").exists()

        # Verify it's a valid git repo
        repo = Repo(repo_path)
        assert repo.git_dir is not None

    def test_init_existing_repository(self, git_agent, temp_repo_dir):
        """Test initializing an already initialized repository"""
        repo_path = temp_repo_dir / "existing_repo"
        repo_path.mkdir()
        Repo.init(repo_path)

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="init"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert "already" in result.message.lower()

    def test_commit_changes(self, git_agent, temp_repo_dir):
        """Test committing changes to a repository"""
        repo_path = temp_repo_dir / "commit_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Create a test file
        test_file = repo_path / "test.txt"
        test_file.write_text("Hello, world!")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="commit",
            message="Initial commit",
            files=["."]
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert result.operation == "commit"
        assert "commit_sha" in result.details
        assert len(repo.head.commit.hexsha) == 40

    def test_commit_no_changes(self, git_agent, temp_repo_dir):
        """Test committing when there are no changes"""
        repo_path = temp_repo_dir / "no_changes_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Create initial commit
        test_file = repo_path / "test.txt"
        test_file.write_text("Initial")
        repo.index.add(["."])
        repo.index.commit("Initial commit")

        # Try to commit again without changes (don't add anything)
        operation = GitOperation(
            repo_path=str(repo_path),
            operation="commit",
            message="Second commit",
            files=[]  # Empty files list means nothing to add
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert "no changes" in result.message.lower()

    def test_commit_without_message(self, git_agent, temp_repo_dir):
        """Test that commit without message fails gracefully"""
        repo_path = temp_repo_dir / "no_msg_repo"
        repo_path.mkdir()
        Repo.init(repo_path)

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="commit"
        )

        result = git_agent.execute(operation)

        assert result.success is False
        assert "message is required" in result.message.lower()

    def test_add_remote(self, git_agent, temp_repo_dir):
        """Test adding a remote to a repository"""
        repo_path = temp_repo_dir / "remote_repo"
        repo_path.mkdir()
        Repo.init(repo_path)

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="add_remote",
            remote_url="https://github.com/test/repo.git",
            remote_name="origin"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert result.operation == "add_remote"
        assert "origin" in result.message

        # Verify remote was added
        repo = Repo(repo_path)
        assert "origin" in [r.name for r in repo.remotes]
        assert repo.remote("origin").url == "https://github.com/test/repo.git"

    def test_add_remote_already_exists(self, git_agent, temp_repo_dir):
        """Test adding a remote that already exists with same URL"""
        repo_path = temp_repo_dir / "existing_remote_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)
        repo.create_remote("origin", "https://github.com/test/repo.git")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="add_remote",
            remote_url="https://github.com/test/repo.git",
            remote_name="origin"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert "already exists" in result.message.lower()

    def test_update_remote_url(self, git_agent, temp_repo_dir):
        """Test updating an existing remote's URL"""
        repo_path = temp_repo_dir / "update_remote_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)
        repo.create_remote("origin", "https://github.com/old/repo.git")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="add_remote",
            remote_url="https://github.com/new/repo.git",
            remote_name="origin"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert "updated" in result.message.lower()

        # Verify URL was updated
        repo = Repo(repo_path)
        assert repo.remote("origin").url == "https://github.com/new/repo.git"

    def test_get_status_clean_repo(self, git_agent, temp_repo_dir):
        """Test getting status of a clean repository"""
        repo_path = temp_repo_dir / "status_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Create initial commit
        test_file = repo_path / "test.txt"
        test_file.write_text("Initial")
        repo.index.add(["."])
        repo.index.commit("Initial commit")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="status"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert result.operation == "status"
        assert "branch" in result.message.lower()
        assert result.details["is_dirty"] == "False"

    def test_get_status_dirty_repo(self, git_agent, temp_repo_dir):
        """Test getting status of a dirty repository"""
        repo_path = temp_repo_dir / "dirty_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Create and commit initial file
        test_file = repo_path / "test.txt"
        test_file.write_text("Initial")
        repo.index.add(["."])
        repo.index.commit("Initial commit")

        # Modify file
        test_file.write_text("Modified")

        # Add untracked file
        untracked = repo_path / "untracked.txt"
        untracked.write_text("Untracked")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="status"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert result.details["is_dirty"] == "True"
        assert int(result.details["untracked_files"]) >= 1  # At least one untracked file
        assert result.details["modified_files"] == "1"

    def test_create_branch(self, git_agent, temp_repo_dir):
        """Test creating a new branch"""
        repo_path = temp_repo_dir / "branch_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Need at least one commit
        test_file = repo_path / "test.txt"
        test_file.write_text("Initial")
        repo.index.add(["."])
        repo.index.commit("Initial commit")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="create_branch",
            branch="feature-branch"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert "created" in result.message.lower()
        assert "feature-branch" in repo.branches

    def test_create_existing_branch(self, git_agent, temp_repo_dir):
        """Test creating a branch that already exists"""
        repo_path = temp_repo_dir / "existing_branch_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Need at least one commit
        test_file = repo_path / "test.txt"
        test_file.write_text("Initial")
        repo.index.add(["."])
        repo.index.commit("Initial commit")

        # Create branch first time
        repo.create_head("existing-branch")

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="create_branch",
            branch="existing-branch"
        )

        result = git_agent.execute(operation)

        assert result.success is True
        assert "already exists" in result.message.lower()

    def test_operation_validation(self, git_agent, temp_repo_dir):
        """Test that invalid operations are rejected"""
        repo_path = temp_repo_dir / "validation_repo"

        with pytest.raises(Exception):  # Pydantic validation error
            GitOperation(
                repo_path=str(repo_path),
                operation="invalid_operation"
            )

    def test_invalid_repository_path(self, git_agent, temp_repo_dir):
        """Test operations on non-existent repository paths"""
        non_existent = temp_repo_dir / "non_existent"

        operation = GitOperation(
            repo_path=str(non_existent),
            operation="commit",
            message="Test"
        )

        result = git_agent.execute(operation)

        assert result.success is False
        assert "not a valid" in result.message.lower() or "failed" in result.message.lower()

    def test_operation_logging(self, git_agent, temp_repo_dir):
        """Test that operations are logged to activity log"""
        repo_path = temp_repo_dir / "log_test_repo"

        operation = GitOperation(
            repo_path=str(repo_path),
            operation="init"
        )

        git_agent.execute(operation)

        # Verify log file was created and contains entry
        assert git_agent.log_file.exists()
        log_content = git_agent.log_file.read_text()
        assert "init" in log_content
        assert str(repo_path) in log_content

    def test_commit_specific_files(self, git_agent, temp_repo_dir):
        """Test committing only specific files"""
        repo_path = temp_repo_dir / "specific_files_repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Create multiple files
        file1 = repo_path / "file1.txt"
        file2 = repo_path / "file2.txt"
        file1.write_text("File 1")
        file2.write_text("File 2")

        # Commit only file1
        operation = GitOperation(
            repo_path=str(repo_path),
            operation="commit",
            message="Add file1",
            files=["file1.txt"]
        )

        result = git_agent.execute(operation)

        assert result.success is True

        # Verify file1 is committed but file2 is not
        repo = Repo(repo_path)
        committed_files = [item.path for item in repo.head.commit.tree.traverse()]
        assert "file1.txt" in committed_files
        # file2.txt should still be untracked
        assert "file2.txt" in repo.untracked_files


class TestGitOperationModel:
    """Test the GitOperation data model"""

    def test_default_values(self):
        """Test that default values are set correctly"""
        op = GitOperation(
            repo_path="/test/path",
            operation="init"
        )

        assert op.remote_name == "origin"
        assert op.branch == "main"
        assert op.files == ["."]
        assert op.force is False

    def test_custom_values(self):
        """Test setting custom values"""
        op = GitOperation(
            repo_path="/test/path",
            operation="push",
            remote_name="upstream",
            branch="develop",
            files=["src/"],
            force=True
        )

        assert op.remote_name == "upstream"
        assert op.branch == "develop"
        assert op.files == ["src/"]
        assert op.force is True


class TestGitResultModel:
    """Test the GitResult data model"""

    def test_result_creation(self):
        """Test creating a GitResult"""
        result = GitResult(
            success=True,
            operation="init",
            message="Repository initialized",
            details={"repo_path": "/test/path"}
        )

        assert result.success is True
        assert result.operation == "init"
        assert result.message == "Repository initialized"
        assert result.details["repo_path"] == "/test/path"
        assert result.timestamp is not None
