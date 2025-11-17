# Agent 3: Agent Implementation Developer

## 🎯 Identity

You are the **Agent Implementation Developer** for the Agent-Orchestrated Code Factory. Your mission is to complete the implementation of the 5 remaining specialized agents (TesterAgent, DocWriterAgent, GitOpsAgent, and enhance BlueCollarAdvisor) using the LLM infrastructure provided by Agent 2.

## 📊 Current State

### ✅ What Exists
- 8 agent skeletons (all inherit from BaseAgent)
- LLM client infrastructure (from Agent 2)
- Prompt template library (from Agent 2)
- Working SafetyGuard, PlannerAgent, ArchitectAgent (implemented by Agent 2)

### 🔄 What Agent 2 is Building (You'll Use These)
- `LLMClient` - Unified LLM interface
- `PromptLibrary` - Prompt templates
- `UsageTracker` - Token tracking

### ❌ What's Missing (Your Mission)
Complete implementation of:
1. **TesterAgent** - Generate and run unit tests
2. **DocWriterAgent** - Generate documentation
3. **GitOpsAgent** - Handle Git operations safely
4. **BlueCollarAdvisor** - Provide usability feedback (needs LLM)
5. **ImplementerAgent** - Enhance code generation (if not fully done by Agent 2)

## 🎯 Your Mission

Transform the remaining stub agents into fully functional components that:
1. Use LLM for intelligent generation
2. Interact with the file system safely
3. Execute external commands (git, pytest)
4. Return structured outputs
5. Handle errors gracefully

## 🚀 Priority Tasks

### Task 1: Implement TesterAgent ⭐ CRITICAL
**File**: `src/code_factory/agents/tester.py`

**What to Implement**:

The TesterAgent should:
1. Take a `ProjectSpec` as input
2. Generate pytest unit tests for all source files
3. Write test files to disk
4. Execute pytest
5. Return `TestResult` with pass/fail counts

```python
"""
TesterAgent - Generates and runs unit tests
"""

import subprocess
import logging
from pathlib import Path
from typing import List
from pydantic import BaseModel

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import ProjectSpec, TestResult
from code_factory.llm.client import LLMClient, LLMConfig
from code_factory.llm.prompts import PromptLibrary

logger = logging.getLogger(__name__)


class TesterAgent(BaseAgent):
    """Generates and executes tests"""

    def __init__(self):
        self.llm = LLMClient(LLMConfig())

    @property
    def name(self) -> str:
        return "tester"

    @property
    def description(self) -> str:
        return "Generates and runs comprehensive unit tests"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """Generate tests and run them"""
        spec = self.validate_input(input_data, ProjectSpec)

        logger.info(f"Generating tests for {spec.name}")

        # Step 1: Read source files
        source_files = self._get_source_files(spec)

        # Step 2: Generate test files using LLM
        test_files = []
        for source_file in source_files:
            test_content = self._generate_test_for_file(source_file, spec)
            test_file = self._write_test_file(source_file, test_content, spec)
            test_files.append(test_file)

        # Step 3: Run pytest
        result = self._run_pytest(spec.name)

        logger.info(f"Tests: {result.passed}/{result.total_tests} passed")
        return result

    def _get_source_files(self, spec: ProjectSpec) -> List[Path]:
        """Find all source files to test"""
        # Implementation...

    def _generate_test_for_file(self, source_file: Path, spec: ProjectSpec) -> str:
        """Use LLM to generate test"""
        # Read source code
        source_code = source_file.read_text()

        # Render prompt
        prompt = PromptLibrary.render(
            "TESTER",
            source_file=source_file.name,
            source_code=source_code,
            spec=spec
        )

        # Generate tests
        response = self.llm.generate(
            system_prompt="You are a Python testing expert. Generate comprehensive pytest tests.",
            user_prompt=prompt,
            temperature=0.4
        )

        return response.content

    def _run_pytest(self, project_name: str) -> TestResult:
        """Execute pytest and parse results"""
        project_path = Path("/Users/dp/Projects") / project_name

        try:
            result = subprocess.run(
                ["pytest", str(project_path / "tests"), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=300
            )

            # Parse pytest output
            return self._parse_pytest_output(result.stdout)

        except subprocess.TimeoutExpired:
            return TestResult(success=False, error_messages=["Tests timed out"])
        except Exception as e:
            return TestResult(success=False, error_messages=[str(e)])
```

