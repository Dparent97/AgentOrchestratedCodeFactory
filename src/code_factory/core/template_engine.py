"""
Template Engine for Code Generation

Provides template-based code generation using Jinja2 templates.
Supports multiple project types (CLI, library) and domains.
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from code_factory.core.models import ProjectSpec

logger = logging.getLogger(__name__)


class TemplateEngine:
    """
    Engine for rendering code templates

    Uses Jinja2 to render project files from templates based on
    ProjectSpec and domain-specific requirements.
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize template engine

        Args:
            template_dir: Directory containing templates (defaults to package templates)
        """
        if template_dir is None:
            # Use package templates
            package_root = Path(__file__).parent.parent
            template_dir = package_root / "templates"

        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")

        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        logger.info(f"Template engine initialized with directory: {self.template_dir}")

    def render_template(self, template_path: str, context: Dict[str, Any]) -> str:
        """
        Render a single template

        Args:
            template_path: Relative path to template file (e.g., "cli/main.py.j2")
            context: Template context variables

        Returns:
            Rendered template content

        Raises:
            TemplateNotFound: If template doesn't exist
        """
        try:
            template = self.env.get_template(template_path)
            rendered = template.render(**context)
            logger.debug(f"Rendered template: {template_path}")
            return rendered
        except TemplateNotFound:
            logger.error(f"Template not found: {template_path}")
            raise
        except Exception as e:
            logger.error(f"Error rendering template {template_path}: {e}")
            raise

    def generate_project_files(self, spec: ProjectSpec) -> Dict[str, str]:
        """
        Generate all project files from spec

        Args:
            spec: Project specification

        Returns:
            Dict mapping file paths to content
        """
        files = {}
        context = self._build_context(spec)

        logger.info(f"Generating files for project: {spec.name}")

        # Determine project type (CLI, library, or both)
        is_cli = self._is_cli_project(spec)
        is_library = self._is_library_project(spec)

        # Generate common files (always created)
        files.update(self._generate_common_files(context))

        # Generate CLI files if needed
        if is_cli:
            files.update(self._generate_cli_files(context))

        # Generate library files if needed
        if is_library:
            files.update(self._generate_library_files(context, spec))

        # Generate domain-specific files
        files.update(self._generate_domain_files(context, spec))

        # Generate test files
        files.update(self._generate_test_files(context, is_cli))

        # Generate __init__.py files for Python packages
        files.update(self._generate_init_files(spec))

        logger.info(f"Generated {len(files)} files")
        return files

    def _build_context(self, spec: ProjectSpec) -> Dict[str, Any]:
        """
        Build template context from ProjectSpec

        Args:
            spec: Project specification

        Returns:
            Context dictionary for templates
        """
        # Extract package name (convert hyphens to underscores)
        package_name = spec.name.replace("-", "_")

        # Generate script name for CLI
        script_name = spec.name

        # Generate class name (PascalCase)
        class_name = self._to_pascal_case(spec.name)

        context = {
            "project_name": spec.name,
            "package_name": package_name,
            "script_name": script_name,
            "class_name": class_name,
            "description": spec.description,
            "tech_stack": spec.tech_stack,
            "dependencies": spec.dependencies,
            "entry_point": spec.entry_point,
            "environment": spec.environment,
            "user_profile": spec.user_profile,
            "features": [],  # Will be populated from description/tasks
        }

        return context

    def _is_cli_project(self, spec: ProjectSpec) -> bool:
        """Check if project is a CLI application"""
        return (
            "cli" in spec.tech_stack.get("cli_framework", "").lower()
            or "typer" in spec.dependencies
            or spec.entry_point == "src/main.py"
        )

    def _is_library_project(self, spec: ProjectSpec) -> bool:
        """Check if project is a library (has core functionality)"""
        # Most projects have some library component
        return True

    def _generate_common_files(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate common project files"""
        files = {}

        # README.md
        try:
            files["README.md"] = self.render_template("common/README.md.j2", context)
        except TemplateNotFound:
            files["README.md"] = self._fallback_readme(context)

        # pyproject.toml
        try:
            files["pyproject.toml"] = self.render_template("common/pyproject.toml.j2", context)
        except TemplateNotFound:
            files["pyproject.toml"] = self._fallback_pyproject(context)

        # .gitignore
        try:
            files[".gitignore"] = self.render_template("common/gitignore.j2", context)
        except TemplateNotFound:
            files[".gitignore"] = self._fallback_gitignore()

        return files

    def _generate_cli_files(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate CLI-specific files"""
        files = {}
        package_name = context["package_name"]

        # Main CLI entry point
        try:
            files[f"src/{package_name}/main.py"] = self.render_template(
                "cli/main.py.j2", context
            )
        except TemplateNotFound:
            files[f"src/{package_name}/main.py"] = self._fallback_cli_main(context)

        # CLI utilities
        try:
            files[f"src/{package_name}/cli.py"] = self.render_template(
                "cli/cli.py.j2", context
            )
        except TemplateNotFound:
            pass  # Optional file

        return files

    def _generate_library_files(
        self, context: Dict[str, Any], spec: ProjectSpec
    ) -> Dict[str, str]:
        """Generate library/core files"""
        files = {}
        package_name = context["package_name"]

        # Core module
        try:
            files[f"src/{package_name}/core.py"] = self.render_template(
                "library/core.py.j2", context
            )
        except TemplateNotFound:
            files[f"src/{package_name}/core.py"] = self._fallback_core(context)

        return files

    def _generate_domain_files(
        self, context: Dict[str, Any], spec: ProjectSpec
    ) -> Dict[str, str]:
        """Generate domain-specific files based on folder structure"""
        files = {}
        package_name = context["package_name"]

        # Check for data processing domain
        if "data_library" in spec.tech_stack:
            try:
                files[f"src/{package_name}/data_processor.py"] = self.render_template(
                    "library/data_processor.py.j2", context
                )
            except TemplateNotFound:
                pass  # Optional

        return files

    def _generate_test_files(self, context: Dict[str, Any], is_cli: bool) -> Dict[str, str]:
        """Generate test files"""
        files = {}

        # Main test file
        try:
            files["tests/test_main.py"] = self.render_template(
                "common/test_main.py.j2", context
            )
        except TemplateNotFound:
            files["tests/test_main.py"] = self._fallback_test(context, is_cli)

        return files

    def _generate_init_files(self, spec: ProjectSpec) -> Dict[str, str]:
        """Generate __init__.py files for Python packages"""
        files = {}
        package_name = spec.name.replace("-", "_")
        class_name = self._to_pascal_case(spec.name)

        # Main package __init__.py
        try:
            context = {"project_name": spec.name, "description": spec.description, "class_name": class_name}
            files[f"src/{package_name}/__init__.py"] = self.render_template(
                "library/__init__.py.j2", context
            )
        except TemplateNotFound:
            files[f"src/{package_name}/__init__.py"] = (
                f'"""\n{spec.name}\n\n{spec.description}\n"""\n\n'
                f'__version__ = "0.1.0"\n'
            )

        # Tests __init__.py
        files["tests/__init__.py"] = '"""Test suite for {}"""\n'.format(spec.name)

        return files

    def _to_pascal_case(self, snake_or_kebab: str) -> str:
        """Convert snake_case or kebab-case to PascalCase"""
        words = re.split(r"[-_]", snake_or_kebab)
        return "".join(word.capitalize() for word in words if word)

    # Fallback methods for when templates are missing

    def _fallback_readme(self, context: Dict[str, Any]) -> str:
        """Fallback README template"""
        return f"""# {context['project_name']}

{context['description']}

## Installation

```bash
pip install -e .
```

## Usage

```bash
{context['script_name']} --help
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
"""

    def _fallback_pyproject(self, context: Dict[str, Any]) -> str:
        """Fallback pyproject.toml template"""
        deps = '\n'.join(f'    "{dep}",' for dep in context['dependencies'])
        return f"""[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{context['project_name']}"
version = "0.1.0"
description = "{context['description']}"
requires-python = ">=3.11"
dependencies = [
{deps}
]

[project.scripts]
{context['script_name']} = "{context['package_name']}.main:app"
"""

    def _fallback_gitignore(self) -> str:
        """Fallback .gitignore template"""
        return """__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.venv/
venv/
.env
"""

    def _fallback_cli_main(self, context: Dict[str, Any]) -> str:
        """Fallback CLI main template"""
        return f"""import typer

app = typer.Typer()

@app.command()
def main():
    \"\"\"Main command for {context['project_name']}\"\"\"
    print("Hello from {context['project_name']}!")

if __name__ == "__main__":
    app()
"""

    def _fallback_core(self, context: Dict[str, Any]) -> str:
        """Fallback core module template"""
        return f'''"""Core functionality for {context['project_name']}"""

class {context['class_name']}:
    """Main class for {context['project_name']}"""

    def __init__(self):
        """Initialize {context['class_name']}"""
        pass
'''

    def _fallback_test(self, context: Dict[str, Any], is_cli: bool) -> str:
        """Fallback test template"""
        if is_cli:
            return f"""from typer.testing import CliRunner
from {context['package_name']}.main import app

runner = CliRunner()

def test_main():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
"""
        else:
            return f"""from {context['package_name']}.core import {context['class_name']}

def test_initialization():
    instance = {context['class_name']}()
    assert instance is not None
"""
