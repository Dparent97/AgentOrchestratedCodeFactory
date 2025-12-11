# Code Generation System

The Agent-Orchestrated Code Factory uses a template-based code generation system to create complete, working Python projects from specifications.

## Overview

The code generation system consists of three main components:

1. **TemplateEngine** - Renders Jinja2 templates with project context
2. **ImplementerAgent** - Coordinates code generation using the template engine
3. **CodeWriter** - Safely writes generated files to disk with transaction support

## Architecture

```
ProjectSpec → TemplateEngine → Generated Files → CodeWriter → Disk
                    ↓
              Jinja2 Templates
```

## Template Engine

The `TemplateEngine` (`src/code_factory/core/template_engine.py`) provides template-based code generation:

### Features

- **Jinja2-based templating** for flexible code generation
- **Multiple project types**: CLI applications, libraries, data processing tools
- **Domain-specific templates** for common use cases
- **Fallback templates** when custom templates are unavailable
- **Context building** from ProjectSpec

### Template Structure

Templates are organized by type:

```
src/code_factory/templates/
├── common/              # Shared templates
│   ├── README.md.j2
│   ├── pyproject.toml.j2
│   ├── gitignore.j2
│   └── test_main.py.j2
├── cli/                 # CLI-specific templates
│   ├── main.py.j2
│   └── cli.py.j2
└── library/             # Library templates
    ├── core.py.j2
    ├── __init__.py.j2
    └── data_processor.py.j2
```

### Template Context

Templates receive the following context variables:

- `project_name` - Project name (kebab-case)
- `package_name` - Python package name (snake_case)
- `script_name` - CLI script name
- `class_name` - Main class name (PascalCase)
- `description` - Project description
- `tech_stack` - Technology choices
- `dependencies` - Package dependencies
- `entry_point` - Main entry point file
- `features` - List of features
- `environment` - Target environment
- `user_profile` - Target user profile

### Usage Example

```python
from code_factory.core.template_engine import TemplateEngine
from code_factory.core.models import ProjectSpec

# Create specification
spec = ProjectSpec(
    name="my-cli-tool",
    description="A command-line tool",
    tech_stack={"language": "python", "cli_framework": "typer"},
    dependencies=["typer", "rich"],
    entry_point="src/main.py",
    folder_structure={}
)

# Generate files
engine = TemplateEngine()
files = engine.generate_project_files(spec)

# files is a dict mapping file paths to content
for file_path, content in files.items():
    print(f"{file_path}: {len(content)} bytes")
```

## ImplementerAgent

The `ImplementerAgent` (`src/code_factory/agents/implementer.py`) is the main code generation agent:

### Responsibilities

- Accept ProjectSpec as input
- Generate complete project structure using TemplateEngine
- Validate generated files
- Return CodeOutput with all files

### Features

- **Template-based generation** - Uses templates for consistency
- **Multiple project types** - CLI, library, data processing
- **File validation** - Ensures required files are present
- **Error handling** - Graceful failures with detailed logging

### Usage Example

```python
from code_factory.agents.implementer import ImplementerAgent
from code_factory.core.models import ProjectSpec

# Create agent
agent = ImplementerAgent()

# Generate code
spec = ProjectSpec(...)
result = agent.execute(spec)

# result.files contains all generated files
print(f"Generated {result.files_created} files")
```

### Generated Files

For a typical CLI project, the agent generates:

```
project-name/
├── README.md           # Project documentation
├── pyproject.toml      # Project configuration
├── .gitignore          # Git ignore rules
├── src/
│   └── project_name/
│       ├── __init__.py # Package init
│       ├── main.py     # CLI entry point
│       ├── cli.py      # CLI utilities
│       └── core.py     # Core functionality
└── tests/
    ├── __init__.py     # Test package init
    └── test_main.py    # Main tests
```

## CodeWriter

The `CodeWriter` (`src/code_factory/core/code_writer.py`) safely writes files to disk:

### Features

- **Transaction support** - All-or-nothing file writing
- **Automatic rollback** - On errors, no partial writes
- **Directory creation** - Automatically creates nested directories
- **Staging support** - Optional staging before commit

### Usage Example

