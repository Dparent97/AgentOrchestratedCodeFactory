# Agent 2: Code Generation Engineer

**Repository:** https://github.com/Dparent97/AgentOrchestratedCodeFactory
**Branch:** `claude/implement-code-generation`
**Iteration:** Phase 3 - ImplementerAgent Implementation
**Time Estimate:** 3-4 hours

---

## 🎯 Your Mission

Transform the ImplementerAgent from a placeholder (returns mock code) into a real code generator that creates functional Python projects from ProjectSpec. You'll implement template-based code generation, file structure creation, and integration with the transaction system for safe file operations.

---

## 🔴 Current Problem

**File:** `src/code_factory/agents/implementer.py`
**Lines:** 48-56
**Status:** Placeholder implementation

**Current Code:**
```python
def execute(self, input_data: BaseModel) -> BaseModel:
    spec = self.validate_input(input_data, ProjectSpec)
    logger.info(f"Generating code for: {spec.name}")

    # TODO: Implement actual code generation
    files = {
        "src/main.py": "# Placeholder implementation\nprint('Hello')\n",
        "README.md": f"# {spec.name}\n\nPlaceholder project\n",
    }

    return CodeOutput(files=files, files_created=len(files))
```

**Problem:** Returns hardcoded placeholder strings, not real project code.

---

## ✅ Your Solution

Implement a **template-based code generation system** that:
1. Takes `ProjectSpec` as input
2. Generates project folder structure from `spec.folder_structure`
3. Creates Python files with proper imports, classes, functions
4. Generates configuration files (pyproject.toml, .gitignore, etc.)
5. Uses the transaction system for safe file operations
6. Returns real, runnable code

---

## 🏗️ Implementation Architecture

### Design Pattern: Template-Based Generation

```python
# High-level flow:
ProjectSpec
  → Template Selector (choose templates based on spec.tech_stack)
  → Template Renderer (jinja2 or string.Template)
  → File Generator (create actual files)
  → Transaction Manager (safe write with rollback)
  → CodeOutput (return results)
```

---

## 📝 Implementation Steps

### Step 1: Create Template System (60 minutes)

**Create:** `src/code_factory/templates/` directory

**Files to create:**
```
src/code_factory/templates/
├── __init__.py
├── python_cli/
│   ├── main.py.template
│   ├── pyproject.toml.template
│   ├── README.md.template
│   ├── gitignore.template
│   └── config.py.template
├── python_library/
│   ├── __init__.py.template
│   ├── core.py.template
│   └── pyproject.toml.template
└── base/
    ├── README.md.template
    └── gitignore.template
```

**Example Template (main.py.template):**
```python
#!/usr/bin/env python3
"""
{{ project_name }}

{{ description }}
"""
import argparse
import sys
from typing import Optional

def main(args: Optional[list] = None) -> int:
    """Main entry point for {{ project_name }}"""
    parser = argparse.ArgumentParser(description="{{ description }}")
    parser.add_argument("--version", action="version", version="0.1.0")

    # TODO: Add your CLI arguments here

    parsed_args = parser.parse_args(args)

    print("{{ project_name }} is running!")
    print("{{ description }}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Example Template (pyproject.toml.template):**
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
{% for dep in dependencies %}
    "{{ dep }}",
{% endfor %}
]

[project.scripts]
{{ project_name }} = "{{ module_name }}.main:main"
```

---

### Step 2: Create Template Renderer (45 minutes)

**File:** `src/code_factory/templates/__init__.py`

