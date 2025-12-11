# Agent Roles and Responsibilities

This document describes each agent in the Code Factory pipeline, their inputs, outputs, and responsibilities.

## Overview

The Code Factory uses a multi-agent architecture where each agent has a specific role:

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| SafetyGuard | Validate ideas for safety | `Idea` | `SafetyCheck` |
| PlannerAgent | Create task breakdown | `Idea` | `PlanResult` |
| ArchitectAgent | Design architecture | `Idea` + `Tasks` | `ArchitectResult` |
| ImplementerAgent | Generate code | `ProjectSpec` | `CodeOutput` |
| TesterAgent | Create tests | `ProjectSpec` + code | `TestResult` |
| DocWriterAgent | Write documentation | `ProjectSpec` | `DocOutput` |
| GitOpsAgent | Git operations | `GitOperation` | `GitResult` |
| BlueCollarAdvisor | Review for field use | `Idea` + `ProjectSpec` | `AdvisoryReport` |

---

## Agent Details

### 📋 PlannerAgent

**File**: `src/code_factory/agents/planner.py`

**Purpose**: Transform a high-level idea into actionable tasks with dependencies

**Input**: `Idea`

**Output**: `PlanResult` containing:
- `tasks`: List of `Task` objects with IDs, types, descriptions, dependencies
- `dependency_graph`: Dict mapping task IDs to their dependencies
- `estimated_complexity`: "simple", "moderate", or "complex"
- `warnings`: List of planning warnings

**Algorithm**:
1. Analyze idea description and features
2. Create CONFIG task (setup, dependencies)
3. Create CODE tasks (one per feature, or one default)
4. Create TEST tasks (one per code task)
5. Create DOC tasks (README, examples for 3+ features)
6. Build dependency graph
7. Detect circular dependencies
8. Estimate complexity based on task/feature counts

**Task Types**:
- `CONFIG`: Project setup and configuration
- `CODE`: Implementation code
- `TEST`: Unit and integration tests
- `DOC`: Documentation files

---

### 🏗️ ArchitectAgent

**File**: `src/code_factory/agents/architect.py`

**Purpose**: Design project architecture and technology choices

**Input**: `Idea` or `ArchitectInput(idea, tasks)`

**Output**: `ArchitectResult` containing:
- `spec`: Complete `ProjectSpec`
- `rationale`: Dict explaining decisions
- `blue_collar_score`: 0-10 field usability rating
- `warnings`: Architectural warnings

**Algorithm**:
1. Analyze idea domain (data_processing, calculator, web_service, etc.)
2. Select tech stack based on domain
3. Design folder structure (simple vs complex)
4. Identify dependencies
5. Generate valid project name
6. Calculate blue-collar score
7. Generate warnings for potential issues

**Domain Detection**:
- `data_processing`: CSV, Excel, data, parse, analyze
- `logging_tracking`: log, monitor, track, record
- `calculator`: calculate, math, formula, compute
- `converter`: convert, transform, translate
- `web_service`: web, api, http, server
- `general_utility`: fallback for unrecognized domains

**Blue-Collar Considerations**:
- CLI tools are better than web apps for offline work
- Simple output formats (plain text, CSV) beat complex dashboards
- Must work with limited screen real estate (tablets in engine rooms)
- Consider that users may be wearing gloves or safety gear

**Example ProjectSpec**:
```python
ProjectSpec(
    name="marine-alarm-analyzer",
    tech_stack={
        "language": "python",
        "cli": "typer",
        "parsing": "regex"
    },
    folder_structure={
        "src/": ["main.py", "parser.py", "filters.py"],
        "tests/": ["test_parser.py"],
        "examples/": ["sample_log.txt"]
    },
    dependencies=["typer", "rich"],
    entry_point="src/main.py",
    user_profile="marine_engineer",
    environment="noisy engine room, limited connectivity"
)
```

---

### 💻 ImplementerAgent

**File**: `src/code_factory/agents/implementer.py`

**Purpose**: Generate the actual source code files

**Input**: `ProjectSpec` + `List[Task]`

**Output**: `Dict[str, str]` mapping file paths to file contents

**Key Responsibilities**:
- Create folder structure
- Generate code files based on spec using templates
- Follow language conventions and best practices
- Add helpful comments and docstrings
- Create configuration files (pyproject.toml, .gitignore, etc.)

**Implementation**: Template-based code generation using Jinja2
**Components**:
- `TemplateEngine` - Renders Jinja2 templates with project context
- `CodeWriter` - Safely writes files with transaction support

**Supported Project Types**:
- **CLI Applications** - typer-based command-line tools
- **Python Libraries** - Reusable packages with core classes
- **Data Processing Tools** - pandas-based data processors

**Code Generation Strategy**:
1. Build context from ProjectSpec (name, dependencies, tech stack)
2. Render templates for project type (CLI, library, or both)
3. Generate common files (README, pyproject.toml, .gitignore)
4. Generate domain-specific files (data_processor.py for data tools)
5. Generate test files with appropriate test structure
6. Validate generated files for completeness

