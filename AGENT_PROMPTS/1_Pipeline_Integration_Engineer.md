# Agent 1: Pipeline Integration Engineer

**Repository:** https://github.com/Dparent97/AgentOrchestratedCodeFactory
**Branch:** `claude/fix-pipeline-integration`
**Iteration:** Phase 3 - Critical Infrastructure Fixes
**Time Estimate:** 2-3 hours

---

## 🎯 Your Mission

Fix critical infrastructure issues preventing the Code Factory from working end-to-end. You'll restore the orchestrator pipeline, fix module imports, resolve task ID format inconsistencies, and enable full project generation.

---

## 🔴 Critical Issues to Fix

### Issue #1: Broken Module Imports (CRITICAL)
**File:** `src/code_factory/agents/__init__.py`
**Line:** 1-8
**Problem:** All agent imports are commented out, making the public API unusable

**Current State:**
```python
"""Specialized agents for the Code Factory"""
# Agent imports will be added as they are implemented
# from code_factory.agents.planner import PlannerAgent
# ... (all commented)
__all__ = []
```

**Your Fix:**
```python
"""Specialized agents for the Code Factory"""

from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent
from code_factory.agents.implementer import ImplementerAgent
from code_factory.agents.tester import TesterAgent
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.agents.git_ops import GitOpsAgent
from code_factory.agents.blue_collar_advisor import BlueCollarAdvisor
from code_factory.agents.safety_guard import SafetyGuard

__all__ = [
    "PlannerAgent",
    "ArchitectAgent",
    "ImplementerAgent",
    "TesterAgent",
    "DocWriterAgent",
    "GitOpsAgent",
    "BlueCollarAdvisor",
    "SafetyGuard",
]
```

---

### Issue #2: Orchestrator Pipeline Disconnected (CRITICAL)
**File:** `src/code_factory/core/orchestrator.py`
**Lines:** 84-114
**Problem:** All 7 pipeline stages are commented out with TODO markers

**Current State:**
```python
logger.info("Stage 1: Safety validation")
# TODO: Implement safety check
# safety_run = self.runtime.execute_agent("safety_guard", idea)
```

**Your Fix:** Uncomment and connect all 7 pipeline stages:

1. **Stage 1: Safety Validation**
```python
logger.info("Stage 1: Safety validation")
safety_run = self.runtime.execute_agent("safety_guard", idea)
result.agent_runs.append(safety_run)

if not safety_run.output_data.approved:
    result.success = False
    result.errors.append(f"Safety check failed: {safety_run.output_data.blocked_keywords}")
    return result
```

2. **Stage 2: Planning**
```python
logger.info("Stage 2: Planning tasks")
planner_run = self.runtime.execute_agent("planner", idea)
result.agent_runs.append(planner_run)
tasks = planner_run.output_data.tasks
```

3. **Stage 3: Architecture**
```python
logger.info("Stage 3: Designing architecture")
architect_input = {"idea": idea, "tasks": tasks}
architect_run = self.runtime.execute_agent("architect", architect_input)
result.agent_runs.append(architect_run)
result.project_spec = architect_run.output_data.spec
result.project_name = result.project_spec.name
```

