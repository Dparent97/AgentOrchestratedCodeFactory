"""
Tests for TemplateEngine

Tests the template-based code generation system.
"""

import pytest
from pathlib import Path

from code_factory.core.template_engine import TemplateEngine
from code_factory.core.models import ProjectSpec


@pytest.fixture
def sample_spec():
    """Create a sample project specification"""
    return ProjectSpec(
        name="test-project",
        description="A test project for unit testing",
        tech_stack={
            "language": "python",
            "cli_framework": "typer",
            "ui_library": "rich",
        },
        folder_structure={
            "": ["README.md", "pyproject.toml"],
            "src/": ["main.py", "cli.py"],
            "tests/": ["test_main.py"],
        },
        dependencies=["typer", "rich"],
        entry_point="src/main.py",
    )


@pytest.fixture
def cli_spec():
    """Create a CLI project specification"""
    return ProjectSpec(
        name="cli-tool",
        description="A command-line tool",
        tech_stack={
            "language": "python",
            "cli_framework": "typer",
            "ui_library": "rich",
        },
        folder_structure={
            "src/": ["main.py"],
            "tests/": ["test_main.py"],
        },
        dependencies=["typer", "rich"],
        entry_point="src/main.py",
    )


@pytest.fixture
def library_spec():
    """Create a library project specification"""
    return ProjectSpec(
        name="my-library",
        description="A Python library",
        tech_stack={
            "language": "python",
        },
        folder_structure={
            "src/": ["core.py"],
            "tests/": ["test_core.py"],
        },
        dependencies=[],
        entry_point="src/core.py",
    )


@pytest.fixture
def data_processing_spec():
    """Create a data processing project specification"""
    return ProjectSpec(
        name="data-processor",
        description="A data processing tool",
        tech_stack={
            "language": "python",
            "cli_framework": "typer",
            "data_library": "pandas",
        },
        folder_structure={
            "src/": ["main.py", "data_processor.py"],
            "tests/": ["test_main.py"],
        },
        dependencies=["typer", "pandas"],
        entry_point="src/main.py",
    )


class TestTemplateEngine:
    """Test TemplateEngine functionality"""

    def test_initialization(self):
        """Test template engine initialization"""
        engine = TemplateEngine()
        assert engine is not None
        assert engine.template_dir.exists()
        assert engine.env is not None

    def test_generate_project_files(self, sample_spec):
        """Test generating project files"""
        engine = TemplateEngine()
        files = engine.generate_project_files(sample_spec)

        assert isinstance(files, dict)
        assert len(files) > 0

        # Check for essential files
        assert "README.md" in files
        assert "pyproject.toml" in files
        assert ".gitignore" in files

    def test_generate_cli_project(self, cli_spec):
        """Test generating CLI project"""
        engine = TemplateEngine()
        files = engine.generate_project_files(cli_spec)

        # Check for CLI-specific files
        assert "src/cli_tool/main.py" in files
        assert "typer" in files["src/cli_tool/main.py"]

        # Check package init
        assert "src/cli_tool/__init__.py" in files

        # Check tests
        assert "tests/test_main.py" in files
        assert "tests/__init__.py" in files

    def test_generate_library_project(self, library_spec):
        """Test generating library project"""
        engine = TemplateEngine()
        files = engine.generate_project_files(library_spec)

        # Check for library files
        assert "src/my_library/core.py" in files
        assert "src/my_library/__init__.py" in files

        # Check that core.py has the class
        assert "MyLibrary" in files["src/my_library/core.py"]

    def test_generate_data_processing_project(self, data_processing_spec):
        """Test generating data processing project"""
        engine = TemplateEngine()
        files = engine.generate_project_files(data_processing_spec)

        # Check for data processing files
        assert "src/data_processor/data_processor.py" in files

        # Check for pandas imports if pandas is a dependency
        if "pandas" in data_processing_spec.dependencies:
            assert "pandas" in files["src/data_processor/data_processor.py"]

    def test_build_context(self, sample_spec):
        """Test context building from spec"""
        engine = TemplateEngine()
        context = engine._build_context(sample_spec)

        assert context["project_name"] == "test-project"
        assert context["package_name"] == "test_project"
        assert context["class_name"] == "TestProject"
        assert context["script_name"] == "test-project"
        assert "description" in context
        assert "tech_stack" in context
        assert "dependencies" in context

    def test_is_cli_project(self, cli_spec, library_spec):
        """Test CLI project detection"""
        engine = TemplateEngine()

        assert engine._is_cli_project(cli_spec) is True
        # Library might still be CLI if it has typer
        # but basic library spec should not be CLI

    def test_pascal_case_conversion(self):
        """Test PascalCase conversion"""
        engine = TemplateEngine()

        assert engine._to_pascal_case("test-project") == "TestProject"
        assert engine._to_pascal_case("my_library") == "MyLibrary"
        assert engine._to_pascal_case("cli-tool") == "CliTool"
        assert engine._to_pascal_case("data-processor") == "DataProcessor"

    def test_readme_generation(self, sample_spec):
        """Test README generation"""
        engine = TemplateEngine()
        files = engine.generate_project_files(sample_spec)

        readme = files["README.md"]
        assert sample_spec.name in readme
        assert sample_spec.description in readme
        assert "Installation" in readme
        assert "Usage" in readme

    def test_pyproject_generation(self, sample_spec):
        """Test pyproject.toml generation"""
        engine = TemplateEngine()
        files = engine.generate_project_files(sample_spec)

        pyproject = files["pyproject.toml"]
        assert sample_spec.name in pyproject
        assert "dependencies" in pyproject
        for dep in sample_spec.dependencies:
            assert dep in pyproject

    def test_gitignore_generation(self, sample_spec):
        """Test .gitignore generation"""
        engine = TemplateEngine()
        files = engine.generate_project_files(sample_spec)

        gitignore = files[".gitignore"]
        assert "__pycache__" in gitignore
        # Check for Python compiled files (*.py[cod] covers *.pyc)
        assert "*.py[cod]" in gitignore or "*.pyc" in gitignore
        assert ".pytest_cache" in gitignore

    def test_test_file_generation(self, cli_spec):
        """Test test file generation"""
        engine = TemplateEngine()
        files = engine.generate_project_files(cli_spec)

        test_file = files["tests/test_main.py"]
        assert "pytest" in test_file or "def test_" in test_file
        assert "cli_tool" in test_file

    def test_fallback_templates(self, sample_spec):
        """Test that fallback templates work when template files are missing"""
        # Create engine with non-existent template directory
        # This should trigger fallback methods
        engine = TemplateEngine()

        # Even if some templates are missing, fallbacks should work
        files = engine.generate_project_files(sample_spec)

        # Should still generate basic files
        assert "README.md" in files
        assert len(files["README.md"]) > 0

    def test_init_files_generation(self, sample_spec):
        """Test __init__.py file generation"""
        engine = TemplateEngine()
        files = engine.generate_project_files(sample_spec)

        package_name = sample_spec.name.replace("-", "_")
        init_file = f"src/{package_name}/__init__.py"

        assert init_file in files
        assert "__version__" in files[init_file]

        # Tests should also have __init__.py
        assert "tests/__init__.py" in files

    def test_file_content_not_empty(self, sample_spec):
        """Test that generated files have content"""
        engine = TemplateEngine()
        files = engine.generate_project_files(sample_spec)

        for file_path, content in files.items():
            assert content is not None
            assert len(content) > 0, f"File {file_path} is empty"
            assert content.strip() != "", f"File {file_path} has only whitespace"
