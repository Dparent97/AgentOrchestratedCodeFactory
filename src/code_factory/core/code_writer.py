"""
Code Writer - Safe file writing with transaction support

Provides safe file writing operations using the transaction system
for rollback capability and error recovery.
"""

import logging
from pathlib import Path
from typing import Dict

from code_factory.core.transaction import Transaction

logger = logging.getLogger(__name__)


class CodeWriter:
    """
    Writes generated code files to disk safely

    Uses the transaction system to ensure all-or-nothing semantics:
    either all files are written successfully, or none are (with automatic rollback).
    """

    def __init__(self, project_root: Path):
        """
        Initialize code writer

        Args:
            project_root: Root directory for the project
        """
        self.project_root = Path(project_root)
        logger.info(f"CodeWriter initialized for: {self.project_root}")

    def write_project_files(
        self,
        files: Dict[str, str],
        enable_staging: bool = True
    ) -> None:
        """
        Write project files to disk with transaction safety

        Args:
            files: Dictionary mapping file paths to content
            enable_staging: Use staging directory (True) or write directly (False)

        Raises:
            RuntimeError: If writing fails
        """
        logger.info(f"Writing {len(files)} files to {self.project_root}")

        try:
            with Transaction(self.project_root, enable_staging=enable_staging) as txn:
                for file_path, content in files.items():
                    self._write_file(txn, file_path, content)

                logger.info(f"Successfully wrote {len(files)} files")

        except Exception as e:
            logger.error(f"Failed to write files: {e}")
            raise RuntimeError(f"Failed to write project files: {e}")

    def _write_file(self, transaction: Transaction, file_path: str, content: str) -> None:
        """
        Write a single file within a transaction

        Args:
            transaction: Active transaction
            file_path: Relative path to file
            content: File content
        """
        path = Path(file_path)

        # Create parent directories if needed
        if path.parent != Path("."):
            transaction.create_directory(path.parent)

        # Write the file
        transaction.create_file(path, content)

        logger.debug(f"Wrote file: {file_path} ({len(content)} bytes)")

    def create_project_structure(
        self,
        folder_structure: Dict[str, list],
        enable_staging: bool = True
    ) -> None:
        """
        Create project directory structure

        Args:
            folder_structure: Dict mapping directories to list of files
            enable_staging: Use staging directory

        Raises:
            RuntimeError: If creation fails
        """
        logger.info(f"Creating project structure with {len(folder_structure)} directories")

        try:
            with Transaction(self.project_root, enable_staging=enable_staging) as txn:
                for directory, _ in folder_structure.items():
                    if directory:  # Skip root directory
                        txn.create_directory(Path(directory))

                logger.info("Successfully created directory structure")

        except Exception as e:
            logger.error(f"Failed to create structure: {e}")
            raise RuntimeError(f"Failed to create project structure: {e}")

    def validate_project_structure(self) -> bool:
        """
        Validate that project structure exists

        Returns:
            bool: True if valid, False otherwise
        """
        if not self.project_root.exists():
            logger.warning(f"Project root does not exist: {self.project_root}")
            return False

        # Check for essential files
        essential_files = ["README.md", "pyproject.toml"]
        for file_name in essential_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                logger.warning(f"Missing essential file: {file_name}")
                return False

        logger.info("Project structure validation passed")
        return True

    def get_project_files(self) -> Dict[str, str]:
        """
        Read all project files from disk

        Returns:
            Dict mapping file paths to content
        """
        if not self.project_root.exists():
            logger.warning("Project root does not exist")
            return {}

        files = {}

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                # Skip common exclusions
                if any(part.startswith(".") for part in file_path.parts):
                    continue
                if "__pycache__" in file_path.parts:
                    continue

                # Read file content
                try:
                    relative_path = file_path.relative_to(self.project_root)
                    content = file_path.read_text(encoding="utf-8")
                    files[str(relative_path)] = content
                except Exception as e:
                    logger.warning(f"Could not read {file_path}: {e}")

        logger.info(f"Read {len(files)} files from project")
        return files
