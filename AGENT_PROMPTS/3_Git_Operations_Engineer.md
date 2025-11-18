# Agent 3: Git Operations Engineer

**Repository:** https://github.com/Dparent97/AgentOrchestratedCodeFactory
**Branch:** `claude/implement-git-operations`
**Iteration:** Phase 3 - GitOpsAgent Implementation
**Time Estimate:** 2-3 hours

---

## 🎯 Your Mission

Transform the GitOpsAgent from a logging-only placeholder into a real Git operations manager that creates repositories, commits code at each pipeline stage, and supports GitHub remote operations using the gitpython library.

---

## 🔴 Current Problem

**File:** `src/code_factory/agents/git_ops.py`
**Lines:** 65-75
**Status:** Logs operations but doesn't perform them

**Current Code:**
```python
def execute(self, input_data: BaseModel) -> BaseModel:
    spec = self.validate_input(input_data, ProjectSpec)
    logger.info(f"Setting up Git repository for: {spec.name}")

    # TODO: Implement actual Git operations using gitpython
    # For now, log to git_activity.log
    log_file = Path("git_activity.log")
    with open(log_file, "a") as f:
        f.write(f"Would create repo for: {spec.name}\n")

    return GitOutput(
        repo_created=True,
        initial_commit=True,
        remote_url="https://example.com/placeholder.git"
    )
```

**Problem:**
- Writes to log file instead of performing Git operations
- Returns fake remote URL
- gitpython dependency installed but never used

---

## ✅ Your Solution

Implement **real Git operations** using gitpython:
1. Create local Git repository
2. Initialize with .gitignore
3. Commit project files
4. Support staged commits (commit after each pipeline stage)
5. Optionally push to GitHub remote
6. Handle Git errors gracefully
7. Support both local-only and remote repositories

---

## 🏗️ Implementation Architecture

### Design Pattern: Repository Manager

```python
# High-level flow:
ProjectSpec + Files
  → Create local repo (git init)
  → Add .gitignore
  → Stage files (git add)
  → Commit (git commit -m "Initial commit")
  → [Optional] Add remote (git remote add origin)
  → [Optional] Push (git push -u origin main)
  → GitOutput (return results)
```

---

## 📝 Implementation Steps

### Step 1: Import and Setup gitpython (10 minutes)

**File:** `src/code_factory/agents/git_ops.py`

**Add imports:**
```python
from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)
```

**Verify gitpython is installed:**
```bash
# Should already be in pyproject.toml:
# gitpython>=3.1.41
```

---

### Step 2: Implement Git Repository Creation (45 minutes)

**Update GitOpsAgent class:**

