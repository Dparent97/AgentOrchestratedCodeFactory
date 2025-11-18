"""
DocWriterAgent - Generates project documentation

Creates comprehensive documentation including README, contributing guidelines,
usage guides, API documentation, and other user-facing documentation.
"""

import ast
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, ProjectSpec
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DocInput(BaseModel):
    """Input for documentation generation"""
    spec: ProjectSpec
    idea: Optional[Idea] = Field(None, description="Original idea for context")
    code_files: Optional[Dict[str, str]] = Field(None, description="Code files for API docs")


class DocOutput(BaseModel):
    """Output containing generated documentation files"""
    files: Dict[str, str]  # file_path -> content


class DocWriterAgent(BaseAgent):
    """
    Generates comprehensive project documentation

    This agent creates professional documentation including:
    - README.md with project overview, installation, and usage
    - CONTRIBUTING.md with contribution guidelines
    - LICENSE file (MIT)
    - docs/usage.md with detailed usage guide
    - docs/api.md with API documentation (if code provided)
    - docs/architecture.md with design decisions

    The documentation is tailored for blue-collar users - clear,
    practical, and focused on real-world usage.
    """

    @property
    def name(self) -> str:
        return "doc_writer"

    @property
    def description(self) -> str:
        return "Generates comprehensive documentation and usage guides"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Generate documentation

        Args:
            input_data: DocInput with ProjectSpec and optional code

        Returns:
            DocOutput: Generated documentation files
        """
        # Accept both ProjectSpec and DocInput
        if isinstance(input_data, ProjectSpec):
            doc_input = DocInput(spec=input_data)
        else:
            doc_input = self.validate_input(input_data, DocInput)

        spec = doc_input.spec
        logger.info(f"Generating documentation for: {spec.name}")

        files = {}

        # Generate README.md
        files["README.md"] = self._generate_readme(spec, doc_input.idea)

        # Generate CONTRIBUTING.md
        files["CONTRIBUTING.md"] = self._generate_contributing(spec)

        # Generate LICENSE
        files["LICENSE"] = self._generate_license(spec)

        # Generate docs/usage.md
        files["docs/usage.md"] = self._generate_usage_guide(spec, doc_input.idea)

        # Generate docs/architecture.md
        files["docs/architecture.md"] = self._generate_architecture_doc(spec, doc_input.idea)

        # Generate API documentation if code files provided
        if doc_input.code_files:
            api_docs = self._generate_api_docs(spec, doc_input.code_files)
            if api_docs:
                files["docs/api.md"] = api_docs

        # Generate .gitignore
        files[".gitignore"] = self._generate_gitignore(spec)

        logger.info(f"Generated {len(files)} documentation files")
        return DocOutput(files=files)

    def _generate_readme(self, spec: ProjectSpec, idea: Optional[Idea] = None) -> str:
        """Generate comprehensive README.md"""

        # Extract tech stack info
        language = spec.tech_stack.get('language', 'Python').title()
        cli_framework = spec.tech_stack.get('cli', '')

        # Build features list
        features_section = ""
        if idea and idea.features:
            features_list = '\n'.join(f"- {feature}" for feature in idea.features)
            features_section = f"""## Features

{features_list}
"""

        # Build installation section based on language
        install_section = self._build_installation_section(spec, language)

        # Build usage section
        usage_section = self._build_usage_section(spec, cli_framework)

        # Build target users section if available
        target_users_section = ""
        if idea and idea.target_users:
            users_list = ', '.join(idea.target_users)
            target_users_section = f"""## Who Is This For?

This tool is designed for **{users_list}** who need a practical, reliable solution that works in real-world environments.
"""

        # Environment notes
        environment_section = ""
        if spec.environment or (idea and idea.environment):
            env = spec.environment or idea.environment
            environment_section = f"""## Environment

**Designed for:** {env}

This tool is built with field conditions in mind - works offline, handles errors gracefully, and provides clear feedback.
"""

        readme = f"""# {spec.name}

> {spec.description}

{target_users_section}
{environment_section}
{features_section}
{install_section}
{usage_section}
## Documentation

- [Usage Guide](docs/usage.md) - Detailed usage instructions
- [Architecture](docs/architecture.md) - Design decisions and structure
- [Contributing](CONTRIBUTING.md) - How to contribute
- [API Documentation](docs/api.md) - API reference (if available)

