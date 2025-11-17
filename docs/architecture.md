# Architecture Overview

## System Design Philosophy

The Agent-Orchestrated Code Factory follows a **hub-and-spoke model** where a central Orchestrator coordinates multiple specialized agents. Each agent has a single responsibility and communicates through well-defined data models.

## High-Level Flow

```
Human Idea (text/file)
        ↓
   Orchestrator
        ↓
    ┌───┴───┬───────┬──────────┬─────────┬────────────┐
    ↓       ↓       ↓          ↓         ↓            ↓
  Planner Architect Implementer Tester DocWriter GitOps
    ↓       ↓       ↓          ↓         ↓            ↓
    └───┬───┴───────┴──────────┴─────────┴────────────┘
        ↓
   Complete Project Repository
        ↓
   GitHub (optional)
```

## Core Components

### 1. Orchestrator (`core/orchestrator.py`)

**Responsibility**: Coordinate the entire build pipeline

**Key Methods**:
- `run_factory(idea: Idea) -> ProjectResult`
- `checkpoint(stage: str)` - Git commit at each stage
- `handle_failure(agent: str, error: Exception)` - Graceful degradation

**Flow**:
1. Accept Idea input
2. Call SafetyGuard to validate
3. Call PlannerAgent to create task graph
4. Call ArchitectAgent for ProjectSpec
5. Create project directory structure
6. Call ImplementerAgent to generate code
7. Call TesterAgent to create and run tests
8. Call DocWriterAgent for documentation
9. Call GitOps to initialize repo and push (optional)
10. Return ProjectResult with paths and status

### 2. Agent Runtime (`core/agent_runtime.py`)

**Responsibility**: Execute individual agents with isolation and error handling

**Key Features**:
- Agent registration and discovery
- Input validation (Pydantic models)
- Output capture and logging
- Timeout protection
- Resource limits (memory, CPU)

**Agent Interface** (all agents must implement):
```python
class BaseAgent(ABC):
    @abstractmethod
    def execute(self, input_data: BaseModel) -> BaseModel:
        """Execute agent logic and return structured output"""
        pass
```

### 3. Data Models (`core/models.py`)

**Core Types**:

```python
class Idea(BaseModel):
    """Human input - what to build"""
    description: str
    target_users: List[str]  # e.g., ["marine engineer", "mechanic"]
    environment: str          # e.g., "noisy engine room, limited WiFi"
    features: List[str]       # Optional specific features

class ProjectSpec(BaseModel):
    """Architecture decisions"""
    name: str
    tech_stack: Dict[str, str]  # {"language": "python", "framework": "flask"}
    folder_structure: Dict[str, List[str]]
    dependencies: List[str]
    entry_point: str
    
class Task(BaseModel):
    """Single unit of work"""
    id: str
    type: str  # "code", "test", "doc", "config"
    dependencies: List[str]  # Task IDs that must complete first
    description: str
    files_to_create: List[str]
    
class AgentRun(BaseModel):
    """Execution record"""
    agent_name: str
    input_data: BaseModel
    output_data: Optional[BaseModel]
    status: str  # "pending", "running", "success", "failed"
    started_at: datetime
    completed_at: Optional[datetime]
    error: Optional[str]
```

## Agent Descriptions

### PlannerAgent (`agents/planner.py`)
- **Input**: Idea
- **Output**: List[Task] (task dependency graph)
- **Logic**: Break down idea into concrete implementation tasks
- **Example**: "Log analyzer" → [setup_project, parse_logs, filter_alarms, format_output, write_tests]

### ArchitectAgent (`agents/architect.py`)
- **Input**: Idea + List[Task]
- **Output**: ProjectSpec
- **Logic**: Choose tech stack, design folder structure, identify dependencies
- **Heuristics**: CLI tools → typer, Data processing → pandas, etc.

### ImplementerAgent (`agents/implementer.py`)
- **Input**: ProjectSpec + List[Task]
- **Output**: Dict[str, str] (file_path → content)
- **Logic**: Generate code files based on spec and tasks
- **Future**: LLM integration for actual code generation