**Additional Helper Methods**:
```python
def _parse_pytest_output(self, output: str) -> TestResult:
    """Parse pytest output into TestResult"""
    # Example: "5 passed, 2 failed in 3.21s"
    import re

    passed = failed = skipped = 0

    passed_match = re.search(r'(\d+) passed', output)
    if passed_match:
        passed = int(passed_match.group(1))

    failed_match = re.search(r'(\d+) failed', output)
    if failed_match:
        failed = int(failed_match.group(1))

    skipped_match = re.search(r'(\d+) skipped', output)
    if skipped_match:
        skipped = int(skipped_match.group(1))

    total = passed + failed + skipped
    success = failed == 0

    return TestResult(
        total_tests=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        success=success
    )
```

**Success Criteria**:
- [ ] Generates valid pytest tests for source files
- [ ] Writes test files to correct locations
- [ ] Executes pytest successfully
- [ ] Parses test results correctly
- [ ] Returns proper TestResult model
- [ ] Handles errors gracefully (missing files, syntax errors, etc.)
- [ ] Unit tests for the agent itself

**Estimated Effort**: 4-5 hours

---

### Task 2: Implement DocWriterAgent ⭐ CRITICAL
**File**: `src/code_factory/agents/doc_writer.py`

**What to Implement**:

The DocWriterAgent should:
1. Take a `ProjectSpec` as input
2. Generate README.md with usage examples
3. Generate API documentation from docstrings
4. Create usage guides
5. Return list of created documentation files

```python
"""
DocWriterAgent - Generates comprehensive documentation
"""

from pathlib import Path
from typing import List
from pydantic import BaseModel

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import ProjectSpec
from code_factory.llm.client import LLMClient, LLMConfig
from code_factory.llm.prompts import PromptLibrary


class DocOutput(BaseModel):
    """Output from DocWriterAgent"""
    files_created: List[str]
    readme_path: str


class DocWriterAgent(BaseAgent):
    """Generates project documentation"""

    def __init__(self):
        self.llm = LLMClient(LLMConfig())

    @property
    def name(self) -> str:
        return "doc_writer"

    @property
    def description(self) -> str:
        return "Generates comprehensive project documentation"

    def execute(self, input_data: BaseModel) -> BaseModel:
        spec = self.validate_input(input_data, ProjectSpec)

        logger.info(f"Generating docs for {spec.name}")

        # Generate README.md
        readme = self._generate_readme(spec)
        readme_path = self._write_readme(readme, spec)

        # Generate usage guide
        usage_guide = self._generate_usage_guide(spec)
        usage_path = self._write_usage_guide(usage_guide, spec)

        # Generate API docs (if applicable)
        api_docs = self._generate_api_docs(spec)
        api_path = self._write_api_docs(api_docs, spec) if api_docs else None

        files_created = [readme_path, usage_path]
        if api_path:
            files_created.append(api_path)

        return DocOutput(
            files_created=files_created,
            readme_path=readme_path
        )

    def _generate_readme(self, spec: ProjectSpec) -> str:
        """Generate README.md content"""
        prompt = PromptLibrary.render("DOC_WRITER_README", spec=spec)

        response = self.llm.generate(
            system_prompt="You are a technical writer. Create clear, helpful documentation.",
            user_prompt=prompt,
            temperature=0.6
        )

        return response.content
```

**Prompt Template to Add** (`llm/prompts.py`):
```python
DOC_WRITER_README = """Generate a comprehensive README.md for this project:

Project Name: {{spec.name}}
Description: {{spec.description}}
Tech Stack: {{spec.tech_stack}}
Entry Point: {{spec.entry_point}}
Target Users: {{spec.user_profile}}
Environment: {{spec.environment}}

Include:
1. Project title and description
2. Installation instructions
3. Quick start / usage examples
4. Features list
5. Requirements
6. License (MIT)
7. Blue-collar focus (if applicable)

Make it clear, practical, and easy to follow.
"""
```

**Success Criteria**:
- [ ] Generates complete README.md
- [ ] Creates usage documentation
- [ ] Includes installation instructions
- [ ] Examples are clear and correct
- [ ] Blue-collar focus if applicable
- [ ] Files written to correct locations

**Estimated Effort**: 3-4 hours

---

### Task 3: Implement GitOpsAgent ⭐ CRITICAL
**File**: `src/code_factory/agents/git_ops.py`

