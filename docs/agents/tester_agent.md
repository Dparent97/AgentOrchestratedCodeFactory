# TesterAgent - Automated Test Generation and Execution

## Overview

The TesterAgent is a specialized agent that analyzes generated code and automatically creates comprehensive pytest test suites. It parses Python source code using AST (Abstract Syntax Tree) analysis to identify testable components, generates unit tests for functions and classes, and executes the tests to provide coverage reports.

**Position in Pipeline**: Wave 2 - Code Generation (follows ImplementerAgent)

**Key Responsibilities**:
- Parse Python source code to extract testable components
- Generate pytest test files with unit tests for functions and classes
- Execute generated tests in isolated environments
- Report test results, pass/fail statistics, and coverage metrics
- Ensure code quality meets project standards (>80% coverage)

---

## API Reference

### Input Model

```python
class TestInput(BaseModel):
    spec: ProjectSpec = Field(..., description="Project specification")
    code_files: Dict[str, str] = Field(..., description="Mapping of file paths to code content")
```

**Field Descriptions**:
- `spec`: ProjectSpec containing project metadata (name, tech stack, dependencies)
- `code_files`: Dictionary mapping file paths (e.g., "src/parser.py") to their source code content

### Output Model

```python
class TestResult(BaseModel):
    total_tests: int = Field(default=0, ge=0)
    passed: int = Field(default=0, ge=0)
    failed: int = Field(default=0, ge=0)
    skipped: int = Field(default=0, ge=0)
    coverage_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    error_messages: List[str] = Field(default_factory=list)
    success: bool = Field(default=False)
```

**Field Descriptions**:
- `total_tests`: Total number of tests generated and executed
- `passed`: Number of tests that passed
- `failed`: Number of tests that failed
- `skipped`: Number of tests that were skipped
- `coverage_percent`: Estimated code coverage percentage (0-100)
- `error_messages`: List of error messages if tests failed
- `success`: Boolean indicating overall test success (True if no failures)

### Execute Method

```python
def execute(self, input_data: BaseModel) -> BaseModel:
    """
    Generate and execute tests for provided code

    This method:
    1. Analyzes code files using AST parsing
    2. Generates pytest test files for each source file
    3. Executes tests in a temporary isolated environment
    4. Parses pytest output to extract statistics
    5. Returns comprehensive test results

    Args:
        input_data: TestInput containing ProjectSpec and code files

    Returns:
        TestResult: Execution results with pass/fail stats and coverage

    Raises:
        ValueError: If input validation fails
        SyntaxError: If code cannot be parsed (handled gracefully)
    """
```

---

## Usage Examples

### Basic Example

```python
from code_factory.agents.tester import TesterAgent, TestInput
from code_factory.core.models import ProjectSpec

# Create agent instance
tester = TesterAgent()

# Prepare project spec
spec = ProjectSpec(
    name="csv-parser",
    description="Simple CSV parser utility",
    tech_stack={"language": "python", "version": "3.11"},
    folder_structure={"src/": ["parser.py"]},
    dependencies=["pandas"],
    entry_point="src/parser.py"
)

# Code to test
code_files = {
    "src/parser.py": '''
def read_csv(filepath):
    """Read CSV file and return contents"""
    with open(filepath, 'r') as f:
        return f.read()

def parse_csv(content):
    """Parse CSV content into list of rows"""
    lines = content.strip().split('\\n')
    return [line.split(',') for line in lines]
'''
}

# Create input
test_input = TestInput(spec=spec, code_files=code_files)

# Execute agent
result = tester.execute(test_input)

# Use result
print(f"Tests run: {result.total_tests}")
print(f"Passed: {result.passed}")
print(f"Failed: {result.failed}")
print(f"Coverage: {result.coverage_percent:.1f}%")
print(f"Success: {result.success}")
```

**Expected Output**:
```
Tests run: 4
Passed: 4
Failed: 0
Coverage: 80.0%
Success: True
```

### Real-World Example: Marine Equipment Logger

```python
from code_factory.agents.tester import TesterAgent, TestInput
from code_factory.core.models import ProjectSpec

# Marine equipment log analyzer project
spec = ProjectSpec(
    name="marine-log-analyzer",
    description="Equipment alarm log analyzer for ship engineers",
    tech_stack={"language": "python", "cli": "typer"},
    folder_structure={
        "src/marine_logger/": ["parser.py", "filters.py", "reporter.py"]
    },
    dependencies=["pandas", "typer"],
    entry_point="src/marine_logger/main.py"
)

# Sample code for equipment log parser
code_files = {
    "src/marine_logger/parser.py": '''
import csv
from datetime import datetime

class LogParser:
    """Parse marine equipment alarm logs"""

    def parse_log_file(self, filepath):
        """Parse CSV log file"""
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def filter_by_severity(self, logs, severity):
        """Filter logs by severity level"""
        return [log for log in logs if log['severity'] == severity]

    def filter_by_date_range(self, logs, start_date, end_date):
        """Filter logs within date range"""
        filtered = []
        for log in logs:
            log_date = datetime.fromisoformat(log['timestamp'])
            if start_date <= log_date <= end_date:
                filtered.append(log)
        return filtered
''',
    "src/marine_logger/reporter.py": '''
def generate_summary(logs):
    """Generate summary statistics from logs"""
    total = len(logs)
    critical = sum(1 for log in logs if log['severity'] == 'critical')
    warning = sum(1 for log in logs if log['severity'] == 'warning')
    return {
        'total': total,
        'critical': critical,
        'warning': warning
    }
'''
}

# Create test input
test_input = TestInput(spec=spec, code_files=code_files)

# Execute tester
tester = TesterAgent()
result = tester.execute(test_input)

print(f"Marine Logger Test Results:")
print(f"  Total tests: {result.total_tests}")
print(f"  Passed: {result.passed}/{result.total_tests}")
print(f"  Coverage: {result.coverage_percent:.1f}%")
print(f"  Status: {'✓ All tests passed' if result.success else '✗ Some tests failed'}")
```

