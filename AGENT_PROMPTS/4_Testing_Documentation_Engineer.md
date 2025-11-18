# Agent 4: Testing & Documentation Engineer

**Repository:** https://github.com/Dparent97/AgentOrchestratedCodeFactory
**Branch:** `claude/implement-testing-docs`
**Iteration:** Phase 3 - TesterAgent & DocWriterAgent Implementation
**Time Estimate:** 3-4 hours

---

## 🎯 Your Mission

Transform two placeholder agents (TesterAgent and DocWriterAgent) into real implementations that generate pytest test suites and comprehensive documentation for generated projects. You'll implement test generation from ProjectSpec, test execution with coverage reporting, and comprehensive documentation generation.

---

## 🔴 Current Problems

### Problem #1: TesterAgent Returns Mock Data

**File:** `src/code_factory/agents/tester.py`
**Lines:** 48-60
**Status:** Placeholder

**Current Code:**
```python
def execute(self, input_data: BaseModel) -> BaseModel:
    spec = self.validate_input(input_data, ProjectSpec)
    logger.info(f"Running tests for: {spec.name}")

    # TODO: Implement test generation and execution
    mock_results = {
        "tests_passed": 5,
        "tests_failed": 0,
        "coverage": 85.0
    }

    return TestOutput(
        tests_run=5,
        tests_passed=5,
        coverage_percent=85.0
    )
```

---

### Problem #2: DocWriterAgent Generates Minimal README

**File:** `src/code_factory/agents/doc_writer.py`
**Lines:** 47-82
**Status:** Basic README only

**Current Code:**
```python
def execute(self, input_data: BaseModel) -> BaseModel:
    spec = self.validate_input(input_data, ProjectSpec)
    logger.info(f"Writing documentation for: {spec.name}")

    # TODO: Implement comprehensive doc generation
    readme = f"""# {spec.name}

{spec.description}

## Installation

```bash
pip install {spec.name}
```

## Usage

Coming soon...
"""

    return DocOutput(
        docs_created={"README.md": readme},
        files_created=1
    )
```

---

## ✅ Your Solutions

### Solution #1: Real Test Generation & Execution

Implement a test generator that:
1. Generates pytest test files from ProjectSpec
2. Creates test fixtures and helper functions
3. Runs tests using pytest subprocess
4. Collects coverage data
5. Returns real TestOutput with actual results

### Solution #2: Comprehensive Documentation

Implement a documentation generator that:
1. Creates detailed README with installation, usage, examples
2. Generates API documentation from code
3. Creates CONTRIBUTING.md, LICENSE
4. Generates usage examples
5. Creates docs/ directory with additional guides

---

## 📝 Implementation Steps - Part 1: TesterAgent

### Step 1: Create Test Templates (45 minutes)

**Create:** `src/code_factory/templates/tests/` directory

**Files:**
```
src/code_factory/templates/tests/
├── test_main.py.template
├── test_core.py.template
├── conftest.py.template
└── pytest.ini.template
```

**Example: test_main.py.template**
```python
"""
Tests for {{ project_name }} main module
"""
import pytest
from {{ module_name }}.main import main

def test_main_runs_without_errors():
    """Test that main() executes without crashing"""
    try:
        result = main([])
        assert result == 0 or result is None
    except SystemExit as e:
        # Some CLIs call sys.exit()
        assert e.code == 0

def test_main_help():
    """Test that --help works"""
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0

def test_main_version():
    """Test that --version works"""
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0

# TODO: Add more specific tests based on project features
```

**Example: conftest.py.template**
```python
"""
Pytest configuration and fixtures for {{ project_name }}
"""
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {
        "test_key": "test_value"
    }

# Add project-specific fixtures here
```

**Example: pytest.ini.template**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov={{ module_name }}
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=70
```

---

### Step 2: Implement Test Generator (60 minutes)

**File:** `src/code_factory/agents/tester.py`

**Update the class:**

```python
import subprocess
from pathlib import Path
from typing import Dict, Any, List
import logging

from code_factory.core.models import ProjectSpec, TestOutput
from code_factory.agents.base import BaseAgent
from code_factory.templates import TemplateRenderer