```python
"""Template rendering system for code generation"""
from pathlib import Path
from typing import Dict, Any
from string import Template

class TemplateRenderer:
    """Renders code templates with project data"""

    def __init__(self, template_dir: Path):
        self.template_dir = template_dir

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with given context"""
        template_path = self.template_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        with open(template_path, 'r') as f:
            template_content = f.read()

        # Use simple Template (or jinja2 for advanced features)
        template = Template(template_content)

        try:
            return template.safe_substitute(**context)
        except Exception as e:
            raise ValueError(f"Template rendering failed: {e}")

    def render_project(self, spec: 'ProjectSpec') -> Dict[str, str]:
        """Render all templates for a project spec"""
        files = {}

        context = self._build_context(spec)
        template_type = self._select_template_type(spec)

        # Render each template
        for template_name in self._get_templates(template_type):
            file_path = self._template_to_filepath(template_name, spec)
            files[file_path] = self.render(template_name, context)

        return files

    def _build_context(self, spec: 'ProjectSpec') -> Dict[str, Any]:
        """Build template context from ProjectSpec"""
        return {
            "project_name": spec.name,
            "description": spec.description,
            "module_name": spec.name.replace("-", "_"),
            "dependencies": spec.dependencies,
            "entry_point": spec.entry_point,
            "tech_stack": spec.tech_stack,
        }

    def _select_template_type(self, spec: 'ProjectSpec') -> str:
        """Select template type based on project spec"""
        # Decision logic based on spec.tech_stack
        if spec.tech_stack.get("type") == "cli":
            return "python_cli"
        elif spec.tech_stack.get("type") == "library":
            return "python_library"
        else:
            return "python_cli"  # Default

    def _get_templates(self, template_type: str) -> list:
        """Get list of templates for a type"""
        # Return list of template files
        return [
            f"{template_type}/main.py.template",
            f"{template_type}/pyproject.toml.template",
            "base/README.md.template",
            "base/gitignore.template",
        ]

    def _template_to_filepath(self, template_name: str, spec: 'ProjectSpec') -> str:
        """Convert template name to output file path"""
        # Remove template type prefix and .template suffix
        filename = template_name.split('/')[-1].replace('.template', '')

        # Map to project structure
        if filename == 'main.py':
            module = spec.name.replace("-", "_")
            return f"src/{module}/main.py"
        elif filename == 'gitignore':
            return ".gitignore"
        else:
            return filename
```

---

### Step 3: Update ImplementerAgent (60 minutes)

**File:** `src/code_factory/agents/implementer.py`

**Replace the execute() method:**

```python
from pathlib import Path
from code_factory.templates import TemplateRenderer
from code_factory.core.transaction import TransactionManager

class ImplementerAgent(BaseAgent):
    """Agent that generates actual code from specifications"""

    def __init__(self):
        super().__init__()
        # Find templates directory
        templates_dir = Path(__file__).parent.parent / "templates"
        self.renderer = TemplateRenderer(templates_dir)

    def execute(self, input_data: BaseModel) -> BaseModel:
        """Generate code from ProjectSpec using templates"""
        spec = self.validate_input(input_data, ProjectSpec)
        logger.info(f"Generating code for: {spec.name}")

        try:
            # Render all project files from templates
            files = self.renderer.render_project(spec)

            # Add folder structure
            files.update(self._create_folder_markers(spec))

            # Add additional files
            files.update(self._create_config_files(spec))

            logger.info(f"Generated {len(files)} files for {spec.name}")

            return CodeOutput(
                files=files,
                files_created=len(files),
                warnings=[]
            )

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return CodeOutput(
                files={},
                files_created=0,
                warnings=[f"Generation failed: {str(e)}"]
            )

    def _create_folder_markers(self, spec: ProjectSpec) -> Dict[str, str]:
        """Create __init__.py files for Python packages"""
        markers = {}
        module_name = spec.name.replace("-", "_")

        # Create package markers based on folder_structure
        for folder in spec.folder_structure.get("src", []):
            markers[f"src/{module_name}/{folder}/__init__.py"] = '"""Package marker"""\n'

        return markers

    def _create_config_files(self, spec: ProjectSpec) -> Dict[str, str]:
        """Create additional configuration files"""
        configs = {}

        # Create pytest.ini if tests are needed
        configs["pytest.ini"] = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""

        # Create .gitignore
        configs[".gitignore"] = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project specific
*.log
.env
"""

        return configs

    def write_files(self, output_dir: Path, code_output: CodeOutput) -> None:
        """Write generated files to disk using transaction system"""
        from code_factory.core.transaction import TransactionManager

        tm = TransactionManager(output_dir)

        try:
            for file_path, content in code_output.files.items():
                full_path = output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                tm.write_file(full_path, content)

            tm.commit()
            logger.info(f"Successfully wrote {len(code_output.files)} files")

        except Exception as e:
            tm.rollback()
            logger.error(f"File write failed, rolled back: {e}")
            raise
```