```python
class GitOpsAgent(BaseAgent):
    """Agent that manages Git operations for generated projects"""

    @property
    def name(self) -> str:
        return "git_ops"

    @property
    def description(self) -> str:
        return "Manages Git repository creation and version control for generated projects"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """Create Git repository and commit generated code"""
        # Input can be either ProjectSpec or dict with spec + files
        if isinstance(input_data, dict):
            spec = input_data.get("spec")
            files = input_data.get("files", {})
            project_dir = input_data.get("project_dir")
        else:
            spec = self.validate_input(input_data, ProjectSpec)
            files = {}
            project_dir = None

        logger.info(f"Setting up Git repository for: {spec.name}")

        try:
            # Determine project directory
            if project_dir is None:
                project_dir = Path.cwd() / spec.name

            project_dir = Path(project_dir)

            # Create repository
            repo = self._create_repository(project_dir)

            # Configure repository
            self._configure_repo(repo, spec)

            # Initial commit (if files provided)
            commit_sha = None
            if files:
                commit_sha = self._commit_files(repo, files, "Initial project structure")

            # Get remote URL (if configured)
            remote_url = self._get_remote_url(repo)

            logger.info(f"Git repository created at: {project_dir}")

            return GitOutput(
                repo_created=True,
                initial_commit=commit_sha is not None,
                remote_url=remote_url or "No remote configured",
                repo_path=str(project_dir),
                commit_sha=commit_sha
            )

        except GitCommandError as e:
            logger.error(f"Git operation failed: {e}")
            return GitOutput(
                repo_created=False,
                initial_commit=False,
                remote_url="",
                error=str(e)
            )

    def _create_repository(self, project_dir: Path) -> Repo:
        """Create or open Git repository"""
        project_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Try to open existing repo
            repo = Repo(project_dir)
            logger.info(f"Opened existing repository at {project_dir}")
        except InvalidGitRepositoryError:
            # Create new repo
            repo = Repo.init(project_dir)
            logger.info(f"Initialized new repository at {project_dir}")

        return repo

    def _configure_repo(self, repo: Repo, spec: ProjectSpec) -> None:
        """Configure repository settings"""
        with repo.config_writer() as config:
            # Set user if not configured
            if not config.has_option("user", "name"):
                config.set_value("user", "name", "Code Factory")
            if not config.has_option("user", "email"):
                config.set_value("user", "email", "factory@example.com")

        # Create default branch (main)
        try:
            if not repo.heads:
                # No branches yet, will be created on first commit
                pass
            elif "main" not in repo.heads:
                # Rename master to main if needed
                if "master" in repo.heads:
                    repo.heads.master.rename("main")
        except Exception as e:
            logger.warning(f"Branch configuration warning: {e}")

    def _commit_files(self, repo: Repo, files: dict, message: str) -> Optional[str]:
        """Stage and commit files to repository"""
        try:
            # Add all files (they should already exist on disk)
            repo.git.add(A=True)  # git add -A

            # Check if there's anything to commit
            if not repo.is_dirty(untracked_files=True):
                logger.info("No changes to commit")
                return None

            # Commit
            commit = repo.index.commit(message)
            logger.info(f"Created commit: {commit.hexsha[:8]} - {message}")

            return commit.hexsha

        except GitCommandError as e:
            logger.error(f"Commit failed: {e}")
            return None

    def _get_remote_url(self, repo: Repo) -> Optional[str]:
        """Get remote URL if configured"""
        try:
            if "origin" in repo.remotes:
                return repo.remotes.origin.url
        except Exception:
            pass
        return None

    def add_remote(self, repo_path: Path, remote_url: str, remote_name: str = "origin") -> bool:
        """Add remote to repository"""
        try:
            repo = Repo(repo_path)

            # Remove existing remote if present
            if remote_name in repo.remotes:
                repo.delete_remote(remote_name)

            # Add new remote
            repo.create_remote(remote_name, remote_url)
            logger.info(f"Added remote '{remote_name}': {remote_url}")

            return True

        except Exception as e:
            logger.error(f"Failed to add remote: {e}")
            return False

    def push_to_remote(self, repo_path: Path, branch: str = "main", remote: str = "origin") -> bool:
        """Push commits to remote repository"""
        try:
            repo = Repo(repo_path)

            if remote not in repo.remotes:
                logger.error(f"Remote '{remote}' not configured")
                return False

            # Push to remote
            repo.remotes[remote].push(branch)
            logger.info(f"Pushed {branch} to {remote}")

            return True

        except GitCommandError as e:
            logger.error(f"Push failed: {e}")
            return False

    def commit_stage(self, repo_path: Path, stage_name: str, message: Optional[str] = None) -> Optional[str]:
        """Commit current state as a pipeline stage"""
        try:
            repo = Repo(repo_path)

            if not message:
                message = f"Pipeline stage: {stage_name}"

            # Add all changes
            repo.git.add(A=True)

            # Commit if there are changes
            if repo.is_dirty(untracked_files=True):
                commit = repo.index.commit(message)
                logger.info(f"Stage commit: {commit.hexsha[:8]} - {stage_name}")
                return commit.hexsha
            else:
                logger.info(f"No changes for stage: {stage_name}")
                return None

        except Exception as e:
            logger.error(f"Stage commit failed: {e}")
            return None
```

---

### Step 3: Update GitOutput Model (15 minutes)

**File:** `src/code_factory/core/models.py`

**Find GitOutput model and update:**

```python
class GitOutput(BaseModel):
    """Output from GitOpsAgent"""
    repo_created: bool
    initial_commit: bool
    remote_url: str
    repo_path: str = ""
    commit_sha: Optional[str] = None
    branch: str = "main"
    error: str = ""
```

---

### Step 4: Create Unit Tests (45 minutes)

**File:** `tests/unit/test_git_ops.py`