logger = logging.getLogger(__name__)

class TesterAgent(BaseAgent):
    """Agent that generates and runs tests for generated projects"""

    def __init__(self):
        super().__init__()
        templates_dir = Path(__file__).parent.parent / "templates" / "tests"
        self.renderer = TemplateRenderer(templates_dir)

    @property
    def name(self) -> str:
        return "tester"

    @property
    def description(self) -> str:
        return "Generates pytest tests and runs test suite for generated projects"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """Generate tests and optionally run them"""
        # Input can be ProjectSpec or dict with spec + project_dir
        if isinstance(input_data, dict):
            spec = input_data.get("spec")
            project_dir = input_data.get("project_dir")
            run_tests = input_data.get("run_tests", False)
        else:
            spec = self.validate_input(input_data, ProjectSpec)
            project_dir = None
            run_tests = False

        logger.info(f"Generating tests for: {spec.name}")

        try:
            # Generate test files
            test_files = self._generate_test_files(spec)

            # Optionally run tests if project_dir provided
            if run_tests and project_dir:
                test_results = self._run_tests(Path(project_dir))
            else:
                test_results = None

            return TestOutput(
                tests_run=test_results["total"] if test_results else 0,
                tests_passed=test_results["passed"] if test_results else 0,
                tests_failed=test_results["failed"] if test_results else 0,
                coverage_percent=test_results["coverage"] if test_results else 0.0,
                test_files=test_files,
                error=""
            )

        except Exception as e:
            logger.error(f"Test generation failed: {e}")
            return TestOutput(
                tests_run=0,
                tests_passed=0,
                tests_failed=0,
                coverage_percent=0.0,
                test_files={},
                error=str(e)
            )

    def _generate_test_files(self, spec: ProjectSpec) -> Dict[str, str]:
        """Generate pytest test files from spec"""
        module_name = spec.name.replace("-", "_")

        context = {
            "project_name": spec.name,
            "module_name": module_name,
            "description": spec.description,
            "features": spec.features if hasattr(spec, 'features') else []
        }

        test_files = {}

        # Generate main test file
        test_files["tests/test_main.py"] = self.renderer.render(
            "test_main.py.template",
            context
        )

        # Generate conftest
        test_files["tests/conftest.py"] = self.renderer.render(
            "conftest.py.template",
            context
        )

        # Generate pytest.ini
        test_files["pytest.ini"] = self.renderer.render(
            "pytest.ini.template",
            context
        )

        # Generate feature-specific tests
        if hasattr(spec, 'features') and spec.features:
            for idx, feature in enumerate(spec.features):
                test_name = f"test_feature_{idx + 1}.py"
                test_files[f"tests/{test_name}"] = self._generate_feature_test(
                    feature,
                    module_name
                )

        # Create __init__.py for tests package
        test_files["tests/__init__.py"] = '"""Test suite for {}"""\n'.format(spec.name)

        return test_files

    def _generate_feature_test(self, feature: str, module_name: str) -> str:
        """Generate a test for a specific feature"""
        safe_name = feature.lower().replace(" ", "_").replace("-", "_")

        return f'''"""
Test for feature: {feature}
"""
import pytest

def test_{safe_name}():
    """Test: {feature}"""
    # TODO: Implement test for {feature}
    assert True  # Placeholder

# Add more specific tests for {feature}
'''

    def _run_tests(self, project_dir: Path) -> Dict[str, Any]:
        """Run pytest in project directory and collect results"""
        logger.info(f"Running tests in {project_dir}")

        try:
            # Run pytest with coverage
            result = subprocess.run(
                ["pytest", "--cov", "--cov-report=term", "-v"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )

            # Parse output (simple parsing, can be improved)
            output = result.stdout + result.stderr

            # Extract test counts (this is basic, pytest-json-report would be better)
            import re

            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)
            coverage_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)

            passed = int(passed_match.group(1)) if passed_match else 0
            failed = int(failed_match.group(1)) if failed_match else 0
            total = passed + failed

            coverage = float(coverage_match.group(1)) if coverage_match else 0.0

            return {
                "total": total,
                "passed": passed,
                "failed": failed,
                "coverage": coverage,
                "output": output
            }

        except subprocess.TimeoutExpired:
            logger.error("Tests timed out after 120 seconds")
            return {"total": 0, "passed": 0, "failed": 0, "coverage": 0.0}

        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return {"total": 0, "passed": 0, "failed": 0, "coverage": 0.0}

    def write_test_files(self, test_files: Dict[str, str], project_dir: Path) -> None:
        """Write test files to disk"""
        for file_path, content in test_files.items():
            full_path = project_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            logger.info(f"Created test file: {file_path}")
