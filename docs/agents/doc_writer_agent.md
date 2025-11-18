# DocWriterAgent - Comprehensive Documentation Generation

## Overview

The DocWriterAgent is a specialized agent that generates professional, comprehensive documentation for generated projects. It creates README files, contributing guidelines, licenses, usage guides, architecture documentation, and API references. All documentation is tailored for blue-collar users with clear, practical language focused on real-world usage.

**Position in Pipeline**: Wave 2 - Code Generation (follows TesterAgent)

**Key Responsibilities**:
- Generate README.md with project overview and quick start
- Create CONTRIBUTING.md with contribution guidelines
- Generate MIT LICENSE file
- Create docs/usage.md with detailed usage instructions
- Generate docs/architecture.md with design decisions
- Create docs/api.md from code analysis (AST-based)
- Generate .gitignore with appropriate exclusions
- Ensure blue-collar focus in all documentation

---

## API Reference

### Input Model

```python
class DocInput(BaseModel):
    spec: ProjectSpec = Field(..., description="Project specification")
    idea: Optional[Idea] = Field(None, description="Original idea for context")
    code_files: Optional[Dict[str, str]] = Field(None, description="Code files for API docs")
```

**Field Descriptions**:
- `spec`: ProjectSpec containing project metadata, tech stack, and structure
- `idea`: Original Idea object for context (target users, environment, features)
- `code_files`: Optional dictionary of code files for generating API documentation

**Note**: The agent also accepts `ProjectSpec` directly for backward compatibility.

### Output Model

```python
class DocOutput(BaseModel):
    files: Dict[str, str]  # file_path -> content
```

**Field Descriptions**:
- `files`: Dictionary mapping file paths to generated documentation content
  - Always includes: README.md, CONTRIBUTING.md, LICENSE, .gitignore
  - Always includes: docs/usage.md, docs/architecture.md
  - Conditionally includes: docs/api.md (if code_files provided)

### Execute Method

```python
def execute(self, input_data: BaseModel) -> BaseModel:
    """
    Generate comprehensive project documentation

    This method:
    1. Analyzes ProjectSpec to understand project structure
    2. Generates README with features, installation, usage
    3. Creates contribution guidelines (CONTRIBUTING.md)
    4. Generates MIT LICENSE
    5. Creates detailed usage guide
    6. Generates architecture documentation
    7. Optionally creates API docs from code analysis
    8. Generates appropriate .gitignore

    Args:
        input_data: DocInput with ProjectSpec and optional code/idea

    Returns:
        DocOutput: Dictionary of generated documentation files

    Raises:
        ValueError: If input validation fails
    """
```

---

## Usage Examples

### Basic Example

```python
from code_factory.agents.doc_writer import DocWriterAgent, DocInput
from code_factory.core.models import ProjectSpec

# Create agent instance
doc_writer = DocWriterAgent()

# Prepare project spec
spec = ProjectSpec(
    name="csv-parser",
    description="Simple and reliable CSV parser for field data",
    tech_stack={"language": "python", "version": "3.11"},
    folder_structure={"src/": ["parser.py", "utils.py"]},
    dependencies=["pandas", "typer"],
    entry_point="src/main.py"
)

# Create input
doc_input = DocInput(spec=spec)

# Execute agent
result = doc_writer.execute(doc_input)

# Access generated files
print(f"Generated {len(result.files)} documentation files:")
for filepath in result.files.keys():
    print(f"  - {filepath}")

# Write files to disk
for filepath, content in result.files.items():
    with open(filepath, 'w') as f:
        f.write(content)
```

**Expected Output**:
```
Generated 7 documentation files:
  - README.md
  - CONTRIBUTING.md
  - LICENSE
  - docs/usage.md
  - docs/architecture.md
  - .gitignore
```

### Real-World Example: Marine Equipment Logger with API Docs

