# Configuration Guide

The Agent-Orchestrated Code Factory supports flexible configuration through environment variables, configuration files, and runtime parameters.

## Configuration Priority

Configuration is loaded in the following order (highest priority first):

1. Explicit runtime parameters (passed to functions)
2. Environment variables (`CODE_FACTORY_*`)
3. Configuration file (JSON)
4. Default values

## Environment Variables

All configuration options can be set via environment variables with the `CODE_FACTORY_` prefix:

### Directory Settings

```bash
# Projects directory (where generated projects are stored)
export CODE_FACTORY_PROJECTS_DIR="~/my-projects"

# Checkpoint directory (for pipeline state saves)
export CODE_FACTORY_CHECKPOINT_DIR="~/.code-factory/checkpoints"

# Staging directory (for work-in-progress)
export CODE_FACTORY_STAGING_DIR="~/.code-factory/staging"
```

### Timeout Settings

```bash
# Default timeout for agent execution (seconds)
export CODE_FACTORY_DEFAULT_AGENT_TIMEOUT=300

# Timeout for safety checks (seconds)
export CODE_FACTORY_SAFETY_CHECK_TIMEOUT=30

# Timeout for LLM API calls (seconds) - for Phase 3
export CODE_FACTORY_LLM_API_TIMEOUT=120
```

### Retry Settings

```bash
# Maximum number of retries for failed operations
export CODE_FACTORY_MAX_RETRIES=3

# Base for exponential backoff (seconds)
export CODE_FACTORY_RETRY_BACKOFF_BASE=2.0
```

### Safety Settings

```bash
# Enable/disable safety guard (true/false)
export CODE_FACTORY_ENABLE_SAFETY_GUARD=true

# Use strict safety mode (true/false)
export CODE_FACTORY_STRICT_SAFETY_MODE=true
```

### Testing Settings

```bash
# Enable automatic test generation (true/false)
export CODE_FACTORY_ENABLE_TEST_GENERATION=true

# Minimum test coverage percentage required
export CODE_FACTORY_MIN_TEST_COVERAGE=80.0
```

### Git Settings

```bash
# Enable Git operations (true/false)
export CODE_FACTORY_ENABLE_GIT_OPS=true

# Automatically commit after each stage (true/false)
export CODE_FACTORY_GIT_AUTO_COMMIT=true
```

### Logging Settings

```bash
# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export CODE_FACTORY_LOG_LEVEL=INFO

# Enable audit logging for safety decisions (true/false)
export CODE_FACTORY_ENABLE_AUDIT_LOG=true
```

## Configuration File

You can also provide configuration via a JSON file:

```json
{
  "projects_dir": "~/my-projects",
  "default_agent_timeout": 600,
  "enable_safety_guard": true,
  "strict_safety_mode": true,
  "log_level": "DEBUG"
}
```

Load the configuration file:

```python
from code_factory.core.config import load_config

config = load_config(config_file="path/to/config.json")
```

## Programmatic Configuration

You can also create configuration programmatically:

```python
from pathlib import Path
from code_factory.core.config import FactoryConfig, set_config

# Create custom configuration
config = FactoryConfig(
    projects_dir=Path("~/my-projects"),
    default_agent_timeout=600,
    enable_safety_guard=True,
    log_level="DEBUG"
)

# Set as global configuration
set_config(config)
```

## Default Values

If no configuration is provided, the following defaults are used:

| Setting | Default Value |
|---------|---------------|
| projects_dir | `~/code-factory-projects` |
| checkpoint_dir | `~/.code-factory/checkpoints` |
| staging_dir | `~/.code-factory/staging` |
| default_agent_timeout | 300 seconds (5 minutes) |
| safety_check_timeout | 30 seconds |
| llm_api_timeout | 120 seconds (2 minutes) |
| max_retries | 3 |
| retry_backoff_base | 2.0 seconds |
| enable_safety_guard | true |
| strict_safety_mode | true |
| enable_test_generation | true |
| min_test_coverage | 80.0% |
| enable_git_ops | true |
| git_auto_commit | true |
| log_level | INFO |
| enable_audit_log | true |

## Best Practices

### Development Environment

For development, you may want more verbose logging and longer timeouts:

```bash
export CODE_FACTORY_LOG_LEVEL=DEBUG
export CODE_FACTORY_DEFAULT_AGENT_TIMEOUT=900
export CODE_FACTORY_ENABLE_AUDIT_LOG=true
```

### Production Environment

For production, use stricter settings:

```bash
export CODE_FACTORY_LOG_LEVEL=INFO
export CODE_FACTORY_STRICT_SAFETY_MODE=true
export CODE_FACTORY_ENABLE_SAFETY_GUARD=true
export CODE_FACTORY_MIN_TEST_COVERAGE=90.0
```

### CI/CD Environment

For CI/CD pipelines:

```bash
export CODE_FACTORY_PROJECTS_DIR="/tmp/code-factory-ci"
export CODE_FACTORY_DEFAULT_AGENT_TIMEOUT=300
export CODE_FACTORY_ENABLE_GIT_OPS=false
```

## Platform-Specific Notes

### Windows

On Windows, paths should use forward slashes or raw strings:

```bash
set CODE_FACTORY_PROJECTS_DIR=C:/Projects/code-factory
```

### macOS/Linux

On macOS and Linux, use standard Unix paths:

```bash
export CODE_FACTORY_PROJECTS_DIR=~/projects/code-factory
```

### WSL2

In WSL2, you can access Windows paths:

```bash
export CODE_FACTORY_PROJECTS_DIR=/mnt/c/Projects/code-factory
```

## Troubleshooting

### Configuration Not Loading

If your configuration isn't being applied:

1. Check that environment variables are set in the current shell
2. Verify the variable names have the `CODE_FACTORY_` prefix
3. For boolean values, use `true`/`false`, `1`/`0`, or `yes`/`no`
4. Check for typos in variable names

### Directory Permissions

If you encounter permission errors:

1. Ensure you have write access to configured directories
2. The factory will attempt to create directories if they don't exist
3. Check that parent directories exist and are writable

### Path Expansion

The factory automatically expands:
- `~` to your home directory
- Environment variables in paths (e.g., `$HOME/projects`)

If paths aren't expanding correctly, verify your shell environment.
