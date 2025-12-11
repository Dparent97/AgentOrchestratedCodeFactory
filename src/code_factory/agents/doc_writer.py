"""
DocWriterAgent - Generates project documentation

Creates README files, usage guides, API documentation,
and other user-facing documentation.
"""

import logging
import re
from typing import Dict, List, Optional

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import AdvisoryReport, ProjectSpec
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DocInput(BaseModel):
    """Input for documentation generation"""
    spec: ProjectSpec
    advisory: Optional[AdvisoryReport] = None
    code_files: Optional[Dict[str, str]] = None


class DocOutput(BaseModel):
    """Output containing generated documentation files"""
    files: Dict[str, str]  # file_path -> content


class DocWriterAgent(BaseAgent):
    """
    Generates user-facing documentation
    
    Algorithm:
    1. Analyze ProjectSpec for documentation needs
    2. Generate README.md with sections: description, install, usage, API
    3. Generate usage guide if features are substantial
    4. Include accessibility notes from AdvisoryReport if provided
    5. Return dict of doc files (path → content)
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
            input_data: ProjectSpec or DocInput
            
        Returns:
            DocOutput: Generated documentation files
        """
        # Handle both ProjectSpec and DocInput
        if isinstance(input_data, ProjectSpec):
            spec = input_data
            advisory = None
            code_files = None
        else:
            doc_input = self.validate_input(input_data, DocInput)
            spec = doc_input.spec
            advisory = doc_input.advisory
            code_files = doc_input.code_files
        
        logger.info(f"Generating documentation for: {spec.name}")
        
        files: Dict[str, str] = {}
        
        # Step 1: Generate README.md
        readme_content = self._generate_readme(spec, advisory)
        files["README.md"] = readme_content
        
        # Step 2: Generate usage guide
        usage_content = self._generate_usage_guide(spec, advisory)
        files["docs/usage.md"] = usage_content
        
        # Step 3: Generate API reference if we have code files
        if code_files:
            api_content = self._generate_api_reference(spec, code_files)
            files["docs/api.md"] = api_content
        
        # Step 4: Generate installation guide
        install_content = self._generate_install_guide(spec)
        files["docs/installation.md"] = install_content
        
        # Step 5: Generate contributing guide
        contributing_content = self._generate_contributing_guide(spec)
        files["CONTRIBUTING.md"] = contributing_content
        
        # Step 6: Generate changelog template
        changelog_content = self._generate_changelog()
        files["CHANGELOG.md"] = changelog_content
        
        logger.info(f"Generated {len(files)} documentation files")
        return DocOutput(files=files)
    
    def _generate_readme(
        self, 
        spec: ProjectSpec, 
        advisory: Optional[AdvisoryReport] = None
    ) -> str:
        """
        Generate comprehensive README.md
        
        Args:
            spec: Project specification
            advisory: Optional advisory report for accessibility notes
            
        Returns:
            README.md content
        """
        sections = []
        
        # Title and description
        sections.append(f"# {self._format_title(spec.name)}")
        sections.append("")
        sections.append(spec.description)
        sections.append("")
        
        # Badges (placeholder)
        sections.append("![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)")
        sections.append("![License](https://img.shields.io/badge/license-MIT-green)")
        sections.append("")
        
        # Features section
        features = self._extract_features(spec)
        if features:
            sections.append("## Features")
            sections.append("")
            for feature in features:
                sections.append(f"- {feature}")
            sections.append("")
        
        # Environment compatibility
        if spec.environment or spec.user_profile:
            sections.append("## Designed For")
            sections.append("")
            if spec.user_profile:
                sections.append(f"- **Target Users**: {spec.user_profile}")
            if spec.environment:
                sections.append(f"- **Environment**: {spec.environment}")
            sections.append("")
        
        # Quick Start
        sections.append("## Quick Start")
        sections.append("")
        sections.append("```bash")
        sections.append("# Clone the repository")
        sections.append(f"git clone https://github.com/yourusername/{spec.name}.git")
        sections.append(f"cd {spec.name}")
        sections.append("")
        sections.append("# Install dependencies")
        sections.append("pip install -e .")
        sections.append("")
        sections.append("# Run the application")
        sections.append(f"python {spec.entry_point}")
        sections.append("```")
        sections.append("")
        
        # Installation section
        sections.append("## Installation")
        sections.append("")
        sections.append("### Prerequisites")
        sections.append("")
        sections.append("- Python 3.8 or higher")
        sections.append("- pip package manager")
        sections.append("")
        sections.append("### Install from source")
        sections.append("")
        sections.append("```bash")
        sections.append("pip install -e .")
        sections.append("```")
        sections.append("")
        
        # Dependencies
        if spec.dependencies:
            sections.append("### Dependencies")
            sections.append("")
            for dep in spec.dependencies:
                sections.append(f"- `{dep}`")
            sections.append("")
        
        # Usage section
        sections.append("## Usage")
        sections.append("")
        sections.append("### Basic Usage")
        sections.append("")
        sections.append("```python")
        sections.append(f"from {spec.name.replace('-', '_')} import main")
        sections.append("")
        sections.append("# Run the application")
        sections.append("main()")
        sections.append("```")
        sections.append("")
        
        # CLI Usage if CLI framework is used
        if spec.tech_stack.get("cli_framework"):
            sections.append("### Command Line Interface")
            sections.append("")
            sections.append("```bash")
            sections.append(f"# Show help")
            sections.append(f"python -m {spec.name.replace('-', '_')} --help")
            sections.append("")
            sections.append("# Run with options")
            sections.append(f"python -m {spec.name.replace('-', '_')} [OPTIONS]")
            sections.append("```")
            sections.append("")
        
        # Advisory notes
        if advisory and (advisory.recommendations or advisory.warnings):
            sections.append("## Field Usage Notes")
            sections.append("")
            if advisory.recommendations:
                sections.append("### Recommendations")
                sections.append("")
                for rec in advisory.recommendations:
                    sections.append(f"- {rec}")
                sections.append("")
            if advisory.warnings:
                sections.append("### Important Considerations")
                sections.append("")
                for warn in advisory.warnings:
                    sections.append(f"- ⚠️ {warn}")
                sections.append("")
            if advisory.accessibility_score is not None:
                sections.append(f"**Accessibility Score**: {advisory.accessibility_score}/10")
                sections.append("")
        
        # Project Structure
        sections.append("## Project Structure")
        sections.append("")
        sections.append("```")
        sections.append(self._format_folder_structure(spec))
        sections.append("```")
        sections.append("")
        
        # Development section
        sections.append("## Development")
        sections.append("")
        sections.append("### Setup Development Environment")
        sections.append("")
        sections.append("```bash")
        sections.append("# Create virtual environment")
        sections.append("python -m venv venv")
        sections.append("source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        sections.append("")
        sections.append("# Install development dependencies")
        sections.append("pip install -e \".[dev]\"")
        sections.append("```")
        sections.append("")
        sections.append("### Running Tests")
        sections.append("")
        sections.append("```bash")
        sections.append("pytest")
        sections.append("```")
        sections.append("")
        
        # Contributing
        sections.append("## Contributing")
        sections.append("")
        sections.append("Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.")
        sections.append("")
        
        # License
        sections.append("## License")
        sections.append("")
        sections.append("This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.")
        sections.append("")
        
        return "\n".join(sections)
    
    def _generate_usage_guide(
        self, 
        spec: ProjectSpec,
        advisory: Optional[AdvisoryReport] = None
    ) -> str:
        """
        Generate detailed usage guide
        
        Args:
            spec: Project specification
            advisory: Optional advisory report
            
        Returns:
            Usage guide content
        """
        sections = []
        
        sections.append(f"# {self._format_title(spec.name)} Usage Guide")
        sections.append("")
        sections.append("This guide provides detailed instructions for using the application.")
        sections.append("")
        
        # Getting Started
        sections.append("## Getting Started")
        sections.append("")
        sections.append("After installation, you can start using the application immediately.")
        sections.append("")
        
        # Basic Operations
        sections.append("## Basic Operations")
        sections.append("")
        sections.append("### Running the Application")
        sections.append("")
        sections.append("```bash")
        sections.append(f"python {spec.entry_point}")
        sections.append("```")
        sections.append("")
        
        # CLI Commands
        if spec.tech_stack.get("cli_framework"):
            sections.append("## CLI Commands")
            sections.append("")
            sections.append("The application provides a command-line interface with the following commands:")
            sections.append("")
            sections.append("| Command | Description |")
            sections.append("|---------|-------------|")
            sections.append("| `--help` | Show help message |")
            sections.append("| `--version` | Show version |")
            sections.append("")
        
        # Configuration
        sections.append("## Configuration")
        sections.append("")
        sections.append("The application can be configured using environment variables or a configuration file.")
        sections.append("")
        sections.append("### Environment Variables")
        sections.append("")
        sections.append("| Variable | Description | Default |")
        sections.append("|----------|-------------|---------|")
        sections.append(f"| `{spec.name.upper().replace('-', '_')}_DEBUG` | Enable debug mode | `false` |")
        sections.append(f"| `{spec.name.upper().replace('-', '_')}_LOG_LEVEL` | Logging level | `INFO` |")
        sections.append("")
        
        # Troubleshooting
        sections.append("## Troubleshooting")
        sections.append("")
        sections.append("### Common Issues")
        sections.append("")
        sections.append("#### Application won't start")
        sections.append("")
        sections.append("1. Verify Python version: `python --version` (requires 3.8+)")
        sections.append("2. Check all dependencies are installed: `pip list`")
        sections.append("3. Try reinstalling: `pip install -e .`")
        sections.append("")
        
        return "\n".join(sections)
    
    def _generate_api_reference(
        self, 
        spec: ProjectSpec, 
        code_files: Dict[str, str]
    ) -> str:
        """
        Generate API reference documentation
        
        Args:
            spec: Project specification
            code_files: Dict of file paths to code content
            
        Returns:
            API reference content
        """
        sections = []
        
        sections.append(f"# {self._format_title(spec.name)} API Reference")
        sections.append("")
        sections.append("This document provides API documentation for the project modules.")
        sections.append("")
        
        for file_path, code_content in code_files.items():
            if not file_path.endswith('.py'):
                continue
            if '__init__' in file_path or 'test_' in file_path:
                continue
            
            module_name = file_path.replace('.py', '').replace('/', '.')
            sections.append(f"## Module: `{module_name}`")
            sections.append("")
            
            # Extract docstrings and function signatures (simplified)
            functions = self._extract_functions_with_docs(code_content)
            for func_name, doc, signature in functions:
                sections.append(f"### `{func_name}({signature})`")
                sections.append("")
                if doc:
                    sections.append(doc)
                else:
                    sections.append("*No documentation available*")
                sections.append("")
        
        return "\n".join(sections)
    
    def _generate_install_guide(self, spec: ProjectSpec) -> str:
        """
        Generate detailed installation guide
        
        Args:
            spec: Project specification
            
        Returns:
            Installation guide content
        """
        sections = []
        
        sections.append(f"# Installing {self._format_title(spec.name)}")
        sections.append("")
        
        # Prerequisites
        sections.append("## Prerequisites")
        sections.append("")
        sections.append("Before installing, ensure you have:")
        sections.append("")
        sections.append("- Python 3.8 or higher")
        sections.append("- pip package manager")
        sections.append("- (Optional) virtualenv or venv for isolated environments")
        sections.append("")
        
        # Installation Methods
        sections.append("## Installation Methods")
        sections.append("")
        
        # From PyPI (placeholder)
        sections.append("### From PyPI (Recommended)")
        sections.append("")
        sections.append("```bash")
        sections.append(f"pip install {spec.name}")
        sections.append("```")
        sections.append("")
        
        # From Source
        sections.append("### From Source")
        sections.append("")
        sections.append("```bash")
        sections.append("# Clone the repository")
        sections.append(f"git clone https://github.com/yourusername/{spec.name}.git")
        sections.append(f"cd {spec.name}")
        sections.append("")
        sections.append("# Create and activate virtual environment (recommended)")
        sections.append("python -m venv venv")
        sections.append("source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        sections.append("")
        sections.append("# Install in development mode")
        sections.append("pip install -e .")
        sections.append("```")
        sections.append("")
        
        # Dependencies
        if spec.dependencies:
            sections.append("## Dependencies")
            sections.append("")
            sections.append("This project requires the following packages:")
            sections.append("")
            for dep in spec.dependencies:
                sections.append(f"- `{dep}`")
            sections.append("")
            sections.append("These will be installed automatically when you install the package.")
            sections.append("")
        
        # Verification
        sections.append("## Verifying Installation")
        sections.append("")
        sections.append("After installation, verify it works:")
        sections.append("")
        sections.append("```bash")
        sections.append(f"python -c \"import {spec.name.replace('-', '_')}; print('Installation successful!')\"")
        sections.append("```")
        sections.append("")
        
        return "\n".join(sections)
    
    def _generate_contributing_guide(self, spec: ProjectSpec) -> str:
        """
        Generate contributing guide
        
        Args:
            spec: Project specification
            
        Returns:
            Contributing guide content
        """
        return f"""# Contributing to {self._format_title(spec.name)}

Thank you for your interest in contributing! This document provides guidelines
for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Use the issue template
3. Provide detailed reproduction steps

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Commit with descriptive messages
7. Push and create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/{spec.name}.git
cd {spec.name}

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

## Testing

- Write tests for new features
- Maintain existing test coverage
- Run full test suite before submitting PR

## Questions?

Feel free to open an issue for any questions.
"""
    
    def _generate_changelog(self) -> str:
        """Generate changelog template"""
        return """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Core functionality

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - YYYY-MM-DD

### Added
- Initial release
"""
    
    def _format_title(self, name: str) -> str:
        """Convert project name to title case"""
        return name.replace('-', ' ').replace('_', ' ').title()
    
    def _extract_features(self, spec: ProjectSpec) -> List[str]:
        """Extract features from spec"""
        features = []
        
        # From tech stack
        if spec.tech_stack.get("cli_framework"):
            features.append("Command-line interface")
        if spec.tech_stack.get("data_library"):
            features.append("Data processing capabilities")
        if spec.tech_stack.get("web_framework"):
            features.append("Web API support")
        
        # From folder structure (infer from modules)
        for folder, files in spec.folder_structure.items():
            if "parser.py" in files:
                features.append("File parsing")
            if "database.py" in files:
                features.append("Database integration")
            if "api.py" in files:
                features.append("API endpoints")
        
        if not features:
            features.append("Easy to use")
            features.append("Well documented")
        
        return features
    
    def _format_folder_structure(self, spec: ProjectSpec) -> str:
        """Format folder structure as tree"""
        lines = [f"{spec.name}/"]
        
        for folder, files in sorted(spec.folder_structure.items()):
            if folder == "":
                for f in files:
                    lines.append(f"├── {f}")
            else:
                lines.append(f"├── {folder}")
                for i, f in enumerate(files):
                    prefix = "│   └── " if i == len(files) - 1 else "│   ├── "
                    lines.append(f"{prefix}{f}")
        
        return "\n".join(lines)
    
    def _extract_functions_with_docs(
        self, 
        code: str
    ) -> List[tuple]:
        """
        Extract functions with their docstrings
        
        Args:
            code: Python source code
            
        Returns:
            List of (func_name, docstring, signature)
        """
        functions = []
        # Simple pattern to match function definitions
        pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\):'
        matches = re.finditer(pattern, code)
        
        for match in matches:
            func_name = match.group(1)
            signature = match.group(2).strip()
            
            # Skip private functions
            if func_name.startswith('_') and func_name != '__init__':
                continue
            
            # Try to extract docstring (simplified)
            start = match.end()
            doc_match = re.search(r'"""(.*?)"""', code[start:start+500], re.DOTALL)
            docstring = doc_match.group(1).strip() if doc_match else None
            
            functions.append((func_name, docstring, signature))
        
        return functions