**Template Features**:
- Conditional generation based on tech stack
- Feature-based code generation
- Fallback templates when custom templates unavailable
- Unicode and special character support

For detailed information, see [Code Generation Documentation](code_generation.md)

---

### 🧪 TesterAgent

**File**: `src/code_factory/agents/tester.py`

**Purpose**: Create comprehensive tests and run them

**Input**: `ProjectSpec` + Generated code

**Output**: Test files + `TestResults` (pass/fail, coverage)

**Key Responsibilities**:
- Generate unit tests for each module
- Create integration tests for workflows
- Run tests and report results
- Aim for >80% code coverage
- Generate fixtures and test data

**Test Strategy**:
- One test file per source file
- Test happy paths and error cases
- Use descriptive test names
- Keep tests independent and isolated

---

### 📝 DocWriterAgent

**File**: `src/code_factory/agents/doc_writer.py`

**Purpose**: Generate user-facing documentation

**Input**: `ProjectSpec` + Generated code + Test results

**Output**: `README.md`, usage examples, API documentation

**Key Responsibilities**:
- Write clear README with installation and usage
- Create usage examples for common scenarios
- Document CLI commands and options
- Explain project structure
- Add troubleshooting tips

**Documentation Template**:
- Project title and one-line description
- Installation instructions
- Quick start / basic usage
- Examples with sample input/output
- Configuration options
- Common issues and solutions

**Blue-Collar Writing Style**:
- Short sentences
- Active voice
- Real-world examples
- Avoid jargon where possible
- Include "why" not just "how"

---

### 🔧 GitOpsAgent

**File**: `src/code_factory/agents/git_ops.py`

**Purpose**: Handle all Git and GitHub operations safely

**Input**: Repository path, operation type, parameters

**Output**: Operation result + log entry

**Key Responsibilities**:
- Initialize Git repositories
- Create and manage branches
- Commit changes with descriptive messages
- Create remote repositories (via gh CLI or API)
- Push to remote (with confirmations)
- Log all operations to git_activity.log

**Safety Features**:
- Never force-push without explicit confirmation
- Log every operation with timestamp
- Validate repository paths (must be under /Users/dp/Projects)
- Graceful error handling
- Rollback capability for failed operations

**Supported Operations**:
```python
git_ops.init_repo(path)
git_ops.commit(path, message, files=[])
git_ops.create_remote(repo_name, visibility="private")
git_ops.push(path, branch="main", force=False)
git_ops.create_branch(path, branch_name)
```

---

### 👷 BlueCollarAdvisor

**File**: `src/code_factory/agents/blue_collar_advisor.py`

**Purpose**: Ensure generated tools fit real-world technician workflows

**Input**: `ProjectSpec` + `Idea`

**Output**: `AdvisoryReport` with recommendations and warnings

**Key Responsibilities**:
- Review proposed solution against target environment
- Suggest UX improvements for field conditions
- Flag potential usability issues
- Recommend offline-first features
- Check accessibility for users with limited tech experience

