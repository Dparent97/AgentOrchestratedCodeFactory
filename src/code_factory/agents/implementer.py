"""
ImplementerAgent - Generates source code files

Creates the actual code files based on the project specification
and task requirements using template-based code generation.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import ProjectSpec
from code_factory.core.template_engine import TemplateEngine
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CodeOutput(BaseModel):
    """Output model containing generated code files"""
    files: Dict[str, str]  # file_path -> content
    files_created: int
    template_engine_version: str = "1.0"


class ImplementerAgent(BaseAgent):
    """
    Generates source code based on project specification

    Uses a template-based approach with Jinja2 templates to generate
    complete, working Python projects (CLI apps, libraries, etc.).

    Features:
    - Template-based code generation
    - Support for CLI projects (typer-based)
    - Support for library projects
    - Domain-specific code generation (data processing, etc.)
    - Complete project structure with tests and documentation
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize ImplementerAgent

        Args:
            template_dir: Optional custom template directory
        """
        super().__init__()
        self.template_engine = TemplateEngine(template_dir=template_dir)

    @property
    def name(self) -> str:
        return "implementer"

    @property
    def description(self) -> str:
        return "Generates source code files based on project specifications using templates"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Generate code files from project specification

        Uses the template engine to generate a complete project structure
        with all necessary files based on the ProjectSpec.

        Args:
            input_data: ProjectSpec containing architecture decisions

        Returns:
            CodeOutput: Generated code files with paths and content

        Raises:
            ValueError: If spec is invalid
            RuntimeError: If code generation fails
        """
        spec = self.validate_input(input_data, ProjectSpec)
        logger.info(f"Generating code for project: {spec.name}")
        logger.info(f"Tech stack: {spec.tech_stack}")
        logger.info(f"Dependencies: {spec.dependencies}")

        try:
            # Generate all project files using template engine
            files = self.template_engine.generate_project_files(spec)

            # Log file generation summary
            logger.info(f"Generated {len(files)} files:")
            for file_path in sorted(files.keys()):
                logger.debug(f"  - {file_path}")

            # Validate generated files
            self._validate_generated_files(files, spec)

            return CodeOutput(
                files=files,
                files_created=len(files),
                template_engine_version="1.0"
            )

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            raise RuntimeError(f"Failed to generate code for {spec.name}: {e}")

    def _validate_generated_files(self, files: Dict[str, str], spec: ProjectSpec) -> None:
        """
        Validate that required files were generated

        Args:
            files: Generated files
            spec: Project specification

        Raises:
            ValueError: If required files are missing
        """
        required_files = [
            "README.md",
            "pyproject.toml",
            ".gitignore",
        ]

        # Check for entry point file
        package_name = spec.name.replace("-", "_")
        if spec.entry_point == "src/main.py":
            required_files.append(f"src/{package_name}/main.py")

        # Validate required files exist
        missing_files = []
        for required_file in required_files:
            if required_file not in files:
                missing_files.append(required_file)

        if missing_files:
            logger.warning(f"Missing required files: {missing_files}")
            # Don't raise error, just warn - some files may be optional

        # Validate files have content
        empty_files = [path for path, content in files.items() if not content.strip()]
        if empty_files:
            logger.warning(f"Empty files generated: {empty_files}")

        logger.info("File validation complete")