```python
import pytest
from pathlib import Path
import tempfile
import shutil
from git import Repo

from code_factory.agents.git_ops import GitOpsAgent
from code_factory.core.models import ProjectSpec

@pytest.fixture
def temp_project_dir():
    """Create temporary directory for test repos"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

def test_git_ops_creates_repository(temp_project_dir):
    """Test that GitOpsAgent creates a Git repository"""
    agent = GitOpsAgent()

    spec = ProjectSpec(
        name="test-project",
        description="Test project",
        tech_stack={"language": "python"},
        folder_structure={},
        dependencies=[],
        entry_point="main.py"
    )

    input_data = {
        "spec": spec,
        "project_dir": temp_project_dir / "test-project"
    }

    result = agent.execute(input_data)

    assert result.repo_created is True
    assert (temp_project_dir / "test-project" / ".git").exists()

    # Verify it's a valid Git repo
    repo = Repo(temp_project_dir / "test-project")
    assert repo.git_dir

def test_git_ops_creates_initial_commit(temp_project_dir):
    """Test that GitOpsAgent creates initial commit if files provided"""
    agent = GitOpsAgent()

    spec = ProjectSpec(
        name="test-project",
        description="Test",
        tech_stack={},
        folder_structure={},
        dependencies=[],
        entry_point="main.py"
    )

    # Create some files first
    project_dir = temp_project_dir / "test-project"
    project_dir.mkdir(parents=True)
    (project_dir / "README.md").write_text("# Test")
    (project_dir / "main.py").write_text("print('hello')")

    input_data = {
        "spec": spec,
        "project_dir": project_dir,
        "files": {"README.md": "# Test", "main.py": "print('hello')"}
    }

    result = agent.execute(input_data)

    assert result.initial_commit is True
    assert result.commit_sha is not None

    # Verify commit exists
    repo = Repo(project_dir)
    assert len(list(repo.iter_commits())) > 0

def test_git_ops_handles_existing_repo(temp_project_dir):
    """Test that GitOpsAgent can open existing repository"""
    agent = GitOpsAgent()

    project_dir = temp_project_dir / "existing-repo"
    project_dir.mkdir(parents=True)

    # Create repo manually first
    Repo.init(project_dir)

    spec = ProjectSpec(
        name="existing-repo",
        description="Test",
        tech_stack={},
        folder_structure={},
        dependencies=[],
        entry_point="main.py"
    )

    input_data = {
        "spec": spec,
        "project_dir": project_dir
    }

    result = agent.execute(input_data)

    assert result.repo_created is True  # "Created" means opened or created
    assert result.error == ""

def test_git_ops_commit_stage(temp_project_dir):
    """Test committing a pipeline stage"""
    agent = GitOpsAgent()

    project_dir = temp_project_dir / "stage-test"
    project_dir.mkdir(parents=True)

    # Initialize repo
    repo = Repo.init(project_dir)

    # Create and commit initial file
    (project_dir / "file1.txt").write_text("stage 1")
    repo.git.add(A=True)
    repo.index.commit("Initial commit")

    # Add new file for stage 2
    (project_dir / "file2.txt").write_text("stage 2")

    # Commit stage
    commit_sha = agent.commit_stage(project_dir, "planning")

    assert commit_sha is not None
    assert len(list(repo.iter_commits())) == 2

def test_git_ops_add_remote(temp_project_dir):
    """Test adding remote to repository"""
    agent = GitOpsAgent()

    project_dir = temp_project_dir / "remote-test"
    project_dir.mkdir(parents=True)
    repo = Repo.init(project_dir)

    # Add remote
    success = agent.add_remote(
        project_dir,
        "https://github.com/test/test.git"
    )

    assert success is True
    assert "origin" in repo.remotes
    assert repo.remotes.origin.url == "https://github.com/test/test.git"

def test_git_ops_handles_errors_gracefully(temp_project_dir):
    """Test that GitOpsAgent handles errors without crashing"""
    agent = GitOpsAgent()

    # Invalid input should not crash
    spec = ProjectSpec(
        name="error-test",
        description="Test",
        tech_stack={},
        folder_structure={},
        dependencies=[],
        entry_point="main.py"
    )

    # Point to invalid directory
    input_data = {
        "spec": spec,
        "project_dir": "/invalid/path/that/cannot/be/created/safely"
    }

    # Should not crash, should return error result
    result = agent.execute(input_data)

    # Either created (if permissions allow) or error
    # At minimum, should not raise exception
    assert isinstance(result.repo_created, bool)
```

---

## 📋 Files to Modify/Create

| File | Action | Priority |
|------|--------|----------|
| `src/code_factory/agents/git_ops.py` | MODIFY | CRITICAL |
| `src/code_factory/core/models.py` (GitOutput) | MODIFY | HIGH |
| `tests/unit/test_git_ops.py` | CREATE/MODIFY | HIGH |
| `tests/integration/test_wave1_pipeline.py` | MODIFY | MEDIUM |

---

## ✅ Success Criteria

