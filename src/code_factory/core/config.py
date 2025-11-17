"""
Configuration management for the Code Factory

Centralizes all configuration settings with environment variable support
and sensible defaults. This ensures portability across platforms and
proper separation of environment-specific values.
"""

import os
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Config:
    """
    Configuration manager for the Code Factory

    Handles configuration loading from multiple sources with precedence:
    1. Explicit parameters (highest priority)
    2. Environment variables
    3. Default values (lowest priority)
    """

    # Environment variable names
    ENV_PROJECTS_DIR = "CODE_FACTORY_PROJECTS_DIR"
    ENV_LOG_LEVEL = "CODE_FACTORY_LOG_LEVEL"

    # Default values
    DEFAULT_PROJECTS_DIR = Path.home() / ".code-factory" / "projects"
    DEFAULT_LOG_LEVEL = "INFO"

    def __init__(self):
        """Initialize configuration with defaults"""
        self._projects_dir: Optional[Path] = None
        self._log_level: str = self.DEFAULT_LOG_LEVEL
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Load configuration from environment variables"""
        # Load projects directory
        projects_dir_str = os.getenv(self.ENV_PROJECTS_DIR)
        if projects_dir_str:
            self._projects_dir = Path(projects_dir_str).expanduser().resolve()
            logger.debug(f"Loaded projects_dir from env: {self._projects_dir}")

        # Load log level
        log_level = os.getenv(self.ENV_LOG_LEVEL)
        if log_level:
            self._log_level = log_level.upper()
            logger.debug(f"Loaded log_level from env: {self._log_level}")

    @property
    def projects_dir(self) -> Path:
        """
        Get the projects directory path

        Returns the projects directory from:
        1. Explicitly set value (via set_projects_dir)
        2. Environment variable CODE_FACTORY_PROJECTS_DIR
        3. Default: ~/.code-factory/projects

        Returns:
            Path: The projects directory path
        """
        if self._projects_dir is None:
            self._projects_dir = self.DEFAULT_PROJECTS_DIR
        return self._projects_dir

    def set_projects_dir(self, path: str | Path) -> None:
        """
        Explicitly set the projects directory

        This takes precedence over environment variables and defaults.

        Args:
            path: Path to the projects directory
        """
        self._projects_dir = Path(path).expanduser().resolve()
        logger.info(f"Projects directory set to: {self._projects_dir}")

    @property
    def log_level(self) -> str:
        """
        Get the log level

        Returns:
            str: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        return self._log_level

    def set_log_level(self, level: str) -> None:
        """
        Set the log level

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._log_level = level.upper()
        logger.info(f"Log level set to: {self._log_level}")

    def ensure_projects_dir(self) -> Path:
        """
        Ensure the projects directory exists

        Creates the directory and any parent directories if they don't exist.

        Returns:
            Path: The projects directory path

        Raises:
            OSError: If directory creation fails
        """
        projects_path = self.projects_dir

        if not projects_path.exists():
            logger.info(f"Creating projects directory: {projects_path}")
            try:
                projects_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Successfully created: {projects_path}")
            except OSError as e:
                logger.error(f"Failed to create projects directory: {e}")
                raise
        else:
            logger.debug(f"Projects directory already exists: {projects_path}")

        # Verify it's actually a directory
        if not projects_path.is_dir():
            raise OSError(f"Projects path exists but is not a directory: {projects_path}")

        return projects_path

    def get_config_summary(self) -> dict:
        """
        Get a summary of current configuration

        Returns:
            dict: Configuration summary
        """
        return {
            "projects_dir": str(self.projects_dir),
            "projects_dir_exists": self.projects_dir.exists(),
            "log_level": self.log_level,
            "env_variables": {
                self.ENV_PROJECTS_DIR: os.getenv(self.ENV_PROJECTS_DIR),
                self.ENV_LOG_LEVEL: os.getenv(self.ENV_LOG_LEVEL),
            }
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance

    Returns:
        Config: The global configuration object
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reset_config() -> None:
    """
    Reset the global configuration instance

    Useful for testing or when configuration needs to be reloaded.
    """
    global _config
    _config = None