### TesterAgent (`agents/tester.py`)
- **Input**: ProjectSpec + Generated code
- **Output**: Test files + test results
- **Logic**: Create pytest tests, run them, report results

### DocWriterAgent (`agents/doc_writer.py`)
- **Input**: ProjectSpec + Generated code
- **Output**: README.md, usage examples, API docs
- **Logic**: Extract purpose, write installation steps, create examples

### GitOpsAgent (`agents/git_ops.py`)
- **Input**: Project path, commit message
- **Output**: Git operation results
- **Logic**: Safe Git operations (init, add, commit, remote, push)
- **Safety**: Logs all operations, requires confirmation for destructive actions

### BlueCollarAdvisor (`agents/blue_collar_advisor.py`)
- **Input**: ProjectSpec
- **Output**: Recommendations and warnings
- **Logic**: Check if solution fits target user environment
- **Examples**: 
  - "CLI is better than web app for offline use"
  - "Avoid small fonts—readability in bright sunlight"
  - "Keep output simple—users may be wearing gloves"

### SafetyGuard (`agents/safety_guard.py`)
- **Input**: Idea
- **Output**: SafetyCheck (approved: bool, warnings: List[str])
- **Logic**: Block or flag dangerous project types
- **Blocked**: Equipment control, exploit code, system modification
- **Requires confirmation**: Data deletion, external API calls, file system access

## Data Flow Example

**Idea**: "Build a tool to analyze marine engine alarm logs and highlight critical issues"

**Step 1 - SafetyGuard**:
```python
SafetyCheck(approved=True, warnings=["Read-only analysis tool - good!"])
```

**Step 2 - PlannerAgent**:
```python
[
    Task(id="t1", type="config", description="Setup Python project with CLI"),
    Task(id="t2", type="code", description="Parse alarm log file format", dependencies=["t1"]),
    Task(id="t3", type="code", description="Filter for critical alarms", dependencies=["t2"]),
    Task(id="t4", type="code", description="Format output with color coding", dependencies=["t3"]),
    Task(id="t5", type="test", description="Test parsing and filtering", dependencies=["t2", "t3"]),
    Task(id="t6", type="doc", description="Write usage guide", dependencies=["t4"])
]
```

**Step 3 - ArchitectAgent**:
```python
ProjectSpec(
    name="marine-alarm-analyzer",
    tech_stack={"language": "python", "cli": "typer", "parsing": "re"},
    folder_structure={"src/": ["main.py", "parser.py", "filter.py"]},
    dependencies=["typer", "rich"],
    entry_point="src/main.py"
)
```

**Step 4-7**: Implementer writes code, Tester creates tests, DocWriter generates README

**Step 8 - GitOps**:
```
git init
git add .
git commit -m "Initial commit: Marine alarm analyzer"
git remote add origin git@github.com:user/marine-alarm-analyzer.git
git push -u origin main
```

## Technology Choices

- **Python 3.11+**: Accessibility, rich ecosystem, good for automation
- **Typer**: Modern CLI framework, better UX than argparse
- **Pydantic**: Data validation and serialization
- **GitPython**: Safe Git operations from Python
- **Rich**: Beautiful terminal output
- **pytest**: Industry-standard testing

## Extension Points

1. **Custom Agents**: Drop new agent files in `agents/`, implement BaseAgent interface
2. **Templates**: Add project templates in `docs/templates/`
3. **LLM Integration**: Add LLM provider in future phase for actual code generation
4. **Plugins**: Future support for custom domain-specific logic

## Security & Safety

- **File system isolation**: Only write to `/Users/dp/Projects/`
- **No sudo**: No system-level operations
- **Git logging**: Every Git operation logged to `git_activity.log`
- **Human confirmation**: Required for destructive Git operations
- **Input validation**: All inputs validated via Pydantic

## Performance Considerations

- **Agent isolation**: Each agent runs independently, can be parallelized later
- **Checkpoint commits**: Git commits after each major stage for rollback
- **Resource limits**: Future implementation of timeout and memory limits per agent

---

*For implementation details of each agent, see [agent_roles.md](agent_roles.md)*