```

---

### Step 3: Update TestOutput Model (10 minutes)

**File:** `src/code_factory/core/models.py`

```python
class TestOutput(BaseModel):
    """Output from TesterAgent"""
    tests_run: int
    tests_passed: int
    tests_failed: int = 0
    coverage_percent: float
    test_files: Dict[str, str] = {}
    error: str = ""
```

---

## 📝 Implementation Steps - Part 2: DocWriterAgent

### Step 4: Create Documentation Templates (45 minutes)

**Create:** `src/code_factory/templates/docs/` directory

**Files:**
```
src/code_factory/templates/docs/
├── README.md.template
├── CONTRIBUTING.md.template
├── LICENSE.template
├── installation.md.template
└── usage.md.template
```

**Example: README.md.template**
```markdown
# {{ project_name }}

{{ description }}

## ✨ Features

{% for feature in features %}
- {{ feature }}
{% endfor %}

## 📦 Installation

```bash
# Using pip
pip install {{ project_name }}

# From source
git clone {{ repo_url }}
cd {{ project_name }}
pip install -e .
```

## 🚀 Quick Start

```bash
{{ project_name }} --help
```

## 📖 Usage

```python
from {{ module_name }} import main

# Example usage
result = main()
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov={{ module_name }}
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [API Reference](docs/api.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

{{ license }}

## 🙏 Acknowledgments

Generated with [Agent-Orchestrated Code Factory](https://github.com/Dparent97/AgentOrchestratedCodeFactory)
```

**Example: CONTRIBUTING.md.template**
```markdown
# Contributing to {{ project_name }}

Thank you for considering contributing to {{ project_name }}!

## Development Setup

```bash
# Clone the repository
git clone {{ repo_url }}
cd {{ project_name }}

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small

## Testing

- Write tests for new features
- Maintain >80% code coverage
- All tests must pass before PR

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit pull request

## Questions?

Open an issue or reach out to the maintainers.
```

---

### Step 5: Implement DocWriterAgent (60 minutes)

**File:** `src/code_factory/agents/doc_writer.py`

**Update the class:**

```python
from pathlib import Path
from typing import Dict
from datetime import datetime

from code_factory.core.models import ProjectSpec, DocOutput
from code_factory.agents.base import BaseAgent
from code_factory.templates import TemplateRenderer

class DocWriterAgent(BaseAgent):
    """Agent that generates comprehensive documentation"""

    def __init__(self):
        super().__init__()
        templates_dir = Path(__file__).parent.parent / "templates" / "docs"
        self.renderer = TemplateRenderer(templates_dir)

    @property
    def name(self) -> str:
        return "doc_writer"

    @property
    def description(self) -> str:
        return "Generates comprehensive project documentation"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """Generate comprehensive documentation from ProjectSpec"""
        if isinstance(input_data, dict):
            spec = input_data.get("spec")
        else:
            spec = self.validate_input(input_data, ProjectSpec)

        logger.info(f"Writing documentation for: {spec.name}")

        try:
            docs = self._generate_documentation(spec)

            return DocOutput(
                docs_created=docs,
                files_created=len(docs)
            )

        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            return DocOutput(
                docs_created={},
                files_created=0,
                error=str(e)
            )

    def _generate_documentation(self, spec: ProjectSpec) -> Dict[str, str]:
        """Generate all documentation files"""
        module_name = spec.name.replace("-", "_")

        context = {
            "project_name": spec.name,
            "description": spec.description,
            "module_name": module_name,
            "features": spec.features if hasattr(spec, 'features') else [],
            "dependencies": spec.dependencies,
            "entry_point": spec.entry_point,
            "repo_url": f"https://github.com/YOUR_ORG/{spec.name}",
            "license": "MIT",
            "year": datetime.now().year,
        }

        docs = {}

        # Main README
        docs["README.md"] = self.renderer.render("README.md.template", context)

        # Contributing guide
        docs["CONTRIBUTING.md"] = self.renderer.render("CONTRIBUTING.md.template", context)

        # License
        docs["LICENSE"] = self._generate_license(context)

        # Detailed installation guide
        docs["docs/installation.md"] = self._generate_installation_guide(spec, context)

        # Usage guide
        docs["docs/usage.md"] = self._generate_usage_guide(spec, context)

        # API reference
        docs["docs/api.md"] = self._generate_api_reference(spec, context)

        return docs

    def _generate_license(self, context: Dict) -> str:
        """Generate MIT license"""
        return f"""MIT License

Copyright (c) {context['year']} {context['project_name']}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    def _generate_installation_guide(self, spec: ProjectSpec, context: Dict) -> str:
        """Generate installation guide"""
        return f"""# Installation Guide for {spec.name}

