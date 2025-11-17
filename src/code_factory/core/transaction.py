"""
Transaction system for safe file operations

Provides transaction-like semantics for file system operations with
automatic rollback on failure. All operations are performed in a staging
area and only committed to final location on success.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable

from code_factory.core.config import get_config

logger = logging.getLogger(__name__)


class FileOperation:
    """Represents a single file system operation that can be rolled back"""

    def __init__(
        self,
        operation_type: str,
        target_path: Path,
        backup_path: Optional[Path] = None,
        content: Optional[str] = None,
    ):
        self.operation_type = operation_type  # create, modify, delete, move
        self.target_path = target_path
        self.backup_path = backup_path
        self.content = content
        self.timestamp = datetime.now()

    def rollback(self) -> None:
        """Undo this operation"""
        try:
            if self.operation_type == "create":
                # Delete the created file
                if self.target_path.exists():
                    if self.target_path.is_dir():
                        shutil.rmtree(self.target_path)
                    else:
                        self.target_path.unlink()
                    logger.info(f"Rolled back create: {self.target_path}")

            elif self.operation_type == "modify":
                # Restore from backup
                if self.backup_path and self.backup_path.exists():
                    shutil.copy2(self.backup_path, self.target_path)
                    logger.info(f"Rolled back modify: {self.target_path}")

            elif self.operation_type == "delete":
                # Restore from backup
                if self.backup_path and self.backup_path.exists():
                    if self.backup_path.is_dir():
                        shutil.copytree(self.backup_path, self.target_path)
                    else:
                        shutil.copy2(self.backup_path, self.target_path)
                    logger.info(f"Rolled back delete: {self.target_path}")

            elif self.operation_type == "move":
                # Move back
                if self.backup_path and self.target_path.exists():
                    shutil.move(str(self.target_path), str(self.backup_path))
                    logger.info(f"Rolled back move: {self.target_path}")

        except Exception as e:
            logger.error(f"Failed to rollback operation: {e}")
            raise


class Transaction:
    """
    Manages a transaction of file system operations

    Usage:
        with Transaction(project_root) as txn:
            txn.create_file(path, content)
            txn.modify_file(path, new_content)
            # ... more operations
            # Automatically commits on successful exit
            # Automatically rolls back on exception
    """

    def __init__(self, working_dir: Path, enable_staging: bool = True):
        """
        Initialize transaction

        Args:
            working_dir: Root directory for operations
            enable_staging: Use staging directory (True) or work directly (False)
        """
        self.working_dir = Path(working_dir)
        self.enable_staging = enable_staging
        self.config = get_config()

        # Staging directory for work-in-progress
        if enable_staging:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.staging_dir = self.config.staging_dir / f"txn_{timestamp}"
        else:
            self.staging_dir = self.working_dir

        # Backup directory for rollback
        self.backup_dir = self.config.staging_dir / "backups" / f"txn_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Track all operations for rollback
        self.operations: List[FileOperation] = []

        # Transaction state
        self.active = False
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        """Start transaction"""
        self.active = True

        # Create staging and backup directories
        if self.enable_staging:
            self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Transaction started: {self.staging_dir}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End transaction - commit or rollback"""
        if exc_type is not None:
            # Exception occurred - rollback
            logger.error(f"Transaction failed: {exc_val}")
            self.rollback()
            return False  # Re-raise the exception

        # No exception - commit
        try:
            self.commit()
        except Exception as e:
            logger.error(f"Commit failed: {e}")
            self.rollback()
            raise

        return False

    def create_file(self, relative_path: Path, content: str) -> None:
        """
        Create a new file

        Args:
            relative_path: Path relative to working directory
            content: File content
        """
        if not self.active:
            raise RuntimeError("Transaction not active")

        target_path = self.staging_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        target_path.write_text(content, encoding="utf-8")

        self.operations.append(
            FileOperation("create", target_path, content=content)
        )

        logger.debug(f"Created file: {relative_path}")

    def create_directory(self, relative_path: Path) -> None:
        """
        Create a new directory

        Args:
            relative_path: Path relative to working directory
        """
        if not self.active:
            raise RuntimeError("Transaction not active")

        target_path = self.staging_dir / relative_path
        target_path.mkdir(parents=True, exist_ok=True)

        self.operations.append(FileOperation("create", target_path))

        logger.debug(f"Created directory: {relative_path}")

    def modify_file(self, relative_path: Path, new_content: str) -> None:
        """
        Modify an existing file

        Args:
            relative_path: Path relative to working directory
            new_content: New file content
        """
        if not self.active:
            raise RuntimeError("Transaction not active")

        target_path = self.staging_dir / relative_path

        # Backup existing file if it exists
        backup_path = None
        if target_path.exists():
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, backup_path)

        target_path.write_text(new_content, encoding="utf-8")

        self.operations.append(
            FileOperation("modify", target_path, backup_path, new_content)
        )

        logger.debug(f"Modified file: {relative_path}")

    def delete_file(self, relative_path: Path) -> None:
        """
        Delete a file

        Args:
            relative_path: Path relative to working directory
        """
        if not self.active:
            raise RuntimeError("Transaction not active")

        target_path = self.staging_dir / relative_path

        # Backup before deleting
        backup_path = None
        if target_path.exists():
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, backup_path)

            target_path.unlink()

            self.operations.append(
                FileOperation("delete", target_path, backup_path)
            )

            logger.debug(f"Deleted file: {relative_path}")

    def commit(self) -> None:
        """
        Commit the transaction

        Moves all files from staging to final destination.
        """
        if not self.active:
            raise RuntimeError("Transaction not active")

        if self.committed:
            logger.warning("Transaction already committed")
            return

        logger.info(f"Committing transaction: {len(self.operations)} operations")

        try:
            if self.enable_staging and self.staging_dir != self.working_dir:
                # Copy from staging to final destination
                if self.staging_dir.exists():
                    self.working_dir.mkdir(parents=True, exist_ok=True)

                    # Copy all files from staging to working directory
                    for item in self.staging_dir.rglob("*"):
                        if item.is_file():
                            relative_path = item.relative_to(self.staging_dir)
                            target_path = self.working_dir / relative_path
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, target_path)

            self.committed = True
            self.active = False

            # Clean up staging directory
            if self.enable_staging and self.staging_dir.exists():
                shutil.rmtree(self.staging_dir)

            logger.info("Transaction committed successfully")

        except Exception as e:
            logger.error(f"Failed to commit transaction: {e}")
            raise

    def rollback(self) -> None:
        """
        Rollback the transaction

        Undoes all operations in reverse order.
        """
        if self.rolled_back:
            logger.warning("Transaction already rolled back")
            return

        logger.warning(f"Rolling back transaction: {len(self.operations)} operations")

        # Rollback operations in reverse order
        for operation in reversed(self.operations):
            try:
                operation.rollback()
            except Exception as e:
                logger.error(f"Failed to rollback operation: {e}")

        self.rolled_back = True
        self.active = False

        # Clean up staging directory
        if self.enable_staging and self.staging_dir.exists():
            try:
                shutil.rmtree(self.staging_dir)
            except Exception as e:
                logger.error(f"Failed to clean up staging directory: {e}")

        logger.info("Transaction rolled back")

    def get_staging_path(self, relative_path: Path) -> Path:
        """
        Get the full staging path for a relative path

        Args:
            relative_path: Path relative to working directory

        Returns:
            Path: Full path in staging directory
        """
        return self.staging_dir / relative_path