---

### Step 4: Create Unit Tests (45 minutes)

**File:** `tests/unit/test_implementer.py`

```python
import pytest
from code_factory.agents.implementer import ImplementerAgent
from code_factory.core.models import ProjectSpec

def test_implementer_generates_files():
    """Test that implementer generates actual code files"""
    agent = ImplementerAgent()

    spec = ProjectSpec(
        name="test-cli",
        description="A test CLI tool",
        tech_stack={"type": "cli", "language": "python"},
        folder_structure={"src": ["core", "utils"]},
        dependencies=["click>=8.0.0"],
        entry_point="test_cli.main:main"
    )

    result = agent.execute(spec)

    assert len(result.files) > 0
    assert "src/test_cli/main.py" in result.files
    assert "pyproject.toml" in result.files
    assert "README.md" in result.files
    assert ".gitignore" in result.files

def test_implementer_generated_code_is_valid_python():
    """Test that generated Python code is syntactically valid"""
    agent = ImplementerAgent()

    spec = ProjectSpec(
        name="parser",
        description="CSV parser",
        tech_stack={"type": "library", "language": "python"},
        folder_structure={"src": ["core"]},
        dependencies=["pandas"],
        entry_point="parser.core:parse"
    )

    result = agent.execute(spec)

    # Check main.py is valid Python
    main_py = result.files.get("src/parser/main.py", "")
    assert "def main" in main_py or "class" in main_py

    # Attempt to compile (syntax check)
    import ast
    for file_path, content in result.files.items():
        if file_path.endswith(".py"):
            try:
                ast.parse(content)
            except SyntaxError as e:
                pytest.fail(f"Generated invalid Python in {file_path}: {e}")

def test_implementer_includes_dependencies():
    """Test that pyproject.toml includes specified dependencies"""
    agent = ImplementerAgent()

    spec = ProjectSpec(
        name="tool",
        description="Test tool",
        tech_stack={"type": "cli"},
        folder_structure={},
        dependencies=["requests", "click", "pydantic"],
        entry_point="tool.main:main"
    )

    result = agent.execute(spec)
    pyproject = result.files.get("pyproject.toml", "")

    assert "requests" in pyproject
    assert "click" in pyproject
    assert "pydantic" in pyproject

def test_implementer_handles_errors_gracefully():
    """Test that implementer handles invalid specs gracefully"""
    agent = ImplementerAgent()

    # Invalid spec (missing required fields)
    invalid_spec = {}

    # Should not crash, should return empty CodeOutput or error
    # Test depends on your error handling strategy
```

---

## 📋 Files to Create/Modify

| File | Action | Priority |
|------|--------|----------|
| `src/code_factory/templates/__init__.py` | CREATE | HIGH |
| `src/code_factory/templates/python_cli/main.py.template` | CREATE | HIGH |
| `src/code_factory/templates/python_cli/pyproject.toml.template` | CREATE | HIGH |
| `src/code_factory/templates/base/README.md.template` | CREATE | MEDIUM |
| `src/code_factory/templates/base/gitignore.template` | CREATE | MEDIUM |
| `src/code_factory/agents/implementer.py` | MODIFY | CRITICAL |
| `tests/unit/test_implementer.py` | MODIFY | HIGH |

---

## ✅ Success Criteria

- [ ] Template system implemented with TemplateRenderer class
- [ ] At least 2 template types (python_cli, python_library)
- [ ] ImplementerAgent generates real code (not placeholders)
- [ ] Generated Python code is syntactically valid (can be parsed by ast)
- [ ] Generated projects include pyproject.toml with dependencies
- [ ] Generated projects include README.md with project description
- [ ] Generated projects include .gitignore
- [ ] ImplementerAgent uses transaction system for file writes
- [ ] Unit tests achieve 80%+ coverage
- [ ] All tests pass: `pytest tests/unit/test_implementer.py -v`
- [ ] Integration test works: Generated code can be installed and run
- [ ] Code follows style guide: `ruff` and `black`