**Expected Output**:
```
Marine Logger Test Results:
  Total tests: 8
  Passed: 8/8
  Coverage: 85.0%
  Status: ✓ All tests passed
```

---

## Implementation Details

### Algorithm

1. **Code Analysis**
   - Iterate through all provided code files
   - Skip non-Python files and test files
   - Parse each Python file using `ast.parse()`
   - Extract public functions and classes (non-underscore prefixed)

2. **Test Generation**
   - For each function: Generate existence test and parameter tests
   - For each class: Generate instantiation test and method tests
   - Create import statements with proper module paths
   - Generate test class structure following pytest conventions

3. **Test Execution**
   - Create temporary directory for isolated execution
   - Write source files to proper structure
   - Write generated test files to `tests/` directory
   - Execute pytest with coverage collection
   - Parse output to extract statistics

4. **Result Reporting**
   - Parse pytest output for pass/fail/skip counts
   - Calculate coverage percentage (estimated from test success)
   - Compile error messages if any failures
   - Return TestResult with comprehensive statistics

### Design Decisions

**Why AST-based analysis?**
- More reliable than regex pattern matching
- Understands Python syntax correctly
- Extracts docstrings and type information
- Handles complex code structures

**Why temporary directory execution?**
- Isolates test execution from main environment
- Prevents file system pollution
- Allows proper module import testing
- Clean up is automatic

**Why pytest?**
- Industry standard for Python testing
- Excellent output formatting
- Comprehensive plugin ecosystem
- Great integration with coverage tools

### Generated Test Structure

```python
"""
Tests for src/example.py

Auto-generated by TesterAgent
"""

import pytest
from module.path import (
    function_name,
    ClassName,
)


class TestExample:
    """Test suite for src/example.py"""

    def test_function_name_exists(self):
        """Test that function_name is callable"""
        assert callable(function_name)

    def test_ClassName_instantiation(self):
        """Test that ClassName can be instantiated"""
        # TODO: Provide appropriate constructor arguments
        pass
```

### Blue-Collar Considerations

- **Clear error messages**: Test failures include helpful context
- **No complex setup**: Tests work out-of-the-box with pytest installed
- **Readable test names**: Self-documenting test method names
- **TODO markers**: Placeholder tests marked for manual completion
- **Isolated execution**: Tests don't interfere with main project

---

## Testing

### Unit Tests

**Location**: `tests/unit/test_agents.py` (includes TesterAgent tests)

**Coverage**: Part of overall agent test suite

**Key Test Cases**:
- Test AST parsing of valid Python code
- Test test file generation for functions
- Test test file generation for classes
- Test handling of syntax errors in source code
- Test pytest execution and result parsing
- Test coverage calculation
- Test error handling when pytest unavailable

### Integration Tests

**Location**: `tests/integration/test_wave1_pipeline.py`

**Tests**:
- Test TesterAgent in full pipeline (after ImplementerAgent)
- Test with realistic code generation scenarios
- Test with marine equipment logger example
- Test with various project structures

---

## Performance

**Typical Execution Time**: 5-15 seconds for small projects

**Memory Usage**: ~50MB for typical code analysis + test execution

**Scalability**:
- Handles projects with 10-20 source files efficiently
- Test generation is O(n) where n = number of functions/classes
- Execution time depends on generated test count

---

## Known Limitations

- **Basic test generation**: Generated tests are templates requiring manual completion
- **No integration tests**: Only generates unit tests, not integration scenarios
- **Coverage estimation**: Coverage is estimated, not measured with pytest-cov
- **Python only**: Only supports Python code analysis
- **No async support**: Async functions get basic tests but may need manual work
- **pytest required**: Gracefully handles absence but cannot execute tests

---

## Future Enhancements

- Add pytest-cov integration for real coverage measurement
- Generate more sophisticated test cases based on function signatures
- Add integration test generation
- Support for async/await functions
- Property-based testing with Hypothesis
- Mocking support for external dependencies
- Test data generation from type hints

---

## Related Documentation

- [ImplementerAgent](implementer_agent.md) - Generates code that TesterAgent tests
- [DocWriterAgent](doc_writer_agent.md) - Documents tested code
- [Agent Integration Guide](../agent_integration.md) - How agents work together
- [Architecture](../architecture.md) - Overall system design

---

## Changelog

### v0.2.0 - 2025-11-18
- Implemented real pytest generation using AST analysis
- Added test execution in isolated environment
- Added coverage estimation
- Added comprehensive error handling
- Added support for functions and classes

### v0.1.0 - Initial
- Basic scaffold with placeholder implementation

---

*Last Updated: 2025-11-18*
*Maintained by: Testing & Documentation Engineer (Wave 2)*
