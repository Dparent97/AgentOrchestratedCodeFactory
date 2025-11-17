# CLI Usage Guide

## Installation

### Using uv (recommended)

```bash
cd /Users/dp/Projects/AgentOrchestratedCodeFactory
uv sync
```

### Using pip

```bash
cd /Users/dp/Projects/AgentOrchestratedCodeFactory
pip install -e ".[dev]"
```

## Commands

### `code-factory init`

Initialize or verify the factory environment.

```bash
code-factory init
```

**What it does**:
- Checks Python version (requires 3.11+)
- Verifies all required directories exist
- Creates any missing configuration files
- Displays environment status

**Example output**:
```
✅ Python 3.11.5 detected
✅ All core directories present
✅ Configuration valid
🎉 Factory is ready to use!
```

### `code-factory status`

Display current factory status and environment info.

```bash
code-factory status
```

**What it shows**:
- Python version and location
- Git status
- Available agents
- Project directory location
- Recent activity (if any)

**Example output**:
```
Agent-Orchestrated Code Factory v0.1.0
=====================================

Environment:
  Python: 3.11.5 (/usr/local/bin/python3)
  Working Directory: /Users/dp/Projects/AgentOrchestratedCodeFactory
  Git: Initialized (clean)

Available Agents:
  ✓ PlannerAgent
  ✓ ArchitectAgent
  ✓ ImplementerAgent
  ✓ TesterAgent
  ✓ DocWriterAgent
  ✓ GitOpsAgent
  ✓ BlueCollarAdvisor
  ✓ SafetyGuard

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

Configuration is stored in `~/.code-factory/config.yaml` (future feature).

Example config:
```yaml
projects_directory: /Users/dp/Projects
github:
  auto_create_repo: true
  visibility: private
  use_ssh: true
agents:
  timeout_seconds: 300
  enable_parallel: false
safety:
  require_confirmation: true
  allowed_directories:
    - /Users/dp/Projects
```

## Environment Variables

- `CODE_FACTORY_HOME`: Override factory installation directory
- `CODE_FACTORY_PROJECTS`: Override projects directory (default: ~/Projects)
- `CODE_FACTORY_LOG_LEVEL`: Set log verbosity (DEBUG, INFO, WARNING, ERROR)

## Tips

1. **Start simple**: Test with small ideas first
2. **Review generated code**: Always review before running in production
3. **Use version control**: Factory creates Git repos automatically
4. **Check logs**: Look at `git_activity.log` if something goes wrong
5. **Safety first**: Factory will ask before destructive operations

## Troubleshooting

### "Python version too old"
Upgrade to Python 3.11 or higher: `brew install python@3.11`

### "Git not found"
Install Git: `brew install git`

### "Permission denied"
Check that `/Users/dp/Projects` exists and is writable

### "Agent execution failed"
Check `logs/agent_runs.log` for detailed error messages

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