## Requirements

- Python 3.11 or higher

## Installation Methods

### Method 1: pip (recommended)

```bash
pip install {spec.name}
```

### Method 2: From source

```bash
git clone {context['repo_url']}
cd {spec.name}
pip install -e .
```

## Verifying Installation

```bash
{spec.name} --version
```

## Dependencies

The following packages will be automatically installed:

{chr(10).join(f"- {dep}" for dep in spec.dependencies)}

## Troubleshooting

### Issue: Command not found

Make sure `~/.local/bin` is in your PATH.

### Issue: Permission denied

Use `pip install --user {spec.name}`
"""

    def _generate_usage_guide(self, spec: ProjectSpec, context: Dict) -> str:
        """Generate usage guide"""
        return f"""# Usage Guide for {spec.name}

## Basic Usage

```bash
{spec.name} --help
```

## Features

{chr(10).join(f"### {feature}{chr(10)}TODO: Document {feature}{chr(10)}" for feature in context['features'])}

## Examples

### Example 1: Basic usage

```bash
{spec.name} input.txt
```

### Example 2: With options

```bash
{spec.name} --option value input.txt
```

## Advanced Usage

TODO: Add advanced usage examples

## Configuration

Configuration file: `~/.{module_name}/config.ini`

```ini
[settings]
option1 = value1
option2 = value2
```
"""

    def _generate_api_reference(self, spec: ProjectSpec, context: Dict) -> str:
        """Generate API reference"""
        return f"""# API Reference for {spec.name}

## Main Module

### `{context['module_name']}.main`

Main entry point for {spec.name}.

```python
from {context['module_name']}.main import main

result = main(args)
```

#### Functions

TODO: Document public functions

## Core Module

### `{context['module_name']}.core`

Core functionality.

TODO: Document core classes and functions

## Utilities

### `{context['module_name']}.utils`

Utility functions.

