# Contributing to Agent-Orchestrated Code Factory

Thank you for your interest in contributing! This project uses a multi-agent development workflow to build an intelligent code generation system. Your contributions help make it better.

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- GitHub CLI (`gh`) optional but recommended
- A code editor (VS Code, PyCharm, Neovim, etc.)

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/Dparent97/AgentOrchestratedCodeFactory.git
cd AgentOrchestratedCodeFactory
```

2. **Install dependencies**

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e ".[dev]"
```

3. **Run tests**

```bash
pytest
```

4. **Check code quality**

```bash
# Linting
ruff check src/ tests/

# Formatting
black --check src/ tests/

# Type checking
mypy src/
```

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if it's already reported in [Issues](https://github.com/Dparent97/AgentOrchestratedCodeFactory/issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Any error messages or stack traces

### Suggesting Features

We welcome feature suggestions! Please:

1. Check existing issues/discussions first
2. Create an issue describing:
   - The problem you're trying to solve
   - Why existing features don't work
   - How you envision the solution
   - Who would benefit (users, developers, etc.)
   - Any blue-collar use cases it enables

### Submitting Changes

1. **Create a branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

2. **Make your changes**
   - Write clear, well-commented code
   - Follow existing code style (PEP 8, type hints)
   - Add tests for new features
   - Update documentation

3. **Test your changes**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/code_factory --cov-report=term-missing

# Run specific tests
pytest tests/unit/test_your_feature.py

# Check code quality
ruff check src/ tests/
black src/ tests/
mypy src/
```

4. **Commit your changes**

```bash
git add .
git commit -m "feat: brief description of feature"
```

**Commit Message Conventions:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

5. **Push and create Pull Request**

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear description of changes
- Why the change is needed
- Any testing done
- Screenshots (if UI/CLI output changes)
- Link to related issues

## Code Style

### Python Style Guide

- **PEP 8** compliance
- **Type hints** on all functions and methods
- **Docstrings** following Google style:
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """
      Brief description of function

      Args:
          param1: Description of param1
          param2: Description of param2

      Returns:
          Description of return value

      Raises:
          ValueError: When something is invalid
      """
      pass
  ```
- **Maximum line length**: 100 characters
- **Use ruff** for linting: `ruff check .`
- **Use black** for formatting: `black .`

### Project Structure

```
src/code_factory/
├── agents/          # Agent implementations
├── cli/             # CLI interface
└── core/            # Core infrastructure
    ├── agent_runtime.py
    ├── checkpoint.py
    ├── config.py
    ├── models.py
    ├── orchestrator.py
    └── transaction.py
```

## Testing

### Test Coverage

- All new features **must** have tests
- Aim for **>80%** code coverage
- Test edge cases and error handling
- Tests should be clear and well-documented

### Test Structure

```
tests/
├── unit/            # Unit tests for individual components
├── integration/     # Integration tests for agent interactions
├── e2e/             # End-to-end workflow tests
└── harness/         # Test harness and fixtures
```

### Writing Tests

```python
import pytest
from code_factory.agents.planner import PlannerAgent
from code_factory.core.models import Idea, PlanResult

def test_planner_generates_tasks():
    """Test that PlannerAgent generates valid task list"""
    planner = PlannerAgent()
    idea = Idea(
        description="Build a CSV parser",
        features=["Read CSV", "Parse data"]
    )

    result = planner.execute(idea)

    assert isinstance(result, PlanResult)
    assert len(result.tasks) > 0
    assert result.estimated_complexity in ["simple", "moderate", "complex"]
```

## Documentation

### Updating Documentation

- Update **README.md** for user-facing changes
- Update **docs/** for new features
- Add **docstrings** to all functions/classes
- Include **usage examples** in docs
- Update **AGENT_PROMPTS/** for agent-related changes

### Documentation Files

- `docs/architecture.md` - System architecture
- `docs/cli_usage.md` - CLI commands and usage
- `docs/agent_roles.md` - Agent descriptions
- `docs/safety.md` - Safety guidelines
- `docs/agents/` - Individual agent documentation

## Multi-Agent Development

This project uses a unique multi-agent workflow for development. See `AGENT_PROMPTS/` for details.

### Wave Structure

- **Wave 1**: Foundation agents (Planner, Architect)
- **Wave 2**: Code generation (Implementer, Tester, DocWriter)
- **Wave 3**: GitOps and polish

### Agent Roles

- **PlannerAgent**: Breaks ideas into tasks
- **ArchitectAgent**: Designs project structure
- **ImplementerAgent**: Generates code
- **TesterAgent**: Creates and runs tests
- **DocWriterAgent**: Generates documentation
- **GitOpsAgent**: Manages version control
- **BlueCollarAdvisor**: Ensures field-practical design
- **SafetyGuard**: Enforces safety boundaries

## Review Process

1. **Automated checks** - Tests, linting, type checking must pass
2. **Code review** - Maintainer reviews code quality
3. **Documentation review** - Docs are clear and complete
4. **Integration testing** - Changes work with existing system
5. **Merge to main** - After approval

## Code of Conduct

### Our Standards

- Be **respectful** and **professional**
- Focus on **solving real problems**
- **Welcome newcomers** and provide constructive feedback
- Remember: we're building tools for **real workers**
- **Blue-collar focus**: Practical, reliable, field-tested solutions

### Not Acceptable

- Harassment or discrimination
- Unconstructive criticism
- Off-topic discussions
- Spam or self-promotion
- Code that bypasses safety checks

## Safety and Security

This project implements comprehensive safety measures:

- **Multi-layer security** validation
- **Bypass detection** for obfuscation attempts
- **Audit logging** for all safety decisions
- **No destructive operations** on real equipment

**Do not**:
- Bypass or disable SafetyGuard
- Generate code for dangerous operations
- Create exploits or malicious software
- Access systems without authorization

See `docs/safety.md` for detailed guidelines.

## Questions?

- Check existing **issues** and **discussions**
- Review **AGENT_PROMPTS/** for agent documentation
- Create a new issue with the **"question"** label
- Join project discussions
- Be patient - maintainers are volunteers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project credits
- Wave completion summaries

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make this tool better for everyone!

*These guidelines ensure we build reliable, safe, and practical tools that work in real-world conditions.*
