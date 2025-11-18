"""
GitOpsAgent - Handles all Git and GitHub operations safely

Manages repository initialization, commits, branches, and
remote operations with safety logging and confirmations.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import git
from git import Repo, InvalidGitRepositoryError, GitCommandError, NoSuchPathError, BadName

from code_factory.core.agent_runtime import BaseAgent, AgentExecutionError
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class GitOperation(BaseModel):
    """Input for Git operations"""
    repo_path: str = Field(..., description="Path to the repository")
    operation: str = Field(..., description="Operation: init, commit, add_remote, push, status")
    message: Optional[str] = Field(None, description="Commit message (for commit operations)")
    remote_url: Optional[str] = Field(None, description="Remote URL (for add_remote operations)")
    remote_name: str = Field("origin", description="Remote name")
    branch: str = Field("main", description="Branch name")
    files: List[str] = Field(default_factory=lambda: ["."], description="Files to stage (default: all)")
    force: bool = Field(False, description="Force operation (use with caution)")

    @field_validator("operation")
    @classmethod
    def validate_operation(cls, v: str) -> str:
        valid_ops = {"init", "commit", "add_remote", "push", "status", "create_branch"}
        if v not in valid_ops:
            raise ValueError(f"Invalid operation '{v}'. Must be one of: {valid_ops}")
        return v


class GitResult(BaseModel):
    """Result of Git operation"""
    success: bool
    operation: str
    message: str
    details: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class GitOpsAgent(BaseAgent):
    """Handles all Git and GitHub operations with safety logging"""

    def __init__(self, log_file: str = "git_activity.log"):
        self.log_file = Path(log_file)

    @property
    def name(self) -> str:
        return "git_ops"

    @property
    def description(self) -> str:
        return "Manages Git repositories and GitHub operations safely"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Execute Git operation

        Args:
            input_data: GitOperation specification

        Returns:
            GitResult: Operation result

        Raises:
            AgentExecutionError: If git operation fails
        """
        op = self.validate_input(input_data, GitOperation)
        logger.info(f"Git operation: {op.operation} on {op.repo_path}")

        # Log the operation
        self._log_operation(op)

        try:
            # Dispatch to appropriate operation handler
            if op.operation == "init":
                result = self._init_repo(op)
            elif op.operation == "commit":
                result = self._commit_changes(op)
            elif op.operation == "add_remote":
                result = self._add_remote(op)
            elif op.operation == "push":
                result = self._push_changes(op)
            elif op.operation == "status":
                result = self._get_status(op)
            elif op.operation == "create_branch":
                result = self._create_branch(op)
            else:
                raise ValueError(f"Unsupported operation: {op.operation}")

            logger.info(f"Git {op.operation} completed successfully")
            return result

        except Exception as e:
            error_msg = f"Git operation '{op.operation}' failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return GitResult(
                success=False,
                operation=op.operation,
                message=error_msg,
                details={"error_type": type(e).__name__}
            )

    def _init_repo(self, op: GitOperation) -> GitResult:
        """Initialize a new Git repository"""
        repo_path = Path(op.repo_path)

        try:
            # Check if already a git repo
            try:
                existing_repo = Repo(repo_path)
                return GitResult(
                    success=True,
                    operation="init",
                    message=f"Repository already initialized at {repo_path}",
                    details={"repo_path": str(repo_path), "status": "already_exists"}
                )
            except (InvalidGitRepositoryError, NoSuchPathError):
                # Not a repo yet, create it
                pass

            # Create directory if it doesn't exist
            repo_path.mkdir(parents=True, exist_ok=True)

            # Initialize repository
            repo = Repo.init(repo_path)

            return GitResult(
                success=True,
                operation="init",
                message=f"Initialized Git repository at {repo_path}",
                details={
                    "repo_path": str(repo_path),
                    "git_dir": str(repo.git_dir)
                }
            )
        except Exception as e:
            raise AgentExecutionError(f"Failed to initialize repository: {e}")

    def _commit_changes(self, op: GitOperation) -> GitResult:
        """Stage files and create a commit"""
        try:
            repo = Repo(op.repo_path)

            if not op.message:
                raise ValueError("Commit message is required for commit operation")

            # Stage files
            # Handle explicit empty list (don't stage) vs default (stage all)
            files_to_add = []
            if op.files is not None and len(op.files) == 0:
                # Explicit empty list means don't stage anything
                files_to_add = []
            elif op.files and len(op.files) > 0:
                # Specific files to stage
                files_to_add = op.files
                repo.index.add(op.files)
            else:
                # Default behavior: stage all changes
                files_to_add = ["."]
                repo.index.add(["."])

            # Check if there are changes to commit
            # Need to handle case when there are no commits yet (HEAD doesn't exist)
            try:
                has_staged_changes = bool(repo.index.diff("HEAD"))
            except (BadName, ValueError):
                # No HEAD means this is the first commit, so staged changes exist
                has_staged_changes = True

            # If no files were added and there are no changes, don't commit
            if len(files_to_add) == 0 and not has_staged_changes:
                return GitResult(
                    success=True,
                    operation="commit",
                    message="No changes to commit",
                    details={"status": "no_changes"}
                )

            if not has_staged_changes and not repo.untracked_files:
                return GitResult(
                    success=True,
                    operation="commit",
                    message="No changes to commit",
                    details={"status": "no_changes"}
                )

            # Create commit
            commit = repo.index.commit(op.message)

            return GitResult(
                success=True,
                operation="commit",
                message=f"Created commit: {commit.hexsha[:7]}",
                details={
                    "commit_sha": commit.hexsha,
                    "commit_message": op.message,
                    "files_staged": str(len(files_to_add))
                }
            )
        except InvalidGitRepositoryError:
            raise AgentExecutionError(f"Not a valid Git repository: {op.repo_path}")
        except Exception as e:
            raise AgentExecutionError(f"Failed to commit changes: {e}")

    def _add_remote(self, op: GitOperation) -> GitResult:
        """Add a remote repository"""
        try:
            repo = Repo(op.repo_path)

            if not op.remote_url:
                raise ValueError("Remote URL is required for add_remote operation")

            # Check if remote already exists
            if op.remote_name in [r.name for r in repo.remotes]:
                existing_remote = repo.remote(op.remote_name)
                # Update URL if different
                if existing_remote.url != op.remote_url:
                    repo.delete_remote(op.remote_name)
                    remote = repo.create_remote(op.remote_name, op.remote_url)
                    return GitResult(
                        success=True,
                        operation="add_remote",
                        message=f"Updated remote '{op.remote_name}' to {op.remote_url}",
                        details={"remote_name": op.remote_name, "url": op.remote_url}
                    )
                else:
                    return GitResult(
                        success=True,
                        operation="add_remote",
                        message=f"Remote '{op.remote_name}' already exists with same URL",
                        details={"remote_name": op.remote_name, "url": op.remote_url}
                    )

            # Create new remote
            remote = repo.create_remote(op.remote_name, op.remote_url)

            return GitResult(
                success=True,
                operation="add_remote",
                message=f"Added remote '{op.remote_name}': {op.remote_url}",
                details={"remote_name": op.remote_name, "url": op.remote_url}
            )
        except InvalidGitRepositoryError:
            raise AgentExecutionError(f"Not a valid Git repository: {op.repo_path}")
        except Exception as e:
            raise AgentExecutionError(f"Failed to add remote: {e}")

    def _push_changes(self, op: GitOperation) -> GitResult:
        """Push commits to remote repository"""
        try:
            repo = Repo(op.repo_path)

            # Get the remote
            if op.remote_name not in [r.name for r in repo.remotes]:
                raise ValueError(f"Remote '{op.remote_name}' not found")

            remote = repo.remote(op.remote_name)

            # Push to remote
            push_args = [f"{op.branch}:{op.branch}"]
            if op.force:
                push_args.append("--force")

            push_info = remote.push(refspec=op.branch)

            # Check push result
            if push_info and push_info[0].flags & push_info[0].ERROR:
                raise GitCommandError("push", f"Push failed: {push_info[0].summary}")

            return GitResult(
                success=True,
                operation="push",
                message=f"Pushed to {op.remote_name}/{op.branch}",
                details={
                    "remote": op.remote_name,
                    "branch": op.branch,
                    "forced": str(op.force)
                }
            )
        except InvalidGitRepositoryError:
            raise AgentExecutionError(f"Not a valid Git repository: {op.repo_path}")
        except Exception as e:
            raise AgentExecutionError(f"Failed to push changes: {e}")

    def _get_status(self, op: GitOperation) -> GitResult:
        """Get repository status"""
        try:
            repo = Repo(op.repo_path)

            # Get branch name safely
            try:
                branch_name = repo.active_branch.name if repo.head.is_valid() else "No commits yet"
            except (TypeError, ValueError):
                branch_name = "No commits yet"

            # Get status information
            # Handle case when there are no commits yet
            try:
                staged_files_count = len([item.a_path for item in repo.index.diff("HEAD")])
            except (BadName, ValueError):
                # No HEAD means no commits yet
                staged_files_count = len(repo.index.entries)

            status_info = {
                "branch": branch_name,
                "is_dirty": str(repo.is_dirty()),
                "untracked_files": str(len(repo.untracked_files)),
                "modified_files": str(len([item.a_path for item in repo.index.diff(None)])),
                "staged_files": str(staged_files_count)
            }

            # Build status message
            status_lines = [
                f"Branch: {status_info['branch']}",
                f"Modified files: {status_info['modified_files']}",
                f"Staged files: {status_info['staged_files']}",
                f"Untracked files: {status_info['untracked_files']}"
            ]

            return GitResult(
                success=True,
                operation="status",
                message="\n".join(status_lines),
                details=status_info
            )
        except InvalidGitRepositoryError:
            raise AgentExecutionError(f"Not a valid Git repository: {op.repo_path}")
        except Exception as e:
            raise AgentExecutionError(f"Failed to get status: {e}")

    def _create_branch(self, op: GitOperation) -> GitResult:
        """Create a new branch"""
        try:
            repo = Repo(op.repo_path)

            # Check if branch already exists
            if op.branch in repo.branches:
                return GitResult(
                    success=True,
                    operation="create_branch",
                    message=f"Branch '{op.branch}' already exists",
                    details={"branch": op.branch, "status": "already_exists"}
                )

            # Create new branch
            new_branch = repo.create_head(op.branch)

            return GitResult(
                success=True,
                operation="create_branch",
                message=f"Created branch '{op.branch}'",
                details={"branch": op.branch}
            )
        except InvalidGitRepositoryError:
            raise AgentExecutionError(f"Not a valid Git repository: {op.repo_path}")
        except Exception as e:
            raise AgentExecutionError(f"Failed to create branch: {e}")

    def _log_operation(self, operation: GitOperation) -> None:
        """Log Git operation to activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {operation.operation} - {operation.repo_path}\n"

        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.log_file, "a") as f:
            f.write(log_entry)
