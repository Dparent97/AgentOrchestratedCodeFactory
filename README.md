# Agent-Orchestrated Code Factory

> **A meta-agent system that transforms ideas into working software**

The Agent-Orchestrated Code Factory is an intelligent code generation system that takes plain-language project ideas and orchestrates multiple specialized agents to design, build, test, and document complete software projects.

## 🎯 Vision

Build practical tools that help real workers—marine engineers, plant operators, HVAC technicians, mechanics, and industrial troubleshooters—solve everyday problems with custom software generated in hours, not weeks.

## ✨ Features

- **Plain-language input**: Describe what you want to build in simple terms
- **Intelligent architecture**: Automatic project structure and technology selection
- **Multi-agent orchestration**: Specialized agents for planning, coding, testing, and documentation
- **Blue-collar focus**: Optimized for building tools that work in harsh environments with practical constraints
- **Safety-first**: Multi-layer security validation with bypass detection
- **Git integration**: Automatic version control and GitHub repository management
- **Cross-platform**: Portable configuration system works on Windows, Linux, and macOS
- **Timeout protection**: Prevents runaway processes with configurable timeouts
- **Transaction safety**: Rollback mechanism for error recovery
- **Comprehensive testing**: >70% test coverage with automated safety checks

## 🚀 Quick Start

```bash
# Install dependencies (using uv)
uv sync

# Or with pip
pip install -e ".[dev]"

# Initialize the factory
code-factory init

# Check system status
code-factory status

# Run tests with coverage
pytest

# (More commands coming soon)
```

## ⚙️ Configuration

The factory can be configured via environment variables:

```bash
# Set custom projects directory
export CODE_FACTORY_PROJECTS_DIR="~/my-projects"

# Set agent timeout (in seconds)
export CODE_FACTORY_DEFAULT_AGENT_TIMEOUT=600

# Disable safety guard (not recommended)
export CODE_FACTORY_ENABLE_SAFETY_GUARD=false

# Set log level
export CODE_FACTORY_LOG_LEVEL=DEBUG
```

See [docs/configuration.md](docs/configuration.md) for all available options.

## 📋 Requirements

- Python 3.11 or higher
- Git
- GitHub CLI (`gh`) or SSH access to GitHub (optional, for remote repos)
- macOS, Linux, or WSL2

## 🏗️ Architecture

The factory consists of several specialized agents:

- **Orchestrator**: Coordinates the entire build process
- **PlannerAgent**: Breaks ideas into actionable tasks
- **ArchitectAgent**: Designs project structure and technology choices
- **ImplementerAgent**: Writes the actual code
- **TesterAgent**: Creates and runs tests
- **DocWriterAgent**: Generates documentation
- **GitOpsAgent**: Manages version control
- **BlueCollarAdvisor**: Ensures solutions are practical for field use
- **SafetyGuard**: Enforces safety boundaries

See [docs/architecture.md](docs/architecture.md) for details.

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [CLI Usage Guide](docs/cli_usage.md)
- [Agent Roles](docs/agent_roles.md)
- [Safety Guidelines](docs/safety.md)

## 🔒 Safety

This system implements multiple layers of security:

- **Input normalization**: Prevents obfuscation-based bypasses
- **Regex pattern matching**: Detects dangerous operations with variations
- **Semantic analysis**: Understands context and intent
- **Audit logging**: Complete trail of all safety decisions
- **Bypass detection**: Identifies and blocks evasion attempts

This system is designed for **decision support and tool building only**. It does not:
- Control real-world equipment or machinery
- Generate exploit code or malicious software
- Modify files outside designated project directories

All generated tools are for analysis, documentation, and human-in-the-loop workflows.

See [docs/safety.md](docs/safety.md) for detailed security information.

## 🤝 Contributing

This is currently an internal project under active development.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