TODO: Document utility functions
"""

    def write_docs(self, docs: Dict[str, str], project_dir: Path) -> None:
        """Write documentation files to disk"""
        for file_path, content in docs.items():
            full_path = project_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            logger.info(f"Created documentation: {file_path}")
```

---

## 📋 Files to Create/Modify

| File | Action | Priority |
|------|--------|----------|
| `src/code_factory/templates/tests/*.template` | CREATE | HIGH |
| `src/code_factory/templates/docs/*.template` | CREATE | HIGH |
| `src/code_factory/agents/tester.py` | MODIFY | CRITICAL |
| `src/code_factory/agents/doc_writer.py` | MODIFY | CRITICAL |
| `src/code_factory/core/models.py` (TestOutput, DocOutput) | MODIFY | HIGH |
| `tests/unit/test_tester.py` | CREATE | HIGH |
| `tests/unit/test_doc_writer.py` | CREATE | HIGH |

---

## ✅ Success Criteria

### TesterAgent:
- [ ] Generates real pytest test files (not mocks)
- [ ] Creates conftest.py with fixtures
- [ ] Generates pytest.ini configuration
- [ ] Can run tests and collect real results
- [ ] Returns TestOutput with actual coverage data
- [ ] Test files are syntactically valid Python
- [ ] Unit tests achieve 80%+ coverage

### DocWriterAgent:
- [ ] Generates comprehensive README.md
- [ ] Creates CONTRIBUTING.md
- [ ] Generates LICENSE file
- [ ] Creates docs/ directory with guides
- [ ] Documentation is well-formatted Markdown
- [ ] All generated docs are >100 words (not stubs)
- [ ] Unit tests achieve 80%+ coverage

### Both:
- [ ] All tests pass: `pytest tests/unit/test_tester.py tests/unit/test_doc_writer.py -v`
- [ ] Code follows style guide
- [ ] Integration tests work end-to-end

---

## 🧪 Testing Checklist

```bash
# Test TesterAgent
pytest tests/unit/test_tester.py -v

# Test DocWriterAgent
pytest tests/unit/test_doc_writer.py -v

# Test integration
pytest tests/integration/ -v

# Check coverage
pytest --cov=src/code_factory/agents/tester --cov=src/code_factory/agents/doc_writer

# Manual test: Generate project and check docs
code-factory create "Build CSV parser"
cd output/csv-parser
cat README.md  # Should be comprehensive
pytest  # Should run and pass
```

---

## 🚨 Integration Points

### You Depend On:
- **Agent 1 (Pipeline)** - Need working orchestrator
- **Agent 2 (Code Generation)** - Need real code to test and document
- **ProjectSpec model** - Already exists

### Other Agents Depend On You:
- **None** - You work on generated projects

---

## 📝 Git Workflow

```bash
git checkout -b claude/implement-testing-docs

git commit -m "feat: implement test generation in TesterAgent"
git commit -m "feat: add test execution and coverage collection"
git commit -m "feat: implement comprehensive documentation in DocWriterAgent"
git commit -m "test: add unit tests for TesterAgent and DocWriterAgent"

git push -u origin claude/implement-testing-docs
```

**PR Title:** `feat: Implement TesterAgent and DocWriterAgent`

**PR Description:**
```markdown
Completes implementation of TesterAgent and DocWriterAgent.

## TesterAgent Changes:
- Implemented pytest test file generation
- Created test templates (test_main, conftest, pytest.ini)
- Added test execution with coverage collection
- Returns real test results (not mocks)

## DocWriterAgent Changes:
- Implemented comprehensive README generation
- Created CONTRIBUTING.md, LICENSE templates
- Added installation, usage, API reference guides
- Generated docs/ directory structure

## Features:
- Real pytest tests with proper structure
- Test fixtures and configuration
- Comprehensive markdown documentation
- License generation (MIT)
- Professional README with features, usage, examples

## Testing:
- 20+ unit tests across both agents
- Integration tests verify end-to-end workflow
- Manual test: Generated project has full test suite and docs

Closes #XX
```

---

## 💡 Design Decisions

### Why pytest over unittest?
**Decision:** Generate pytest-style tests
**Rationale:**
- Modern, Pythonic syntax
- Better fixtures
- More popular in community
- Already used in Code Factory

### Test Execution: Always run or optional?
**Decision:** Make test execution optional
**Rationale:**
- Requires project to be installed
- May fail if dependencies missing
- Generation is primary goal, execution is bonus

### Documentation Scope?
**Decision:** Generate README, CONTRIBUTING, LICENSE, docs/
**Rationale:**
- Professional projects need all these
- Blue-collar users benefit from clear docs
- Sets up good practices

---

## 📚 Reference Documentation

- **pytest Documentation:** https://docs.pytest.org/
- **Markdown Guide:** https://www.markdownguide.org/
- **Python Packaging:** https://packaging.python.org/
- **Current Agents:** `src/code_factory/agents/tester.py`, `doc_writer.py`

---

## 🎯 Ready to Start?

1. **Create** test templates first
2. **Implement** TesterAgent
3. **Test** test generation
4. **Create** documentation templates
5. **Implement** DocWriterAgent
6. **Test** both agents
7. **Create PR**

---

**START NOW**