4. **Stage 4-7:** Connect ImplementerAgent, TesterAgent, DocWriterAgent, GitOpsAgent (keep placeholder logic for now since agents aren't fully implemented, but enable execution)

---

### Issue #3: Task ID Format Mismatch
**Files:**
- `src/code_factory/agents/planner.py` (line 71, 85, 99, etc.)
- `tests/test_smoke.py` (line 76)

**Problem:** PlannerAgent generates `"task_1"`, but test expects `"t1"`

**Your Fix:** Update PlannerAgent to use consistent format:
```python
# In planner.py, replace:
id=f"task_{task_counter}"

# With:
id=f"t{task_counter}"
```

**OR** update the test expectation - decide which format is better for the project and apply consistently.

---

## 📝 Implementation Steps

### Step 1: Fix Module Imports (10 minutes)
1. Open `src/code_factory/agents/__init__.py`
2. Uncomment all imports
3. Populate `__all__` list
4. Run tests to verify: `pytest tests/test_smoke.py -v`

### Step 2: Fix Task ID Format (10 minutes)
1. Open `src/code_factory/agents/planner.py`
2. Find all instances of `f"task_{task_counter}"`
3. Replace with `f"t{task_counter}"` OR update test expectations
4. Run planner tests: `pytest tests/unit/test_agents.py::test_planner -v`

### Step 3: Restore Orchestrator Pipeline (60-90 minutes)
1. Open `src/code_factory/core/orchestrator.py`
2. Uncomment Stage 1 (Safety validation)
3. Add proper error handling and output collection
4. Uncomment Stage 2 (Planning)
5. Uncomment Stage 3 (Architecture)
6. For Stages 4-7 (Implementer, Tester, DocWriter, GitOps):
   - Uncomment the calls
   - Keep execution enabled even though they return placeholders
   - Document that these are placeholder implementations
7. Remove the hardcoded `result.success = True` at line 114
8. Set `result.success` based on actual pipeline execution

### Step 4: Add Pipeline Error Handling (30 minutes)
1. Wrap each stage in try-except
2. Collect errors in `result.errors`
3. Fail fast on critical errors (safety, planning, architecture)
4. Log warnings for non-critical errors

### Step 5: Test End-to-End (30 minutes)
1. Run integration tests: `pytest tests/integration/test_wave1_pipeline.py -v`
2. Run smoke test: `pytest tests/test_smoke.py -v`
3. Test CLI: `code-factory status` (should work without errors)
4. Manual test: Try running a simple idea through the pipeline

---

## ✅ Success Criteria

- [ ] All imports work: `from code_factory.agents import PlannerAgent` succeeds
- [ ] Smoke test passes: `pytest tests/test_smoke.py`
- [ ] Task ID format is consistent across codebase
- [ ] Orchestrator pipeline executes all 7 stages
- [ ] SafetyGuard, PlannerAgent, ArchitectAgent integrated and working
- [ ] Pipeline returns real `ProjectResult` with actual data
- [ ] No placeholder `result.success = True` bypass
- [ ] All existing tests pass (you may need to update expectations)
- [ ] Integration test passes: `pytest tests/integration/`
- [ ] Code follows style guide: `ruff check src/` and `black src/`
- [ ] All functions have docstrings
- [ ] Mypy type checking passes: `mypy src/`

---

## 🧪 Testing Checklist

Run these commands before creating your PR:

```bash
# 1. Run all unit tests
pytest tests/unit/ -v

# 2. Run integration tests
pytest tests/integration/ -v

# 3. Run smoke test
pytest tests/test_smoke.py -v

# 4. Check code coverage
pytest --cov=src/code_factory --cov-report=term

# 5. Run linting
ruff check src/

# 6. Run formatting check
black --check src/

# 7. Run type checking
mypy src/
```

All must pass before your PR is ready.

---

## 📋 Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| `src/code_factory/agents/__init__.py` | Uncomment imports, populate `__all__` | CRITICAL |
| `src/code_factory/core/orchestrator.py` | Uncomment pipeline stages, add error handling | CRITICAL |
| `src/code_factory/agents/planner.py` | Fix task ID format | HIGH |
| `tests/test_smoke.py` | Update task ID expectation (if needed) | HIGH |
| `tests/integration/test_wave1_pipeline.py` | May need updates after pipeline changes | MEDIUM |

---

## 🚨 Integration Points

### Your Work Depends On:
- **None** - You can start immediately

### Other Agents Depend On You:
- **Agent 2 (Code Generation)** - Needs working pipeline to test ImplementerAgent
- **Agent 3 (Git Operations)** - Needs pipeline to integrate GitOpsAgent
- **Agent 4 (Testing & Docs)** - Needs pipeline to integrate TesterAgent and DocWriterAgent

**Critical:** Your work unblocks all other agents. Prioritize speed and correctness.

---

## 📝 Git Workflow

### Branch Setup:
```bash
git checkout -b claude/fix-pipeline-integration
```

### Commit Messages (use conventional commits):
```bash
git commit -m "fix: restore agent module imports in __init__.py"
git commit -m "fix: connect orchestrator pipeline stages 1-3"
git commit -m "fix: standardize task ID format to 't{n}'"
git commit -m "feat: add pipeline error handling and validation"
git commit -m "test: update integration tests for restored pipeline"
```

### Create PR:
```bash
# Run all tests first
pytest

# Push to remote
git push -u origin claude/fix-pipeline-integration

# Create PR (manually or via gh CLI if available)
# Title: "fix: Restore orchestrator pipeline and fix critical imports"
# Description: "Fixes critical infrastructure issues:
# - Restore agent module imports
# - Connect orchestrator pipeline stages
# - Fix task ID format inconsistency
# - Add proper error handling
# - Enable end-to-end project generation"
```

---

## 💡 Design Decisions

### Task ID Format: "t1" vs "task_1"
**Recommendation:** Use `"t{n}"` (e.g., "t1", "t2", "t3")
**Rationale:**
- Shorter, cleaner IDs
- Consistent with test expectations
- Common pattern in task management systems

### Pipeline Error Handling Strategy
**Recommendation:** Fail fast on critical stages, log warnings on optional stages
**Logic:**
```python
# Critical stages (fail immediately):
- Safety validation
- Planning
- Architecture

# Optional stages (log warnings, continue):
- Code implementation (placeholder for now)
- Testing (placeholder for now)
- Documentation (placeholder for now)
- Git operations (placeholder for now)
```

---

## 📚 Reference Documentation

- **Architecture:** `docs/architecture.md`
- **Agent Roles:** `docs/agent_roles.md`
- **Safety Guidelines:** `docs/safety.md`
- **Orchestrator Design:** `src/code_factory/core/orchestrator.py` (docstrings)
- **Coordination:** `AGENT_PROMPTS/COORDINATION.md`

---

## ❓ Questions?

Post to `AGENT_PROMPTS/questions.md`:

```markdown
## Pipeline Integration Engineer - 2025-11-18 - Q1

**Question:** Should I fail the pipeline if ImplementerAgent returns placeholder code?

**Context:** ImplementerAgent is not fully implemented yet, returns mock data

**Blocking:** No, but affects pipeline logic

**Target:** @Code-Generation-Engineer or Coordinator
```

---

## 📊 Daily Progress Log

Update `AGENT_PROMPTS/daily_logs/2025-11-18.md` with:

```markdown
## Pipeline Integration Engineer - 2025-11-18

### Completed
- [List what you finished]

### In Progress
- [What you're working on now]

### Blockers
- [Any blockers - None expected]

### Next Steps
- [What's next]
```

---

## 🎯 Ready to Start?

1. **Read** this entire prompt
2. **Clone** the repository (if not already)
3. **Create** your branch: `claude/fix-pipeline-integration`
4. **Start** with Issue #1 (module imports) - quick win
5. **Work** through issues in order
6. **Test** continuously as you go
7. **Commit** after each fix
8. **Create PR** when all success criteria met

---

**START NOW**