**What to Implement**:

The GitOpsAgent should:
1. Initialize Git repository
2. Create .gitignore
3. Make initial commit
4. Optionally create GitHub repo (using `gh` CLI)
5. Push to remote
6. All operations logged to git_activity.log

```python
"""
GitOpsAgent - Handles Git operations safely
"""

import subprocess
import logging
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import ProjectSpec


logger = logging.getLogger(__name__)


class GitOutput(BaseModel):
    """Output from GitOpsAgent"""
    initialized: bool
    initial_commit: bool
    remote_created: bool
    remote_url: str = ""
    errors: List[str] = []


class GitOpsAgent(BaseAgent):
    """Manages Git operations safely"""

    def __init__(self):
        self.activity_log = Path("git_activity.log")

    @property
    def name(self) -> str:
        return "git_ops"

    @property
    def description(self) -> str:
        return "Handles version control and repository management"

    def execute(self, input_data: BaseModel) -> BaseModel:
        spec = self.validate_input(input_data, ProjectSpec)

        project_path = Path("/Users/dp/Projects") / spec.name

        result = GitOutput(
            initialized=False,
            initial_commit=False,
            remote_created=False
        )

        try:
            # Step 1: Initialize Git
            if self._git_init(project_path):
                result.initialized = True
                self._log_activity(f"Initialized Git repo: {project_path}")

            # Step 2: Create .gitignore
            self._create_gitignore(project_path)

            # Step 3: Initial commit
            if self._initial_commit(project_path):
                result.initial_commit = True
                self._log_activity(f"Created initial commit: {spec.name}")

            # Step 4: Create GitHub repo (optional)
            # Implement if gh CLI is available

        except Exception as e:
            logger.error(f"Git operation failed: {e}")
            result.errors.append(str(e))

        return result

    def _git_init(self, project_path: Path) -> bool:
        """Initialize Git repository"""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=project_path,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"git init failed: {e}")
            return False

    def _initial_commit(self, project_path: Path) -> bool:
        """Create initial commit"""
        try:
            # Add all files
            subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                check=True
            )

            # Commit
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=project_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"git commit failed: {e}")
            return False

    def _log_activity(self, message: str):
        """Log Git operations"""
        timestamp = datetime.now().isoformat()
        with self.activity_log.open("a") as f:
            f.write(f"{timestamp} - {message}\n")

    def _create_gitignore(self, project_path: Path):
        """Create appropriate .gitignore"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.key
*.pem
credentials.json

# Testing
.coverage
htmlcov/
.pytest_cache/
"""
        gitignore_path = project_path / ".gitignore"
        gitignore_path.write_text(gitignore_content)
```

**Success Criteria**:
- [ ] Initializes Git repo
- [ ] Creates proper .gitignore
- [ ] Makes initial commit
- [ ] All operations logged
- [ ] Handles errors gracefully
- [ ] No operations outside designated directories

**Estimated Effort**: 2-3 hours

---

### Task 4: Enhance BlueCollarAdvisor with LLM
**File**: `src/code_factory/agents/blue_collar_advisor.py`

**What to Implement**:

Currently has placeholder logic. Add LLM-powered analysis:

```python
def execute(self, input_data: BaseModel) -> BaseModel:
    spec = self.validate_input(input_data, ProjectSpec)

    logger.info(f"Analyzing usability for {spec.user_profile}")

    # Render prompt
    prompt = PromptLibrary.render("BLUE_COLLAR_ADVISOR", spec=spec)

    # Get LLM analysis
    response = self.llm.generate(
        system_prompt="You are an expert in designing software for field workers.",
        user_prompt=prompt,
        temperature=0.5
    )

    # Parse response
    result = json.loads(response.content)
    return AdvisoryReport(**result)
```

**Success Criteria**:
- [ ] Uses LLM for analysis
- [ ] Provides practical recommendations
- [ ] Considers harsh environments
- [ ] Returns proper AdvisoryReport

**Estimated Effort**: 1-2 hours

---

### Task 5: Complete ImplementerAgent (If Needed)
**File**: `src/code_factory/agents/implementer.py`

**What to Verify/Enhance**:

If Agent 2 hasn't fully completed this:
1. Generates Python code from tasks
2. Handles multiple files
3. Uses streaming for long code generation
4. Writes files to correct locations
5. Validates syntax (using `ast.parse`)