```python
from code_factory.agents.doc_writer import DocWriterAgent, DocInput
from code_factory.core.models import Idea, ProjectSpec

# Original idea for context
idea = Idea(
    description="Equipment alarm log analyzer for ship engineers",
    target_users=["marine engineer", "ship mechanic"],
    environment="noisy engine room, limited WiFi, harsh conditions",
    features=[
        "Parse CSV equipment logs",
        "Filter by severity (critical, warning, info)",
        "Generate daily summary reports",
        "Export filtered results"
    ],
    constraints=["Must work offline", "Simple CLI interface"]
)

# Project specification
spec = ProjectSpec(
    name="marine-log-analyzer",
    description="Equipment alarm log analyzer for ship engineers",
    tech_stack={"language": "python", "cli": "typer"},
    folder_structure={
        "src/marine_logger/": ["parser.py", "filters.py", "reporter.py", "main.py"]
    },
    dependencies=["pandas", "typer", "rich"],
    entry_point="src/marine_logger/main.py",
    user_profile="marine_engineer",
    environment="noisy engine room, limited WiFi"
)

# Code for API documentation
code_files = {
    "src/marine_logger/parser.py": '''
"""Log parser for marine equipment alarms"""

class LogParser:
    """Parse marine equipment alarm logs from CSV files"""

    def parse_log_file(self, filepath: str) -> list:
        """
        Parse CSV log file

        Args:
            filepath: Path to CSV log file

        Returns:
            List of log entries as dictionaries
        """
        pass
''',
    "src/marine_logger/filters.py": '''
"""Filter utilities for log analysis"""

def filter_by_severity(logs: list, severity: str) -> list:
    """
    Filter logs by severity level

    Args:
        logs: List of log entries
        severity: Severity level (critical, warning, info)

    Returns:
        Filtered list of logs
    """
    pass
'''
}

# Create input with all context
doc_input = DocInput(
    spec=spec,
    idea=idea,
    code_files=code_files
)

# Generate documentation
doc_writer = DocWriterAgent()
result = doc_writer.execute(doc_input)

# Save all files
import os
for filepath, content in result.files.items():
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

print("Documentation generated:")
print(f"  {len(result.files)} files created")
print(f"  README includes target users: {idea.target_users}")
print(f"  Environment notes: {idea.environment}")
print(f"  API docs: {'Yes' if 'docs/api.md' in result.files else 'No'}")
```

**Expected Output**:
```
Documentation generated:
  8 files created
  README includes target users: ['marine engineer', 'ship mechanic']
  Environment notes: noisy engine room, limited WiFi
  API docs: Yes
```

### Backward Compatible Usage (ProjectSpec only)

```python
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.core.models import ProjectSpec

doc_writer = DocWriterAgent()

spec = ProjectSpec(
    name="simple-tool",
    description="A simple utility",
    tech_stack={"language": "python"},
    folder_structure={"src/": ["main.py"]},
    dependencies=[],
    entry_point="src/main.py"
)

# Accepts ProjectSpec directly
result = doc_writer.execute(spec)

# Works the same
print(result.files.keys())
```

---

## Implementation Details

### Algorithm

1. **Input Processing**
   - Accept either ProjectSpec or DocInput
   - Extract spec, idea, and code_files
   - Determine language and tech stack

2. **README Generation**
   - Extract project metadata
   - Build features list from idea.features
   - Generate installation instructions (pip/uv)
   - Create usage examples
   - Add troubleshooting section
   - Include blue-collar focus notes

3. **CONTRIBUTING.md Generation**
   - Language-specific setup instructions
   - Git workflow guidelines
   - Code style requirements
   - Testing requirements
   - Code of conduct

4. **LICENSE Generation**
   - MIT license template
   - Current year
   - Project name as copyright holder

5. **Usage Guide Generation**
   - Quick start section
   - Detailed operations
   - Command reference
   - Configuration options
   - Examples with real scenarios
   - Field usage notes

6. **Architecture Documentation**
   - Project structure visualization
   - Tech stack explanation
   - Design principles
   - Blue-collar considerations
   - Data flow diagrams

7. **API Documentation (if code provided)**
   - Parse code with AST
   - Extract functions and classes
   - Document parameters and docstrings
   - Generate API reference

8. **.gitignore Generation**
   - Language-specific patterns
   - IDE files
   - Build artifacts
   - Virtual environments

### Design Decisions

**Why comprehensive documentation?**
- Blue-collar users need clear, detailed guides
- Reduces support burden
- Enables self-service troubleshooting
- Professional appearance builds trust

**Why blue-collar focus?**
- Target users are field workers, not developers
- Plain language > technical jargon
- Practical examples > theoretical explanations
- Offline-first mindset

**Why AST-based API docs?**
- Automatically extracts function signatures
- Includes docstrings
- No manual maintenance required
- Accurate and up-to-date

### Generated File Structure

```
project/
├── README.md                 # Project overview
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
├── .gitignore               # Git exclusions
└── docs/
    ├── usage.md             # Detailed usage guide
    ├── architecture.md      # Design documentation
    └── api.md               # API reference (if code provided)
```

