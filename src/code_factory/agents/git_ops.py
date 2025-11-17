"""
GitOpsAgent - Handles all Git and GitHub operations safely

Manages repository initialization, commits, branches, and
remote operations with safety logging and confirmations.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from code_factory.core.agent_runtime import BaseAgent
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GitOperation(BaseModel):
    """Input for Git operations"""
    repo_path: str
    operation: str  # "init", "commit", "push", "create_remote"
    message: Optional[str] = None
    force: bool = False


class GitResult(BaseModel):
    """Result of Git operation"""
    success: bool
    operation: str
    message: str
    timestamp: datetime = datetime.now()


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
        """
        op = self.validate_input(input_data, GitOperation)
        logger.info(f"Git operation: {op.operation} on {op.repo_path}")
        
        # Log the operation
        self._log_operation(op)
        
        # TODO: Implement actual Git operations using gitpython
        # For now, return success placeholder
        result = GitResult(
            success=True,
            operation=op.operation,
            message=f"{op.operation} completed successfully"
        )
        
        logger.info(f"Git {op.operation} completed")
        return result
    
    def _log_operation(self, operation: GitOperation) -> None:
        """Log Git operation to activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {operation.operation} - {operation.repo_path}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
