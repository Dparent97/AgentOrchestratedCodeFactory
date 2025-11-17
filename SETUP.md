# Setup Instructions

## Quick Start

### 1. Install Dependencies

Choose one of the following methods:

#### Option A: Using uv (Recommended - Fast)

```bash
cd /Users/dp/Projects/AgentOrchestratedCodeFactory

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Install in development mode
uv pip install -e ".[dev]"
```

#### Option B: Using pip (Traditional)

```bash
cd /Users/dp/Projects/AgentOrchestratedCodeFactory

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Initialize the factory
code-factory init

# Check status
code-factory status
```

Expected output should show:
- ✓ Python 3.11+ detected
- ✓ All required directories present
- ✓ List of available agents

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run just the smoke test
pytest tests/test_smoke.py -v

# Run with coverage
pytest tests/ --cov=code_factory --cov-report=html
```

### 4. Set Up GitHub Repository (Optional)

**DO NOT RUN THESE YET - Wait for confirmation!**

See `GITHUB_SETUP.md` for prepared commands.

## Development Workflow

### Running the CLI

```bash
# From anywhere if installed
code-factory status

# Or directly from the project
python -m code_factory.cli.main status
```

### Adding New Agents

1. Create new agent file in `src/code_factory/agents/`
2. Inherit from `BaseAgent`
3. Implement required methods
4. Register in `cli/main.py`'s `get_runtime()` function
5. Add tests in `tests/unit/agents/`

### Project Structure

```
AgentOrchestratedCodeFactory/
├── src/code_factory/         # Main source code
│   ├── core/                 # Core orchestration logic
│   ├── agents/               # Specialized agents
│   └── cli/                  # Command-line interface
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── docs/                     # Documentation
└── pyproject.toml            # Dependencies and config
```

## Troubleshooting

### "command not found: code-factory"

If the command isn't available after installation:

```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Or use the full path
python -m code_factory.cli.main status
```

### Import Errors

If you get import errors:

```bash
# Reinstall in development mode
pip install -e .
```

### Python Version Issues

The factory requires Python 3.11+:

```bash
# Check your version
python --version

# Install Python 3.11+ if needed (macOS)
brew install python@3.11
```

## Next Steps

After verifying the setup works:

1. Review the documentation in `docs/`
2. Run the test suite to ensure everything works
3. Follow instructions in GITHUB_SETUP.md to push to GitHub
4. Start implementing the full agent orchestration logic
