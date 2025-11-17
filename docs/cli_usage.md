# CLI Usage Guide

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/AgentOrchestratedCodeFactory.git
cd AgentOrchestratedCodeFactory

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/AgentOrchestratedCodeFactory.git
cd AgentOrchestratedCodeFactory

# Install dependencies
pip install -e ".[dev]"
```

## Commands

### `code-factory init`

Initialize or verify the factory environment.

```bash
# Use default projects directory (~/.code-factory/projects)
code-factory init

# Or specify a custom projects directory
code-factory init --projects-dir ~/my-projects

# Short flag version
code-factory init -d /path/to/projects
```

**What it does**:
- Checks Python version (requires 3.11+)
- Verifies all required directories exist
- Creates the projects directory if it doesn't exist
- Displays configuration information
- Shows configuration source (CLI flag, environment, or default)

**Options**:
- `--projects-dir, -d`: Override the projects directory path

**Example output**:
```
Initializing Code Factory...

✓ Python 3.11.5
✓ src/code_factory/core
✓ src/code_factory/agents
✓ src/code_factory/cli
✓ docs
✓ tests/unit
✓ tests/integration
✓ tests/e2e
✓ Git repository initialized

Projects Directory Configuration:
  Location: /home/user/.code-factory/projects
  Source: Default
✓ Projects directory ready

🎉 Factory is ready to use!

Configuration Tips:
  • Set projects directory via environment:
    export CODE_FACTORY_PROJECTS_DIR=/path/to/projects
  • Or use the --projects-dir flag with commands
  • Current projects directory: /home/user/.code-factory/projects
```

### `code-factory status`

Display current factory status and environment info.

```bash
# Use default configuration
code-factory status

# Or override projects directory
code-factory status --projects-dir ~/my-projects

# Short flag version
code-factory status -d /path/to/projects
```

**What it shows**:
- Python version and location
- Git status
- Projects directory (with configuration source)
- Available agents
- Recent activity (if any)

**Options**:
- `--projects-dir, -d`: Override the projects directory path

**Example output**:
```
Agent-Orchestrated Code Factory v0.1.0
============================================================

Environment:
  Python: 3.11.5 (/usr/local/bin/python3)
  Working Directory: /home/user/AgentOrchestratedCodeFactory
  Git: Initialized ✓
  Projects Directory: /home/user/.code-factory/projects ✓ (Default)

Available Agents:
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Agent              ┃ Description                          ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ safety_guard       │ Validates project safety boundaries  │
│ planner            │ Plans tasks from ideas               │
│ architect          │ Designs project architecture         │
│ implementer        │ Implements code from specifications  │
│ tester             │ Creates and runs tests               │
│ doc_writer         │ Generates project documentation      │
│ git_ops            │ Manages Git operations               │
│ blue_collar_advisor│ Ensures practical field usability    │
└────────────────────┴──────────────────────────────────────┘

Execution History: 0 runs

Status: Ready ✅
```

## Future Commands (Coming Soon)

### `code-factory build`

Build a project from an idea.

```bash
# From text description
code-factory build --idea "A tool to analyze PLC alarm logs"

# From idea file
code-factory build --file ideas/marine_log_analyzer.txt

# With specific output location
code-factory build --idea "HVAC load calculator" --output ~/Projects/HVACCalc
```

### `code-factory list-templates`

Show available project templates.

```bash
code-factory list-templates
```

### `code-factory agents`

List and manage agents.

```bash
# List all agents
code-factory agents list

# Get agent details
code-factory agents info planner

# Test an agent
code-factory agents test implementer
```

### `code-factory history`

View recent factory activity.

```bash
# Show last 10 builds
code-factory history

# Show detailed build info
code-factory history --build-id abc123
```

## Configuration

The Code Factory uses a flexible configuration system with three levels of precedence:

1. **CLI Flags** (highest priority) - Override configuration for a single command
2. **Environment Variables** - Persistent configuration for your session
3. **Default Values** (lowest priority) - Built-in sensible defaults

### Environment Variables

Set these in your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) for persistent configuration:

```bash
# Projects directory (where generated projects are stored)
export CODE_FACTORY_PROJECTS_DIR=~/my-projects

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export CODE_FACTORY_LOG_LEVEL=INFO
```

### CLI Flags

Override configuration on a per-command basis:

```bash
# Initialize with custom projects directory
code-factory init --projects-dir /path/to/projects

# Check status with custom directory
code-factory status --projects-dir /path/to/projects
```

### Default Values

If no configuration is provided:
- **Projects Directory**: `~/.code-factory/projects`
- **Log Level**: `INFO`

### Configuration Precedence Example

```bash
# Using defaults
code-factory init
# Projects directory: ~/.code-factory/projects

# Using environment variable
export CODE_FACTORY_PROJECTS_DIR=~/my-projects
code-factory init
# Projects directory: ~/my-projects

# Using CLI flag (overrides environment)
export CODE_FACTORY_PROJECTS_DIR=~/my-projects
code-factory init --projects-dir /tmp/test-projects
# Projects directory: /tmp/test-projects
```

### Future Configuration Features

File-based configuration will be added in a future release (`~/.code-factory/config.yaml`):

```yaml
# Future feature
projects_directory: ~/my-projects
github:
  auto_create_repo: true
  visibility: private
  use_ssh: true
agents:
  timeout_seconds: 300
  enable_parallel: false
safety:
  require_confirmation: true
```

## Tips

1. **Start simple**: Test with small ideas first
2. **Review generated code**: Always review before running in production
3. **Use version control**: Factory creates Git repos automatically
4. **Check logs**: Look at `git_activity.log` if something goes wrong
5. **Safety first**: Factory will ask before destructive operations
6. **Configure once**: Set `CODE_FACTORY_PROJECTS_DIR` in your shell profile for convenience

## Troubleshooting

### "Python version too old"
Upgrade to Python 3.11 or higher:
```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11

# Windows (use official installer)
# https://www.python.org/downloads/
```

### "Git not found"
Install Git:
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# Windows
# https://git-scm.com/download/win
```

### "Permission denied" or "Cannot create directory"
The projects directory may not be writable. Solutions:

1. **Use a directory you own**:
   ```bash
   code-factory init --projects-dir ~/my-projects
   ```

2. **Set environment variable**:
   ```bash
   export CODE_FACTORY_PROJECTS_DIR=~/my-projects
   code-factory init
   ```

3. **Check directory permissions**:
   ```bash
   # Make sure the parent directory exists and is writable
   mkdir -p ~/.code-factory
   chmod 755 ~/.code-factory
   ```

### "Agent execution failed"
Check logs for detailed error messages:
```bash
# Look for error details
cat logs/agent_runs.log

# Or increase log verbosity
export CODE_FACTORY_LOG_LEVEL=DEBUG
code-factory status
```

## Getting Help

```bash
# General help
code-factory --help

# Command-specific help
code-factory build --help
```

For more information:
- [Architecture Overview](architecture.md)
- [Agent Roles](agent_roles.md)
- [Safety Guidelines](safety.md)