---

## 🧪 Testing Strategy

### Unit Tests (test_implementer.py):
- Test template rendering
- Test file generation
- Test dependency injection
- Test error handling

### Integration Tests (test_wave1_pipeline.py):
- Test full pipeline: Idea → Plan → Arch → **Code**
- Verify generated code is valid
- Verify folder structure matches spec

### Manual Tests:
```bash
# Generate a project
code-factory create "Build a CSV parser"

# Try to install and run it
cd output/csv-parser
pip install -e .
csv-parser --help  # Should work!
```

---

## 🚨 Integration Points

### You Depend On:
- **Agent 1 (Pipeline Integration)** - Need working orchestrator to test
- **ProjectSpec model** (already exists in `core/models.py`)

### Other Agents Depend On You:
- **Agent 4 (Testing & Docs)** - Needs real code to test and document
- **Agent 3 (Git Operations)** - Needs real files to commit

---

## 📝 Git Workflow

```bash
# Create branch
git checkout -b claude/implement-code-generation

# Commit incrementally
git commit -m "feat: add template rendering system"
git commit -m "feat: create Python CLI templates"
git commit -m "feat: update ImplementerAgent with real code generation"
git commit -m "test: add comprehensive ImplementerAgent tests"

# Push and create PR
git push -u origin claude/implement-code-generation
```

**PR Title:** `feat: Implement real code generation in ImplementerAgent`

**PR Description:**
```markdown
Transforms ImplementerAgent from placeholder to real code generator.

## Changes:
- Created template-based code generation system
- Implemented TemplateRenderer class
- Created Python CLI and library templates
- Updated ImplementerAgent to generate real, runnable code
- Added comprehensive unit tests
- Integrated with transaction system for safe file writes

## Testing:
- 15+ unit tests covering generation, templates, errors
- Integration test verifies generated code is valid
- Manual test: Generated CLI tool works end-to-end

Closes #XX (if applicable)
```

---

## 💡 Design Decisions

### Why Template-Based vs. AST-Based?
**Decision:** Use simple templates (string.Template)
**Rationale:**
- Faster to implement (3-4 hours vs. days)
- Easier to maintain and extend
- Sufficient for Phase 3 goals
- Can upgrade to jinja2 or AST later if needed

### What Templates to Create?
**Decision:** python_cli and python_library
**Rationale:**
- Covers 80% of blue-collar use cases
- CLI tools are primary target (marine logs, HVAC calc, etc.)
- Libraries support code reuse

### Error Handling Strategy?
**Decision:** Return CodeOutput with warnings, don't crash
**Rationale:**
- Allows pipeline to continue
- Provides feedback to user
- Consistent with other agents

---

## 📚 Reference Documentation

- **Template Design Patterns:** https://docs.python.org/3/library/string.html#template-strings
- **Project Spec Model:** `src/code_factory/core/models.py:ProjectSpec`
- **Transaction System:** `src/code_factory/core/transaction.py`
- **Existing Implementer:** `src/code_factory/agents/implementer.py`

---

## ❓ Questions?

Post to `AGENT_PROMPTS/questions.md`:

```markdown
## Code Generation Engineer - 2025-11-18 - Q1

**Question:** Should templates support jinja2 features (loops, conditionals)?

**Context:** string.Template is simpler, jinja2 is more powerful

**Blocking:** No, but affects template complexity

**Target:** @Coordinator
```

---

## 🎯 Ready to Start?

1. **Wait** for Agent 1 (Pipeline Integration) to merge first (optional but helpful)
2. **Create** templates directory and files
3. **Implement** TemplateRenderer
4. **Update** ImplementerAgent
5. **Write** tests
6. **Test** end-to-end
7. **Create PR**

---

**START NOW**