**Advisory Checklist**:
- ✅ Works offline or with poor connectivity?
- ✅ Readable in bright sunlight / dim lighting?
- ✅ Usable with gloves or dirty hands?
- ✅ Simple installation (no complex dependencies)?
- ✅ Clear error messages (not cryptic codes)?
- ✅ Fast startup time (<5 seconds)?
- ✅ Saves work frequently (won't lose data)?

**Example Advisories**:
- "Consider using CLI instead of web interface—better for offline use in engine room"
- "Use larger fonts—tool may be used on tablets in bright conditions"
- "Add option to export as CSV—easier to share via email than proprietary formats"
- "Keep commands simple—users may not be familiar with complex CLI syntax"

---

### 🛡️ SafetyGuard

**File**: `src/code_factory/agents/safety_guard.py`

**Purpose**: Enforce safety boundaries and prevent dangerous code generation

**Input**: `Idea`

**Output**: `SafetyCheck(approved: bool, warnings: List[str], required_confirmations: List[str])`

**Key Responsibilities**:
- Scan idea description for dangerous keywords
- Enforce project directory boundaries
- Block unsafe project categories
- Require confirmation for risky operations
- Log all safety decisions

**Blocked Categories**:
- ❌ Equipment control (PLCs, actuators, valves)
- ❌ Safety system bypass (interlocks, alarms)
- ❌ Exploit generation (malware, vulnerability scanners)
- ❌ System modification (OS-level changes)
- ❌ Credential theft or storage

**Requires Confirmation**:
- ⚠️ File deletion operations
- ⚠️ External network calls
- ⚠️ Database modifications
- ⚠️ Email/SMS sending
- ⚠️ Privileged operations

**Approved Categories**:
- ✅ Data analysis and visualization
- ✅ Log parsing and filtering
- ✅ Documentation and checklists
- ✅ Calculation and conversion tools
- ✅ Read-only system monitoring
- ✅ Report generation

**Multi-Layer Validation**:
SafetyGuard uses a sophisticated multi-layer validation approach:

1. **Input Normalization**: Converts text to lowercase, removes accents, normalizes leetspeak (h4ck → hack)
2. **Bypass Detection**: Identifies obfuscation attempts (excessive special chars, unicode tricks, case mixing)
3. **Pattern Matching**: Regex-based detection of dangerous operation patterns
4. **Confirmation Patterns**: Identifies operations requiring human confirmation
5. **Semantic Analysis**: Analyzes environment and user roles for additional warnings

**Confidence Scoring**:
Each safety check includes a confidence score (0.0-1.0) that decreases when:
- Bypass attempts are detected (-0.2 per attempt)
- Semantic warnings are triggered (-0.1 per warning)

**Example SafetyCheck Output**:
```python
SafetyCheck(
    approved=False,
    warnings=["Idea violates safety guidelines - see docs/safety.md",
              "Dangerous operation detected: 'hack'"],
    required_confirmations=[],
    blocked_keywords=["hack"],
    metadata=SafetyCheckMetadata(
        normalized_input="hack into the system",
        patterns_matched=["hack(?:ing)?"],
        bypass_attempts_detected=["case_mixing"],
        confidence_score=0.8
    )
)
```

---

## Agent Communication Protocol

All agents follow a standard interface defined in `src/code_factory/core/agent_runtime.py`:

```python
from abc import ABC, abstractmethod
from code_factory.core.models import BaseModel

class BaseAgent(ABC):
    """Base class for all factory agents"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Agent identifier"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """What this agent does"""
        pass
    
    @abstractmethod
    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Execute agent logic
        
        Args:
            input_data: Validated input conforming to agent's expected schema
            
        Returns:
            Validated output conforming to agent's output schema
            
        Raises:
            AgentExecutionError: If execution fails
        """
        pass
    
    def validate_input(self, input_data: Any, expected_type: Type[BaseModel]) -> BaseModel:
        """
        Helper method to validate input against expected schema.
        Accepts either the expected type or a dict that can be converted.
        
        Args:
            input_data: Data to validate
            expected_type: Expected Pydantic model type
            
        Returns:
            Validated input as expected_type
            
        Raises:
            ValueError: If validation fails
        """
        pass
```

### The `execute()` Method Pattern

The `execute()` method is the core of each agent. Key principles:

1. **Single Input, Single Output**: Each call takes one input model, returns one output model
2. **Stateless**: Agents don't maintain state between calls
3. **Pydantic Models**: All inputs/outputs are Pydantic BaseModel subclasses for validation
4. **Idempotent**: Same input should produce same output (given same external state)

**Input Validation Pattern**:
```python
def execute(self, input_data: BaseModel) -> BaseModel:
    # Validate and convert input using helper method
    idea = self.validate_input(input_data, Idea)
    
    # Agent logic here...
    
    return OutputModel(...)
```

This allows agents to accept either:
- Direct Pydantic model instances: `agent.execute(Idea(description="..."))`
- Dictionaries: `agent.execute({"description": "..."})`

## Error Handling

Every agent must handle errors gracefully:

1. **Input Validation**: Use Pydantic models to catch bad inputs early
2. **Execution Errors**: Wrap operations in try/except, return structured errors
3. **Partial Success**: If an agent completes some work before failing, save progress
4. **Logging**: Log all significant events for debugging

Example error handling:
```python
def execute(self, input_data: ProjectSpec) -> CodeGenerationResult:
    try:
        # Validate input
        if not input_data.tech_stack:
            raise ValueError("tech_stack is required")
        
        # Execute logic
        generated_files = self._generate_code(input_data)
        
        return CodeGenerationResult(
            files=generated_files,
            status="success"
        )
    except Exception as e:
        logger.error(f"Code generation failed: {e}")
        return CodeGenerationResult(
            files={},
            status="failed",
            error=str(e)
        )
```

## Testing Agents

Each agent should have its own test file in `tests/unit/agents/`:

```python
# tests/unit/agents/test_planner.py
def test_planner_basic_idea():
    idea = Idea(description="Build a log parser CLI")
    agent = PlannerAgent()
    result = agent.execute(idea)
    
    assert len(result.tasks) > 0
    assert result.tasks[0].type in ["config", "code", "test", "doc"]
```

## Future Enhancements

1. **Parallel Execution**: Run independent agents simultaneously
2. **Agent Plugins**: Load custom agents from external modules
3. **Human-in-the-Loop**: Pause for human review between stages
4. **Iterative Refinement**: Allow agents to revise based on feedback
5. **Learning**: Track which patterns work best and adjust agent behavior

---

*For the orchestration flow, see [architecture.md](architecture.md)*  
*For CLI usage, see [cli_usage.md](cli_usage.md)*  
*For safety guidelines, see [safety.md](safety.md)*
