"""
Configuration management for Code Factory

Handles all configuration settings including paths, timeouts, and
environment-specific settings. Makes the application portable across platforms.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class FactoryConfig(BaseModel):
    """
    Central configuration for the Code Factory

    All configurable settings are defined here. Values can be overridden
    via environment variables or configuration files.
    """

    # Directory settings
    projects_dir: Path = Field(
        default_factory=lambda: Path.home() / "code-factory-projects",
        description="Root directory for generated projects"
    )

    checkpoint_dir: Path = Field(
        default_factory=lambda: Path.home() / ".code-factory" / "checkpoints",
        description="Directory for storing checkpoints"
    )

    staging_dir: Path = Field(
        default_factory=lambda: Path.home() / ".code-factory" / "staging",
        description="Temporary directory for work-in-progress"
    )

    # Timeout settings (in seconds)
    default_agent_timeout: int = Field(
        default=300,
        description="Default timeout for agent execution (5 minutes)"
    )

    safety_check_timeout: int = Field(
        default=30,
        description="Timeout for safety validation (30 seconds)"
    )

    llm_api_timeout: int = Field(
        default=120,
        description="Timeout for LLM API calls (2 minutes)"
    )

    # Retry settings
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for failed operations"
    )

    retry_backoff_base: float = Field(
        default=2.0,
        description="Base for exponential backoff (seconds)"
    )

    # Safety settings
    enable_safety_guard: bool = Field(
        default=True,
        description="Whether to enforce safety checks"
    )

    strict_safety_mode: bool = Field(
        default=True,
        description="Use strict safety validation with multiple layers"
    )

    # Testing settings
    enable_test_generation: bool = Field(
        default=True,
        description="Whether to generate tests automatically"
    )

    min_test_coverage: float = Field(
        default=80.0,
        description="Minimum test coverage percentage required"
    )

    # Git settings
    enable_git_ops: bool = Field(
        default=True,
        description="Whether to initialize Git repositories"
    )

    git_auto_commit: bool = Field(
        default=True,
        description="Automatically commit after each stage"
    )

    # Logging settings
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    enable_audit_log: bool = Field(
        default=True,
        description="Log all safety decisions for audit trail"
    )

    @field_validator("projects_dir", "checkpoint_dir", "staging_dir", mode="before")
    @classmethod
    def expand_path(cls, v) -> Path:
        """Expand environment variables and user home directory in paths"""
        if isinstance(v, str):
            v = os.path.expandvars(os.path.expanduser(v))
        return Path(v)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is valid"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v

    def ensure_directories(self) -> None:
        """Create required directories if they don't exist"""
        for dir_path in [self.projects_dir, self.checkpoint_dir, self.staging_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    class Config:
        """Pydantic configuration"""
        validate_assignment = True


def load_config(
    projects_dir: Optional[str] = None,
    config_file: Optional[Path] = None,
) -> FactoryConfig:
    """
    Load configuration from environment variables, config file, or defaults

    Priority order (highest to lowest):
    1. Explicit parameters passed to this function
    2. Environment variables (CODE_FACTORY_*)
    3. Configuration file
    4. Default values

    Args:
        projects_dir: Override projects directory
        config_file: Path to configuration file (JSON or YAML)

    Returns:
        FactoryConfig: Loaded configuration

    Environment variables:
        CODE_FACTORY_PROJECTS_DIR: Projects directory path
        CODE_FACTORY_DEFAULT_AGENT_TIMEOUT: Agent timeout in seconds
        CODE_FACTORY_ENABLE_SAFETY_GUARD: Enable/disable safety checks (true/false)
        CODE_FACTORY_LOG_LEVEL: Logging level
    """
    config_dict = {}

    # Load from environment variables
    env_mappings = {
        "CODE_FACTORY_PROJECTS_DIR": "projects_dir",
        "CODE_FACTORY_CHECKPOINT_DIR": "checkpoint_dir",
        "CODE_FACTORY_STAGING_DIR": "staging_dir",
        "CODE_FACTORY_DEFAULT_AGENT_TIMEOUT": "default_agent_timeout",
        "CODE_FACTORY_SAFETY_CHECK_TIMEOUT": "safety_check_timeout",
        "CODE_FACTORY_LLM_API_TIMEOUT": "llm_api_timeout",
        "CODE_FACTORY_MAX_RETRIES": "max_retries",
        "CODE_FACTORY_ENABLE_SAFETY_GUARD": "enable_safety_guard",
        "CODE_FACTORY_STRICT_SAFETY_MODE": "strict_safety_mode",
        "CODE_FACTORY_LOG_LEVEL": "log_level",
    }

    for env_var, config_key in env_mappings.items():
        value = os.environ.get(env_var)
        if value is not None:
            # Convert boolean strings
            if value.lower() in ("true", "1", "yes"):
                value = True
            elif value.lower() in ("false", "0", "no"):
                value = False
            # Convert numeric strings
            elif value.isdigit():
                value = int(value)

            config_dict[config_key] = value

    # Load from config file if provided
    if config_file and config_file.exists():
        import json
        with open(config_file) as f:
            file_config = json.load(f)
            # File config has lower priority than env vars
            config_dict = {**file_config, **config_dict}

    # Override with explicit parameters (highest priority)
    if projects_dir is not None:
        config_dict["projects_dir"] = projects_dir

    config = FactoryConfig(**config_dict)
    config.ensure_directories()

    return config


# Global config instance (can be overridden by calling load_config)
_config: Optional[FactoryConfig] = None


def get_config() -> FactoryConfig:
    """
    Get the current configuration instance

    Returns:
        FactoryConfig: Current configuration
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config


def set_config(config: FactoryConfig) -> None:
    """
    Set the global configuration instance

    Args:
        config: Configuration to use
    """
    global _config
    _config = config
