"""
Tests for ImplementerAgent

Tests the code generation agent with template-based implementation.
"""

import pytest

from code_factory.agents.implementer import ImplementerAgent, CodeOutput
from code_factory.core.models import ProjectSpec


@pytest.fixture
def implementer():
    """Create an ImplementerAgent instance"""
    return ImplementerAgent()


@pytest.fixture
def sample_spec():
    """Create a sample project specification"""
    return ProjectSpec(
        name="test-cli-tool",
        description="A test command-line tool",
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
def minimal_spec():
    """Create a minimal project specification"""
    return ProjectSpec(
        name="minimal-project",
        description="Minimal project",
        tech_stack={"language": "python"},
        folder_structure={"src/": ["core.py"]},
        dependencies=[],
        entry_point="src/core.py",
    )


class TestImplementerAgent:
    """Test ImplementerAgent functionality"""

    def test_agent_properties(self, implementer):
        """Test agent name and description"""
        assert implementer.name == "implementer"
        assert "template" in implementer.description.lower()

    def test_execute_returns_code_output(self, implementer, sample_spec):
        """Test that execute returns CodeOutput"""
        result = implementer.execute(sample_spec)

        assert isinstance(result, CodeOutput)
        assert hasattr(result, "files")
        assert hasattr(result, "files_created")
        assert hasattr(result, "template_engine_version")

    def test_generate_files_from_spec(self, implementer, sample_spec):
        """Test generating files from specification"""
        result = implementer.execute(sample_spec)

        assert isinstance(result.files, dict)
        assert result.files_created > 0
        assert len(result.files) == result.files_created

    def test_generated_files_include_essentials(self, implementer, sample_spec):
        """Test that essential files are generated"""
        result = implementer.execute(sample_spec)
        files = result.files

        # Check essential files
        assert "README.md" in files
        assert "pyproject.toml" in files
        assert ".gitignore" in files

    def test_generated_files_include_source_code(self, implementer, sample_spec):
        """Test that source code files are generated"""
        result = implementer.execute(sample_spec)
        files = result.files

        # Should have main.py for CLI project
        package_name = sample_spec.name.replace("-", "_")
        assert f"src/{package_name}/main.py" in files

        # Should have __init__.py
        assert f"src/{package_name}/__init__.py" in files

    def test_generated_files_include_tests(self, implementer, sample_spec):
        """Test that test files are generated"""
        result = implementer.execute(sample_spec)
        files = result.files

        # Should have test files
        assert "tests/test_main.py" in files
        assert "tests/__init__.py" in files

    def test_cli_project_has_typer_code(self, implementer, sample_spec):
        """Test that CLI project includes typer imports"""
        result = implementer.execute(sample_spec)
        files = result.files

        package_name = sample_spec.name.replace("-", "_")
        main_py = files.get(f"src/{package_name}/main.py", "")

        assert "typer" in main_py.lower()
        assert "import typer" in main_py or "from typer" in main_py

    def test_readme_contains_project_info(self, implementer, sample_spec):
        """Test that README contains project information"""
        result = implementer.execute(sample_spec)
        readme = result.files["README.md"]

        assert sample_spec.name in readme
        assert sample_spec.description in readme

    def test_pyproject_has_dependencies(self, implementer, sample_spec):
        """Test that pyproject.toml includes dependencies"""
        result = implementer.execute(sample_spec)
        pyproject = result.files["pyproject.toml"]

        for dep in sample_spec.dependencies:
            assert dep in pyproject

    def test_validate_generated_files(self, implementer, sample_spec):
        """Test file validation"""
        result = implementer.execute(sample_spec)

        # Validation should pass without raising errors
        implementer._validate_generated_files(result.files, sample_spec)

    def test_minimal_project_generation(self, implementer, minimal_spec):
        """Test generating minimal project"""
        result = implementer.execute(minimal_spec)

        assert result.files_created > 0
        assert "README.md" in result.files
        assert "pyproject.toml" in result.files

    def test_different_project_names(self, implementer):
        """Test generation with different project name formats"""
        # Test kebab-case name
        spec1 = ProjectSpec(
            name="my-test-project",
            description="Test",
            tech_stack={"language": "python"},
            folder_structure={},
            dependencies=[],
            entry_point="src/main.py",
        )
        result1 = implementer.execute(spec1)
        assert result1.files_created > 0
        assert "src/my_test_project/__init__.py" in result1.files

        # Test snake_case name
        spec2 = ProjectSpec(
            name="my_other_project",
            description="Test",
            tech_stack={"language": "python"},
            folder_structure={},
            dependencies=[],
            entry_point="src/main.py",
        )
        result2 = implementer.execute(spec2)
        assert result2.files_created > 0
        assert "src/my_other_project/__init__.py" in result2.files

    def test_error_handling_invalid_spec(self, implementer):
        """Test error handling with invalid input"""
        # This should raise an error due to type mismatch
        with pytest.raises(Exception):
            implementer.execute("not a valid spec")

    def test_file_content_quality(self, implementer, sample_spec):
        """Test that generated files have quality content"""
        result = implementer.execute(sample_spec)

        for file_path, content in result.files.items():
            # Files should not be empty
            assert len(content) > 0, f"{file_path} is empty"

            # Python files should have proper structure
            if file_path.endswith(".py"):
                # Should have docstrings or comments
                assert '"""' in content or "#" in content

            # TOML files should be valid format
            if file_path.endswith(".toml"):
                assert "[" in content  # Section headers

    def test_template_engine_version(self, implementer, sample_spec):
        """Test that output includes template engine version"""
        result = implementer.execute(sample_spec)

        assert result.template_engine_version is not None
        assert isinstance(result.template_engine_version, str)
        assert len(result.template_engine_version) > 0

    def test_library_project_has_class(self, implementer):
        """Test that library projects have a main class"""
        spec = ProjectSpec(
            name="my-library",
            description="A Python library",
            tech_stack={"language": "python"},
            folder_structure={"src/": ["core.py"]},
            dependencies=[],
            entry_point="src/core.py",
        )

        result = implementer.execute(spec)
        core_py = result.files.get("src/my_library/core.py", "")

        # Should have a class definition
        assert "class " in core_py
        assert "MyLibrary" in core_py

    def test_data_processing_project(self, implementer):
        """Test data processing project generation"""
        spec = ProjectSpec(
            name="data-tool",
            description="Data processing tool",
            tech_stack={
                "language": "python",
                "data_library": "pandas",
            },
            folder_structure={"src/": ["data_processor.py"]},
            dependencies=["pandas"],
            entry_point="src/main.py",
        )

        result = implementer.execute(spec)

        # Should have data processor file
        assert "src/data_tool/data_processor.py" in result.files
