
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
- Generate code files based on spec
- Follow language conventions and best practices
- Add helpful comments and docstrings
- Create configuration files (pyproject.toml, requirements.txt, etc.)

**Current Approach**: Template-based code generation
**Future**: LLM-powered intelligent code generation

**Code Generation Strategy**:
1. Start with project skeleton (setup files, main entry point)
2. Create core modules based on tasks
3. Add error handling and logging
4. Include inline documentation
5. Ensure all imports and dependencies are correct

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

**Safety Check Logic**:
```python
dangerous_keywords = [
    "control", "actuate", "override", "bypass",
    "hack", "exploit", "crack", "inject"
]

if any(keyword in idea.description.lower() for keyword in dangerous_keywords):
    return SafetyCheck(
        approved=False,
        warnings=["Idea contains dangerous operation keyword"],
        required_confirmations=[]
    )
```

---

## Agent Communication Protocol

All agents follow a standard interface:

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
```

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