- [ ] GitOpsAgent creates real Git repositories (git init)
- [ ] GitOpsAgent commits files with proper messages
- [ ] GitOpsAgent can add remotes
- [ ] GitOpsAgent can commit pipeline stages
- [ ] GitOpsAgent handles errors gracefully (returns GitOutput with error field)
- [ ] Unit tests achieve 80%+ coverage
- [ ] All tests pass: `pytest tests/unit/test_git_ops.py -v`
- [ ] Integration test creates repo for generated project
- [ ] Code follows style guide: `ruff` and `black`
- [ ] Documentation updated in docstrings

---

## 🧪 Testing Strategy

### Unit Tests:
- Repository creation
- Initial commit
- Opening existing repos
- Stage commits
- Remote management
- Error handling

### Integration Tests:
- Full pipeline creates Git repo
- Commits at each stage
- Final project has complete Git history

### Manual Tests:
```bash
# Generate a project
code-factory create "Build a log parser"

# Check Git repo was created
cd output/log-parser
git log  # Should show commits
git remote -v  # Check remotes
```

---

## 🚨 Integration Points

### You Depend On:
- **Agent 1 (Pipeline Integration)** - Need working orchestrator
- **Agent 2 (Code Generation)** - Need real files to commit

### Other Agents Depend On You:
- **None** - You're the final stage in pipeline

### Integration with Orchestrator:
After Agent 1 is complete, the orchestrator will call you like:

```python
# Stage 7: Git operations (in orchestrator.py)
git_input = {
    "spec": result.project_spec,
    "project_dir": output_dir,
    "files": implementer_output.files
}
git_run = self.runtime.execute_agent("git_ops", git_input)
result.agent_runs.append(git_run)
```

---

## 📝 Git Workflow

```bash
# Create branch
git checkout -b claude/implement-git-operations

# Commit incrementally
git commit -m "feat: implement Git repository creation with gitpython"
git commit -m "feat: add commit staging and remote management"
git commit -m "test: add comprehensive GitOpsAgent tests"
git commit -m "docs: update GitOpsAgent docstrings"

# Push and create PR
git push -u origin claude/implement-git-operations
```

**PR Title:** `feat: Implement real Git operations in GitOpsAgent`

**PR Description:**
```markdown
Transforms GitOpsAgent from logging placeholder to real Git manager.

## Changes:
- Implemented Git repository creation using gitpython
- Added commit functionality with staged commits
- Implemented remote management (add remote, push)
- Added comprehensive error handling
- Updated GitOutput model with additional fields
- Created full unit test suite

## Features:
- Create new Git repositories
- Open existing repositories
- Commit files with custom messages
- Commit pipeline stages individually
- Add GitHub remotes
- Push to remotes (optional)
- Handle errors gracefully

## Testing:
- 10+ unit tests covering all operations
- Integration test verifies end-to-end Git workflow
- Manual test: Generated projects have valid Git repos

Closes #XX
```

---

## 💡 Design Decisions

### Why gitpython vs. subprocess?
**Decision:** Use gitpython library
**Rationale:**
- Already in dependencies
- Python-native API
- Better error handling
- Cross-platform compatibility
- Easier to test

### Should we auto-push to GitHub?
**Decision:** Support remote operations but don't auto-push
**Rationale:**
- Requires authentication (SSH keys, tokens)
- User may not want remote repo
- Local-first is safer default
- Can add `--push` flag later

### How to handle Git user config?
**Decision:** Set default "Code Factory" user if none configured
**Rationale:**
- Ensures commits work even if Git not configured
- User can override with their own config
- Prevents "Please tell me who you are" errors

---

## 📚 Reference Documentation

- **gitpython Documentation:** https://gitpython.readthedocs.io/
- **Git Basics:** https://git-scm.com/book/en/v2/Git-Basics
- **Current GitOpsAgent:** `src/code_factory/agents/git_ops.py`
- **GitOutput Model:** `src/code_factory/core/models.py`

---

## ❓ Questions?

Post to `AGENT_PROMPTS/questions.md`:

```markdown
## Git Operations Engineer - 2025-11-18 - Q1

**Question:** Should we support branch creation for features?

**Context:** Currently only creating main branch

**Blocking:** No, but could be useful for future iterations

**Target:** @Coordinator
```

---

## 🎯 Ready to Start?

1. **Read** gitpython documentation (quick skim)
2. **Create** your branch
3. **Import** gitpython in git_ops.py
4. **Implement** repository creation
5. **Add** commit functionality
6. **Write** tests
7. **Test** integration
8. **Create PR**

---

**START NOW**