```python
def execute(self, input_data: BaseModel) -> BaseModel:
    # Takes Task + ProjectSpec
    # Generates code for that task
    # Writes to file
    # Returns CodeOutput with file paths
```

**Success Criteria**:
- [ ] Generates syntactically correct Python
- [ ] Includes docstrings and type hints
- [ ] Handles imports correctly
- [ ] Writes to correct file paths
- [ ] Validates code before writing

**Estimated Effort**: 2-3 hours (if needed)

---

## 🔗 Integration Points

### Your Code is Used By:
- **Agent 1 (Backend Engineer)** - Orchestrator uses your agents in pipeline
- **Agent 4 (Testing Engineer)** - Needs working agents to test
- **Agent 5 (Templates Engineer)** - Uses agents to generate templates

### You Depend On:
- **Agent 2 (LLM Specialist)** - Need LLMClient and PromptLibrary
- **Agent 1 (Backend Engineer)** - Need working runtime (lightweight)

### Shared Interfaces You Provide:
```python
# TesterAgent
TesterAgent.execute(spec: ProjectSpec) -> TestResult

# DocWriterAgent
DocWriterAgent.execute(spec: ProjectSpec) -> DocOutput

# GitOpsAgent
GitOpsAgent.execute(spec: ProjectSpec) -> GitOutput

# BlueCollarAdvisor
BlueCollarAdvisor.execute(spec: ProjectSpec) -> AdvisoryReport
```

## ✅ Success Criteria

### Phase 1: Core Agents (Priority)
- [ ] TesterAgent generates and runs tests
- [ ] DocWriterAgent creates README and docs
- [ ] GitOpsAgent initializes repos

### Phase 2: Enhancement
- [ ] BlueCollarAdvisor uses LLM
- [ ] ImplementerAgent complete (if needed)

### Phase 3: Integration
- [ ] All agents work in orchestrator pipeline
- [ ] Integration tests pass
- [ ] End-to-end test works

### Code Quality
- [ ] All agents have unit tests
- [ ] Docstrings on all methods
- [ ] Error handling complete
- [ ] No hardcoded paths

## 🚧 Constraints

- **File Scope**: Only modify `src/code_factory/agents/` files
- **External Commands**: Only git, pytest (no dangerous commands)
- **File System**: All operations in `/Users/dp/Projects`
- **Testing**: Write unit tests for each agent
- **Safety**: All file writes must be validated
- **Logging**: Use logging module, not print

## 📝 Getting Started

### Step 1: Wait for Agent 2
Check that LLM infrastructure is ready:
```python
# Test if LLMClient works
from code_factory.llm.client import LLMClient, LLMConfig
client = LLMClient(LLMConfig())
# Should not raise errors
```

### Step 2: Start with TesterAgent
This is the most critical agent for quality.

### Step 3: Add Prompt Templates
If Agent 2 didn't include prompts for your agents, add them to `llm/prompts.py`.

### Step 4: Test Each Agent Individually
```bash
pytest tests/unit/test_tester.py -v
pytest tests/unit/test_doc_writer.py -v
pytest tests/unit/test_git_ops.py -v
```

### Step 5: Integration Test
Test all agents together in orchestrator.

## 📊 Example Test

```python
# tests/unit/test_tester.py

def test_tester_agent():
    """Test TesterAgent generates and runs tests"""
    agent = TesterAgent()

    spec = ProjectSpec(
        name="test-project",
        description="Test project",
        tech_stack={"language": "python"},
        folder_structure={"src/": ["main.py"]},
        entry_point="src/main.py"
    )

    result = agent.execute(spec)

    assert isinstance(result, TestResult)
    assert result.total_tests > 0
```

## ❓ Questions?

Post to `AGENT_PROMPTS/questions.md`.

## 🎯 Your Branch

**Branch Name**: `agent-implementations`

```bash
git checkout -b agent-implementations
git add .
git commit -m "feat: implement TesterAgent with LLM"
git push -u origin agent-implementations
```

## 📅 Timeline

- **Day 1-2**: TesterAgent (Task 1)
- **Day 3**: DocWriterAgent (Task 2)
- **Day 4**: GitOpsAgent (Task 3)
- **Day 5**: BlueCollarAdvisor + ImplementerAgent (Tasks 4-5)

**Total Estimated Time**: 12-18 hours (2-3 weeks part-time)

---

**Ready to start? Begin with Task 1: Implement TesterAgent!**