## Requirements

- {language} {self._get_version_requirement(language)}
- Dependencies listed in `{self._get_dependency_file(spec)}`

## Configuration

See `docs/usage.md` for configuration options.

## Troubleshooting

### Common Issues

**Issue:** Installation fails
- **Solution:** Ensure you have {language} installed and up to date

**Issue:** Command not found
- **Solution:** Make sure the installation directory is in your PATH

For more help, see the [Usage Guide](docs/usage.md).

## Support

- Report issues on the project issue tracker
- See `CONTRIBUTING.md` for how to contribute
- Check `docs/` for detailed documentation

## License

MIT License - see [LICENSE](LICENSE) for details.

## Changelog

### v0.1.0 - {datetime.now().strftime('%Y-%m-%d')}

- Initial release
- {len(spec.dependencies)} dependencies
- Core functionality implemented

---

*Built with the Agent-Orchestrated Code Factory*
*Designed for real-world use by real workers*
"""
        return readme

    def _generate_contributing(self, spec: ProjectSpec) -> str:
        """Generate CONTRIBUTING.md"""

        language = spec.tech_stack.get('language', 'Python').title()

        contributing = f"""# Contributing to {spec.name}

Thank you for your interest in contributing! This project is designed to help real workers solve real problems, and your contributions make it better.

## Getting Started

### Prerequisites