### Blue-Collar Documentation Features

- **Clear language**: No jargon, plain explanations
- **Practical examples**: Real-world scenarios
- **Troubleshooting**: Common issues and solutions
- **Offline support**: Notes about offline capabilities
- **Environment context**: Field conditions acknowledged
- **Visual structure**: Easy-to-scan formatting
- **Quick start**: Get running fast
- **Contact info**: Where to get help

---

## Documentation Quality Standards

### README.md
- ✓ Clear project title and description
- ✓ Target audience identification
- ✓ Installation instructions (multiple methods)
- ✓ Quick start example
- ✓ Features list
- ✓ Documentation links
- ✓ Troubleshooting section
- ✓ License information

### CONTRIBUTING.md
- ✓ Prerequisites listed
- ✓ Development setup steps
- ✓ Contribution workflow
- ✓ Code style guidelines
- ✓ Testing requirements
- ✓ Review process
- ✓ Code of conduct

### docs/usage.md
- ✓ Quick start guide
- ✓ Detailed operations
- ✓ Command reference
- ✓ Configuration options
- ✓ Multiple examples
- ✓ Error handling
- ✓ Best practices
- ✓ Field usage notes

### docs/architecture.md
- ✓ System overview
- ✓ Design principles
- ✓ Project structure
- ✓ Tech stack explanation
- ✓ Component descriptions
- ✓ Data flow
- ✓ Blue-collar considerations

---

## Testing

### Unit Tests

**Location**: `tests/unit/test_agents.py` (includes DocWriterAgent tests)

**Key Test Cases**:
- Test README generation with various specs
- Test CONTRIBUTING generation
- Test LICENSE generation
- Test usage guide generation
- Test architecture doc generation
- Test API doc generation from code
- Test .gitignore generation
- Test blue-collar focus elements

### Integration Tests

**Location**: `tests/integration/test_wave1_pipeline.py`

**Tests**:
- Test DocWriterAgent in full pipeline
- Test with marine logger example
- Test with idea context
- Test with code files for API docs

---

## Performance

**Typical Execution Time**: <1 second for most projects

**Memory Usage**: ~10MB for typical documentation generation

**Scalability**:
- Handles projects of any size
- AST parsing scales linearly with code size
- Documentation generation is O(n) where n = number of files

---

## Known Limitations

- **Python-focused**: Best documentation for Python projects
- **Generic templates**: Some sections use TODO placeholders
- **API docs require code**: Cannot generate API docs without code files
- **Basic examples**: Usage examples are templates requiring customization
- **No diagram generation**: Architecture diagrams are textual, not visual

---

## Future Enhancements

- Add support for more languages (JavaScript, Go, Rust)
- Generate actual usage examples from tests
- Create visual architecture diagrams
- Add tutorial generation
- Support for video documentation links
- Multi-language documentation
- Automated changelog from git history
- Badge generation (coverage, build status)

---

## Related Documentation

- [TesterAgent](tester_agent.md) - Tests code before documentation
- [ImplementerAgent](implementer_agent.md) - Generates code to document
- [GitOpsAgent](git_ops_agent.md) - Manages documentation in version control
- [Agent Integration Guide](../agent_integration.md) - How agents work together
- [Architecture](../architecture.md) - Overall system design

---

## Example Generated README

Here's a sample of what DocWriterAgent generates:

```markdown
# marine-log-analyzer

> Equipment alarm log analyzer for ship engineers

## Who Is This For?

This tool is designed for **marine engineer, ship mechanic** who need
a practical, reliable solution that works in real-world environments.

## Environment

**Designed for:** noisy engine room, limited WiFi, harsh conditions

This tool is built with field conditions in mind - works offline,
handles errors gracefully, and provides clear feedback.

## Features

- Parse CSV equipment logs
- Filter by severity (critical, warning, info)
- Generate daily summary reports
- Export filtered results

## Installation

### Option 1: Using pip
...
```

---

## Changelog

### v0.2.0 - 2025-11-18
- Implemented comprehensive documentation generation
- Added AST-based API documentation
- Added blue-collar focus throughout
- Added CONTRIBUTING.md generation
- Added architecture documentation
- Added field usage notes
- Added support for Idea context

### v0.1.0 - Initial
- Basic README generation scaffold

---

*Last Updated: 2025-11-18*
*Maintained by: Testing & Documentation Engineer (Wave 2)*
