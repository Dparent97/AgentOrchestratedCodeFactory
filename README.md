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
- **Safety-first**: Built-in safety guards and project scope boundaries
- **Git integration**: Automatic version control and GitHub repository management

## 🚀 Quick Start

```bash
# Install dependencies (using uv)
uv sync

# Or with pip
pip install -e ".[dev]"

# Initialize the factory
code-factory init

# Optional: Set custom projects directory
export CODE_FACTORY_PROJECTS_DIR=~/my-projects
# Or use the --projects-dir flag
code-factory init --projects-dir ~/my-projects

# Check system status
code-factory status

# (More commands coming soon)
```

## ⚙️ Configuration

The Code Factory uses a flexible configuration system:

1. **Environment Variables** (recommended for persistent settings):
   ```bash
   export CODE_FACTORY_PROJECTS_DIR=~/my-projects
   export CODE_FACTORY_LOG_LEVEL=INFO
   ```

2. **CLI Flags** (for per-command overrides):
   ```bash
   code-factory init --projects-dir /path/to/projects
   code-factory status --projects-dir /path/to/projects
   ```

3. **Default Values**:
   - Projects directory: `~/.code-factory/projects`
   - Log level: `INFO`

The configuration system automatically creates the projects directory if it doesn't exist.

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

This system is designed for **decision support and tool building only**. It does not:
- Control real-world equipment or machinery
- Generate exploit code or malicious software
- Modify files outside designated project directories

All generated tools are for analysis, documentation, and human-in-the-loop workflows.

## 🤝 Contributing

This is currently an internal project under active development.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
