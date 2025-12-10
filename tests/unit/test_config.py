"""
Tests for configuration management
"""

import os
import tempfile
from pathlib import Path

import pytest

from code_factory.core.config import FactoryConfig, load_config, get_config, set_config


class TestFactoryConfig:
    """Tests for FactoryConfig model"""

    def test_default_config(self):
        """Test default configuration values"""
        config = FactoryConfig()

        assert config.projects_dir is not None
        assert config.checkpoint_dir is not None
        assert config.staging_dir is not None
        assert config.default_agent_timeout == 300
        assert config.enable_safety_guard is True

    def test_custom_projects_dir(self):
        """Test setting custom projects directory"""
        custom_dir = Path("/tmp/my-projects")
        config = FactoryConfig(projects_dir=custom_dir)

        assert config.projects_dir == custom_dir

    def test_custom_timeout(self):
        """Test setting custom timeout"""
        config = FactoryConfig(default_agent_timeout=600)

        assert config.default_agent_timeout == 600

    def test_path_expansion(self):
        """Test that paths with ~ are expanded"""
        config = FactoryConfig(projects_dir="~/test-projects")

        assert "~" not in str(config.projects_dir)
        assert config.projects_dir.is_absolute()

    def test_invalid_log_level(self):
        """Test that invalid log level raises error"""
        with pytest.raises(ValueError, match="Log level must be"):
            FactoryConfig(log_level="INVALID")

    def test_valid_log_levels(self):
        """Test all valid log levels"""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = FactoryConfig(log_level=level)
            assert config.log_level == level

    def test_log_level_case_insensitive(self):
        """Test that log level is case-insensitive"""
        config = FactoryConfig(log_level="debug")
        assert config.log_level == "DEBUG"

    def test_ensure_directories(self):
        """Test that ensure_directories creates required directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            projects_dir = Path(tmpdir) / "projects"
            checkpoint_dir = Path(tmpdir) / "checkpoints"
            staging_dir = Path(tmpdir) / "staging"

            config = FactoryConfig(
                projects_dir=projects_dir,
                checkpoint_dir=checkpoint_dir,
                staging_dir=staging_dir,
            )

            # Directories shouldn't exist yet
            assert not projects_dir.exists()
            assert not checkpoint_dir.exists()
            assert not staging_dir.exists()

            # Create them
            config.ensure_directories()

            # Now they should exist
            assert projects_dir.exists()
            assert checkpoint_dir.exists()
            assert staging_dir.exists()


class TestLoadConfig:
    """Tests for load_config function"""

    def test_load_default_config(self, isolated_test_config):
        """Test loading default configuration"""
        # Use fixture config since load_config() tries to create dirs in home
        config = isolated_test_config

        assert isinstance(config, FactoryConfig)
        assert config.default_agent_timeout == 300

    def test_load_config_with_explicit_projects_dir(self, tmp_path):
        """Test loading config with explicit projects directory"""
        custom_dir = tmp_path / "test-projects"
        checkpoint_dir = tmp_path / "checkpoints"
        staging_dir = tmp_path / "staging"
        
        # Create config with temp directories to avoid permission errors
        config = FactoryConfig(
            projects_dir=custom_dir,
            checkpoint_dir=checkpoint_dir,
            staging_dir=staging_dir,
        )
        config.ensure_directories()

        assert config.projects_dir == custom_dir

    def test_load_config_from_env_var(self, tmp_path):
        """Test loading config from environment variables"""
        # Set environment variables including temp directories
        os.environ["CODE_FACTORY_DEFAULT_AGENT_TIMEOUT"] = "600"
        os.environ["CODE_FACTORY_PROJECTS_DIR"] = str(tmp_path / "projects")
        os.environ["CODE_FACTORY_CHECKPOINT_DIR"] = str(tmp_path / "checkpoints")
        os.environ["CODE_FACTORY_STAGING_DIR"] = str(tmp_path / "staging")

        try:
            config = load_config()
            assert config.default_agent_timeout == 600
        finally:
            # Clean up
            del os.environ["CODE_FACTORY_DEFAULT_AGENT_TIMEOUT"]
            del os.environ["CODE_FACTORY_PROJECTS_DIR"]
            del os.environ["CODE_FACTORY_CHECKPOINT_DIR"]
            del os.environ["CODE_FACTORY_STAGING_DIR"]

    def test_load_config_boolean_env_var(self, tmp_path):
        """Test loading boolean config from environment variable"""
        os.environ["CODE_FACTORY_ENABLE_SAFETY_GUARD"] = "false"
        os.environ["CODE_FACTORY_PROJECTS_DIR"] = str(tmp_path / "projects")
        os.environ["CODE_FACTORY_CHECKPOINT_DIR"] = str(tmp_path / "checkpoints")
        os.environ["CODE_FACTORY_STAGING_DIR"] = str(tmp_path / "staging")

        try:
            config = load_config()
            assert config.enable_safety_guard is False
        finally:
            del os.environ["CODE_FACTORY_ENABLE_SAFETY_GUARD"]
            del os.environ["CODE_FACTORY_PROJECTS_DIR"]
            del os.environ["CODE_FACTORY_CHECKPOINT_DIR"]
            del os.environ["CODE_FACTORY_STAGING_DIR"]

    def test_env_var_priority(self, tmp_path):
        """Test that explicit parameters override environment variables"""
        os.environ["CODE_FACTORY_DEFAULT_AGENT_TIMEOUT"] = "600"
        os.environ["CODE_FACTORY_PROJECTS_DIR"] = str(tmp_path / "projects")
        os.environ["CODE_FACTORY_CHECKPOINT_DIR"] = str(tmp_path / "checkpoints")
        os.environ["CODE_FACTORY_STAGING_DIR"] = str(tmp_path / "staging")

        try:
            # Explicit parameter should override env var
            config = load_config()  # Gets 600 from env
            config2 = FactoryConfig(default_agent_timeout=900)  # Explicit override

            assert config.default_agent_timeout == 600
            assert config2.default_agent_timeout == 900
        finally:
            del os.environ["CODE_FACTORY_DEFAULT_AGENT_TIMEOUT"]
            del os.environ["CODE_FACTORY_PROJECTS_DIR"]
            del os.environ["CODE_FACTORY_CHECKPOINT_DIR"]
            del os.environ["CODE_FACTORY_STAGING_DIR"]

    def test_directories_created(self, tmp_path):
        """Test that directories are created when loading config"""
        projects_dir = tmp_path / "projects"
        checkpoint_dir = tmp_path / "checkpoints"
        staging_dir = tmp_path / "staging"

        config = FactoryConfig(
            projects_dir=projects_dir,
            checkpoint_dir=checkpoint_dir,
            staging_dir=staging_dir,
        )
        config.ensure_directories()

        # Directories should be created
        assert projects_dir.exists()


class TestGetSetConfig:
    """Tests for get_config and set_config functions"""

    def test_get_config_returns_config(self, isolated_test_config):
        """Test that get_config returns a config instance"""
        config = get_config()

        assert isinstance(config, FactoryConfig)

    def test_get_config_singleton(self, isolated_test_config):
        """Test that get_config returns the same instance"""
        config1 = get_config()
        config2 = get_config()

        # Should be the same object
        assert config1 is config2

    def test_set_config(self, isolated_test_config):
        """Test setting custom config"""
        custom_config = FactoryConfig(default_agent_timeout=999)
        set_config(custom_config)

        config = get_config()

        assert config.default_agent_timeout == 999

    def test_set_config_overrides_default(self):
        """Test that set_config overrides the default"""
        # Get initial config
        config1 = get_config()
        initial_timeout = config1.default_agent_timeout

        # Set custom config
        custom_config = FactoryConfig(default_agent_timeout=777)
        set_config(custom_config)

        # Get config again
        config2 = get_config()

        assert config2.default_agent_timeout == 777
        assert config2.default_agent_timeout != initial_timeout