```python
from pathlib import Path
from code_factory.core.code_writer import CodeWriter

# Create writer
project_root = Path("/path/to/project")
writer = CodeWriter(project_root)

# Write files with transaction safety
files = {
    "README.md": "# My Project",
    "src/main.py": "def main(): pass"
}

writer.write_project_files(files, enable_staging=True)

# Validate structure
if writer.validate_project_structure():
    print("Project structure is valid")
```

## Template Creation

To create a new template:

1. **Create template file** in appropriate directory (`.j2` extension)
2. **Use Jinja2 syntax** for variable substitution
3. **Access context variables** like `{{ project_name }}`
4. **Add conditionals** for optional features

### Example Template

```jinja2
"""
{{ project_name }} - {{ description }}

Main module for the project.
"""

{% if "cli" in tech_stack.values() %}
import typer

app = typer.Typer()

@app.command()
def main():
    """Main command"""
    print("Hello from {{ project_name }}!")
{% else %}
class {{ class_name }}:
    """Main class for {{ project_name }}"""

    def __init__(self):
        """Initialize {{ class_name }}"""
        pass
{% endif %}
```

## Project Types

### CLI Projects

Detected when:
- `cli_framework` in tech_stack
- `typer` in dependencies
- `entry_point` is "src/main.py"

Generated files:
- `src/{package}/main.py` - CLI entry point with typer
- `src/{package}/cli.py` - CLI utilities
- Tests with CLI testing support

### Library Projects

Default for all projects. Generates:
- `src/{package}/core.py` - Main library class
- `src/{package}/__init__.py` - Package exports
- Tests with class testing

### Data Processing Projects

Detected when:
- `data_library` in tech_stack
- `pandas` or similar in dependencies

Additional files:
- `src/{package}/data_processor.py` - Data processing utilities

## Integration with Orchestrator

The code generation system integrates with the main orchestrator:

```python
# In orchestrator.py
from code_factory.agents.implementer import ImplementerAgent
from code_factory.core.code_writer import CodeWriter

# Generate code
implementer = ImplementerAgent()
code_output = implementer.execute(project_spec)

# Write to disk
writer = CodeWriter(project_path)
writer.write_project_files(code_output.files)
```

## Best Practices

1. **Use templates** for consistency across generated projects
2. **Validate specifications** before generation
3. **Enable staging** for safer file operations
4. **Test generated code** with unit tests
5. **Document templates** for maintainability
6. **Handle errors gracefully** with rollback

## Extension Points

### Adding New Templates

1. Create `.j2` file in templates directory
2. Add logic to `TemplateEngine._generate_*_files()` method
3. Update context building if needed
4. Add tests for new template

### Supporting New Project Types

1. Add detection logic to `_is_*_project()` method
2. Create template directory for project type
3. Add file generation method
4. Update documentation

### Custom Template Directory

```python
from pathlib import Path

# Use custom templates
custom_dir = Path("/path/to/templates")
engine = TemplateEngine(template_dir=custom_dir)
```

## Testing

Comprehensive tests ensure code generation quality:

- **Template tests** - Verify template rendering
- **Agent tests** - Test ImplementerAgent behavior
- **Writer tests** - Verify safe file writing
- **Integration tests** - End-to-end testing

Run tests:

```bash
pytest tests/unit/test_template_engine.py -v
pytest tests/unit/test_implementer_agent.py -v
pytest tests/unit/test_code_writer.py -v
```

## Performance

- Templates are loaded on-demand
- File generation is memory-efficient
- Transaction system minimizes I/O
- Staging reduces filesystem contention

## Troubleshooting

### Template Not Found

```
TemplateNotFound: common/README.md.j2
```

**Solution**: Ensure template file exists in templates directory, or rely on fallback templates.

### Invalid ProjectSpec

```
ValueError: Name must contain only alphanumeric characters
```

**Solution**: Ensure project name follows naming conventions (lowercase, hyphens, underscores).

### File Write Errors

```
RuntimeError: Failed to write project files
```

**Solution**: Check file permissions, disk space, and path validity.

## Future Enhancements

- LLM-powered code generation for complex logic
- Multi-language support (JavaScript, Go, Rust)
- Custom template repositories
- Template versioning and updates
- Generated code optimization
- IDE integration

---

For more information, see:
- [Architecture Overview](architecture.md)
- [Agent Roles](agent_roles.md)
- [Transaction System](../src/code_factory/core/transaction.py)