- {language} {self._get_version_requirement(language)}
- Git
- A code editor (VS Code, PyCharm, etc.)

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/yourusername/{spec.name}.git
cd {spec.name}
```

2. **Install dependencies**

{self._get_install_command(spec)}

3. **Run tests**

```bash
{self._get_test_command(spec)}
```

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if it's already reported in Issues
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, {language} version)
   - Any error messages

### Suggesting Features

We welcome feature suggestions! Please:

1. Check existing issues/discussions first
2. Create an issue describing:
   - The problem you're trying to solve
   - Why existing features don't work
   - How you envision the solution
   - Who would benefit (field workers, engineers, etc.)

### Submitting Changes

1. **Create a branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation

3. **Test your changes**

```bash
{self._get_test_command(spec)}
```

4. **Commit your changes**

```bash
git add .
git commit -m "Add feature: brief description"
```

Use clear commit messages:
- `Add feature: ...` for new features
- `Fix: ...` for bug fixes
- `Update: ...` for improvements
- `Docs: ...` for documentation

5. **Push and create Pull Request**

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear description of changes
- Why the change is needed
- Any testing done
- Screenshots (if UI changes)

## Code Style

{self._get_style_guide(spec)}

## Testing

- All new features must have tests
- Aim for >80% code coverage
- Test edge cases and error handling
- Tests should be clear and well-documented

## Documentation

- Update README.md if user-facing changes
- Update docs/ for new features
- Add docstrings to all functions/classes
- Include usage examples

## Review Process

1. Automated tests must pass
2. Code review by maintainer
3. Documentation review
4. Merge to main

## Code of Conduct

### Our Standards

- Be respectful and professional
- Focus on solving real problems
- Welcome newcomers
- Provide constructive feedback
- Remember: we're building tools for real workers

### Not Acceptable

- Harassment or discrimination
- Unconstructive criticism
- Off-topic discussions
- Spam or self-promotion

## Questions?

- Check existing issues and discussions
- Create a new issue with the "question" label
- Be patient - maintainers are volunteers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project credits

Thank you for helping make this tool better for everyone! 🛠️

---

*These guidelines ensure we build reliable tools that work in real-world conditions.*
"""
        return contributing

    def _generate_license(self, spec: ProjectSpec) -> str:
        """Generate MIT LICENSE"""

        year = datetime.now().year

        license_text = f"""MIT License

Copyright (c) {year} {spec.name} Contributors

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
        return license_text

    def _generate_usage_guide(self, spec: ProjectSpec, idea: Optional[Idea] = None) -> str:
        """Generate detailed usage guide"""

        language = spec.tech_stack.get('language', 'Python')
        cli_framework = spec.tech_stack.get('cli', '')

        usage_guide = f"""# Usage Guide: {spec.name}

This guide covers everything you need to use {spec.name} effectively.

## Quick Start

### Installation

{self._get_install_command(spec)}

### First Run

```bash
{self._get_basic_usage(spec, cli_framework)}
```

## Detailed Usage

### Basic Operations

{self._generate_basic_operations(spec, idea)}

### Advanced Features

{self._generate_advanced_features(spec, idea)}

### Command Reference

{self._generate_command_reference(spec, cli_framework)}

## Configuration

{self._generate_configuration_section(spec)}

## Examples

### Example 1: Basic Usage

```bash
# TODO: Add real example based on actual functionality
{self._get_basic_usage(spec, cli_framework)}
```

### Example 2: Advanced Usage

```bash
# TODO: Add advanced example
# This would include more complex scenarios
```

## Error Handling

Common errors and solutions:

### Error: "Module not found"
- **Cause:** Dependencies not installed
- **Solution:** Run `{self._get_install_command(spec)}`

### Error: "Permission denied"
- **Cause:** Insufficient file permissions
- **Solution:** Check file permissions, run with appropriate access

### Error: "Invalid input"
- **Cause:** Input format incorrect
- **Solution:** Check input format in command reference above

## Best Practices

1. **Always validate input** - Check data before processing
2. **Use offline mode** - Works without internet when needed
3. **Regular backups** - Keep copies of important data
4. **Check logs** - Review logs for troubleshooting

## Performance Tips

- For large datasets, process in batches
- Use caching when available
- Close resources properly
- Monitor memory usage for big operations

## Field Usage Notes

{self._generate_field_notes(spec, idea)}

## Troubleshooting

See the [README troubleshooting section](../README.md#troubleshooting) for common issues.

For additional help:
- Check error messages carefully
- Review logs
- Consult API documentation
- Report bugs in issue tracker

---

*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return usage_guide

    def _generate_architecture_doc(self, spec: ProjectSpec, idea: Optional[Idea] = None) -> str:
        """Generate architecture documentation"""

        # Build folder structure visualization
        folder_viz = self._visualize_folder_structure(spec.folder_structure)

        # Build tech stack section
        tech_stack_lines = []
        for key, value in spec.tech_stack.items():
            tech_stack_lines.append(f"- **{key.title()}:** {value}")
        tech_stack_section = '\n'.join(tech_stack_lines)

        # Build dependencies section
        dependencies_section = ""
        if spec.dependencies:
            deps_list = '\n'.join(f"- `{dep}`" for dep in spec.dependencies[:10])
            if len(spec.dependencies) > 10:
                deps_list += f"\n- ... and {len(spec.dependencies) - 10} more"
            dependencies_section = f"""### Dependencies

{deps_list}

See `requirements.txt` or `pyproject.toml` for complete list.
"""

        architecture = f"""# Architecture: {spec.name}

This document describes the design and structure of {spec.name}.

## Overview

{spec.description}

**Entry Point:** `{spec.entry_point}`

## Design Principles

1. **Simplicity** - Easy to understand and use
2. **Reliability** - Works consistently in field conditions
3. **Offline-first** - No internet required for core functionality
4. **Clear errors** - Helpful error messages that guide users
5. **Blue-collar focus** - Built for real workers, not developers

## Project Structure

```
{folder_viz}
```

## Technology Stack

{tech_stack_section}

### Why These Choices?

{self._explain_tech_choices(spec)}

{dependencies_section}

## Core Components

{self._describe_components(spec)}

## Data Flow

1. **Input** - User provides data via CLI or file
2. **Validation** - Input is checked for correctness
3. **Processing** - Core logic executes
4. **Output** - Results are displayed or saved
5. **Error Handling** - Errors are caught and reported clearly

## Design Decisions

### Blue-Collar Considerations

{self._describe_blue_collar_design(spec, idea)}

### Error Handling

- All errors are caught and explained in plain language
- Recovery suggestions are provided
- Logs are kept for debugging
- No crashes - graceful degradation

### Performance

- Designed for {self._estimate_scale(spec)}
- Optimized for typical field use cases
- Memory-efficient for resource-constrained environments

## Future Enhancements

Potential improvements:
- Additional features based on user feedback
- Performance optimizations
- Extended offline capabilities
- More export formats

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to contribute to this architecture.

---

*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return architecture

    def _generate_api_docs(self, spec: ProjectSpec, code_files: Dict[str, str]) -> Optional[str]:
        """Generate API documentation from code"""

        api_sections = []

        for file_path, code_content in code_files.items():
            if not file_path.endswith('.py'):
                continue

            try:
                tree = ast.parse(code_content)

                # Extract functions and classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        api_sections.append(self._document_function(node, file_path))
                    elif isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                        api_sections.append(self._document_class(node, file_path))

            except SyntaxError:
                continue

        if not api_sections:
            return None

        api_doc = f"""# API Documentation: {spec.name}

This document describes the public API for {spec.name}.

## Overview

{spec.description}

---

{chr(10).join(api_sections)}

---

*Auto-generated API documentation*
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return api_doc

    def _generate_gitignore(self, spec: ProjectSpec) -> str:
        """Generate .gitignore file"""

        language = spec.tech_stack.get('language', 'python').lower()

        if 'python' in language:
            return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Local config
.env
.env.local
config.local.*

# Build artifacts
*.pyc
*.pyo
*.pyd
"""
        else:
            # Generic gitignore
            return """# Build artifacts
build/
dist/
*.o
*.so
*.dylib

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Local config
.env
"""

    # Helper methods

    def _build_installation_section(self, spec: ProjectSpec, language: str) -> str:
        """Build installation instructions"""
        if 'python' in language.lower():
            return """## Installation

### Option 1: Using pip

```bash
pip install -e .
```

### Option 2: Using uv (recommended)

```bash
uv sync
```

### Option 3: Manual

```bash
git clone <repository-url>
cd """ + spec.name + """
pip install -r requirements.txt
```
"""
        return f"""## Installation

```bash
# Installation instructions for {language}
```
"""

    def _build_usage_section(self, spec: ProjectSpec, cli_framework: str) -> str:
        """Build usage section"""
        entry_point = spec.entry_point.replace('.py', '').replace('/', '.')

        if cli_framework:
            return f"""## Usage

### Basic Command

```bash
python -m {entry_point} --help
```

### Example

```bash
python -m {entry_point} [arguments]
```

See [Usage Guide](docs/usage.md) for detailed examples.
"""
        return f"""## Usage

```bash
python {spec.entry_point}
```

See [Usage Guide](docs/usage.md) for detailed examples.
"""

    def _get_version_requirement(self, language: str) -> str:
        """Get version requirement for language"""
        if 'python' in language.lower():
            return "3.11+"
        return "latest"

    def _get_dependency_file(self, spec: ProjectSpec) -> str:
        """Get dependency file name"""
        language = spec.tech_stack.get('language', 'python').lower()
        if 'python' in language:
            return 'pyproject.toml or requirements.txt'
        return 'package manifest'

    def _get_install_command(self, spec: ProjectSpec) -> str:
        """Get installation command"""
        language = spec.tech_stack.get('language', 'python').lower()
        if 'python' in language:
            return '```bash\npip install -e .\n# or\nuv sync\n```'
        return '```bash\n# Install dependencies\n```'

    def _get_test_command(self, spec: ProjectSpec) -> str:
        """Get test command"""
        language = spec.tech_stack.get('language', 'python').lower()
        if 'python' in language:
            return 'pytest'
        return '# Run tests'

    def _get_style_guide(self, spec: ProjectSpec) -> str:
        """Get style guide for language"""
        language = spec.tech_stack.get('language', 'python').lower()
        if 'python' in language:
            return """- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use ruff for linting: `ruff check .`
- Use black for formatting: `black .`"""
        return "Follow project conventions"

    def _get_basic_usage(self, spec: ProjectSpec, cli_framework: str) -> str:
        """Get basic usage command"""
        if cli_framework:
            return f"python -m {spec.name.replace('-', '_')} --help"
        return f"python {spec.entry_point}"

    def _generate_basic_operations(self, spec: ProjectSpec, idea: Optional[Idea]) -> str:
        """Generate basic operations section"""
        return """TODO: Document basic operations based on actual features

This section will include:
- Core commands
- Common use cases
- Input/output formats
"""

    def _generate_advanced_features(self, spec: ProjectSpec, idea: Optional[Idea]) -> str:
        """Generate advanced features section"""
        return """TODO: Document advanced features

This section will include:
- Advanced options
- Configuration
- Automation
- Integration with other tools
"""

    def _generate_command_reference(self, spec: ProjectSpec, cli_framework: str) -> str:
        """Generate command reference"""
        return f"""TODO: Complete command reference

```bash
{self._get_basic_usage(spec, cli_framework)}
```

Arguments and options will be documented here.
"""

    def _generate_configuration_section(self, spec: ProjectSpec) -> str:
        """Generate configuration section"""
        return """Configuration options (if available):

- Environment variables
- Configuration files
- Command-line flags

TODO: Document actual configuration options
"""

    def _generate_field_notes(self, spec: ProjectSpec, idea: Optional[Idea]) -> str:
        """Generate field usage notes"""
        notes = ["This tool is designed for field use:"]

        if idea:
            if idea.environment:
                notes.append(f"- **Environment:** {idea.environment}")
            if idea.constraints:
                notes.append("- **Constraints:**")
                for constraint in idea.constraints:
                    notes.append(f"  - {constraint}")

        notes.append("- Works offline (internet not required for core features)")
        notes.append("- Handles errors gracefully")
        notes.append("- Clear feedback on all operations")

        return '\n'.join(notes)

    def _visualize_folder_structure(self, folder_structure: Dict[str, List[str]]) -> str:
        """Create visual representation of folder structure"""
        lines = []
        for folder, files in sorted(folder_structure.items()):
            folder_clean = folder.rstrip('/')
            lines.append(f"{folder_clean}/")
            for file in files:
                lines.append(f"├── {file}")
        return '\n'.join(lines) if lines else "project/"

    def _explain_tech_choices(self, spec: ProjectSpec) -> str:
        """Explain technology choices"""
        explanations = []

        language = spec.tech_stack.get('language', '').lower()
        if 'python' in language:
            explanations.append("- **Python**: Easy to learn, excellent for CLI tools, good library support")

        cli = spec.tech_stack.get('cli', '').lower()
        if 'typer' in cli:
            explanations.append("- **Typer**: Modern CLI framework with great UX")
        elif 'click' in cli:
            explanations.append("- **Click**: Robust CLI framework, industry standard")

        if not explanations:
            explanations.append("- Technology chosen for reliability and ease of use")

        return '\n'.join(explanations)

    def _describe_components(self, spec: ProjectSpec) -> str:
        """Describe core components"""
        return f"""### Main Entry Point

`{spec.entry_point}` - Application entry point

### Core Modules

Based on the project structure, core modules handle:
- Input validation
- Data processing
- Output generation
- Error handling

See code for detailed component descriptions.
"""

    def _describe_blue_collar_design(self, spec: ProjectSpec, idea: Optional[Idea]) -> str:
        """Describe blue-collar design decisions"""
        points = [
            "- **Clear error messages** - No technical jargon, plain language",
            "- **Offline-first** - Core features work without internet",
            "- **Simple interface** - Minimal learning curve",
            "- **Reliable** - Handles errors gracefully, no crashes",
        ]

        if idea and idea.target_users:
            points.insert(0, f"- **Built for {', '.join(idea.target_users)}**")

        return '\n'.join(points)

    def _estimate_scale(self, spec: ProjectSpec) -> str:
        """Estimate typical scale"""
        return "typical field use cases (hundreds to thousands of records)"

    def _document_function(self, node: ast.FunctionDef, file_path: str) -> str:
        """Document a function from AST"""
        docstring = ast.get_docstring(node) or "No description available"

        # Extract parameters
        params = []
        for arg in node.args.args:
            params.append(arg.arg)

        params_str = ', '.join(params) if params else 'None'

        return f"""### `{node.name}()`

**File:** `{file_path}`

**Parameters:** {params_str}

**Description:**

{docstring}

---
"""

    def _document_class(self, node: ast.ClassDef, file_path: str) -> str:
        """Document a class from AST"""
        docstring = ast.get_docstring(node) or "No description available"

        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                methods.append(f"- `{item.name}()`")

        methods_str = '\n'.join(methods) if methods else "No public methods"

        return f"""### Class: `{node.name}`

**File:** `{file_path}`

**Description:**

{docstring}

**Methods:**

{methods_str}

---
"""
