# Agent Learnings System
**Version:** 1.0  
**Purpose:** Capture, organize, and reuse agent knowledge across iterations and projects

---

## 🧠 Overview

This system enables agents to learn from their experiences and share knowledge across:
- Multiple iterations within a project
- Multiple projects
- Different agent roles
- Common patterns and anti-patterns

### Key Benefits:
1. **Faster Execution** - Agents start with proven patterns
2. **Fewer Mistakes** - Learn from past errors
3. **Better Quality** - Apply accumulated best practices
4. **Knowledge Retention** - Preserve institutional knowledge
5. **Cross-Project Learning** - Apply learnings universally

---

## 📁 File Structure

```
project/
├── AGENT_LEARNINGS/
│   ├── MASTER_LEARNINGS.md           # All learnings aggregated
│   ├── ITERATION_1_LEARNINGS.md      # What we learned this iteration
│   ├── ITERATION_2_LEARNINGS.md
│   ├── BY_ROLE/
│   │   ├── BACKEND_ENGINEER.md       # Role-specific learnings
│   │   ├── FEATURE_DEVELOPER.md
│   │   ├── INTERFACE_ENGINEER.md
│   │   ├── QA_ENGINEER.md
│   │   └── TECHNICAL_WRITER.md
│   ├── BY_CATEGORY/
│   │   ├── ARCHITECTURE.md           # Topic-specific learnings
│   │   ├── SECURITY.md
│   │   ├── PERFORMANCE.md
│   │   ├── TESTING.md
│   │   └── INTEGRATION.md
│   └── BY_LANGUAGE/
│       ├── PYTHON.md                 # Language-specific learnings
│       ├── JAVASCRIPT.md
│       └── TYPESCRIPT.md
└── CROSS_PROJECT_LEARNINGS/
    ├── PROJECT_A_LEARNINGS.md        # Export learnings to reuse
    ├── PROJECT_B_LEARNINGS.md
    └── UNIVERSAL_PATTERNS.md          # Patterns that work everywhere
```

---

## 📝 Learning Entry Template

```markdown
### [Learning Title] ✅ | ⚠️ | ❌
**Date:** YYYY-MM-DD  
**Iteration:** N  
**Agent:** [Role Name]  
**Category:** [Architecture | Security | Performance | Testing | Integration | Other]  
**Impact:** [High | Medium | Low]  
**Reusability:** [Universal | Project-Specific | Language-Specific]

#### Context
[What were you doing? What was the situation?]

#### What Happened
[What did you try? What was the result?]

#### Learning
[What did you learn? What should/shouldn't be done?]

#### Pattern to Follow âœ…
```code
[If this worked, show the pattern]
```

#### Pattern to Avoid ❌
```code
[If this failed, show what NOT to do]
```

#### When to Apply
- [Condition 1: When to use this learning]
- [Condition 2: When it's relevant]
- [Condition 3: When it's NOT applicable]

#### Related Learnings
- [Link to related learning #42]
- [Link to related learning #87]

#### Tags
`#architecture` `#database` `#performance` `#python`
```

---

## ðŸ"Š Learning Categories

### 1. Architecture Learnings
Patterns about code structure, organization, design patterns

### 2. Security Learnings  
Vulnerabilities found, security patterns, best practices

### 3. Performance Learnings
Optimization techniques, bottlenecks discovered, profiling insights

### 4. Testing Learnings
Test strategies, coverage insights, test patterns that work

### 5. Integration Learnings
How to integrate components, handoff patterns, API design

### 6. Tooling Learnings
Tool usage, automation, CI/CD, development workflow

### 7. Communication Learnings
How agents should coordinate, documentation patterns

### 8. Language-Specific Learnings
Best practices for Python, JavaScript, TypeScript, etc.

---

## 📚 Master Learnings Template

```markdown
# Master Agent Learnings
**Project:** [Name]  
**Last Updated:** [Date]  
**Total Learnings:** [Count]

## Quick Navigation
- [Architecture](#architecture)
- [Security](#security)
- [Performance](#performance)
- [Testing](#testing)
- [Integration](#integration)
- [By Agent Role](#by-role)

---

## 🏆 Top 10 Most Impactful Learnings

1. **[Learning Title]** - [Impact: High] - [Iteration 2]
   - Applied in: 5 subsequent iterations
   - Time saved: ~8 hours per iteration
   
2. **[Learning Title]** - [Impact: High] - [Iteration 1]
   - Prevented: 3 security vulnerabilities
   - Quality improvement: +15%

[Continue for top 10...]

---

## 🎯 Universal Patterns (Work Everywhere)

### âœ… Always Validate Input at Boundaries
**Learning:** Never trust user input, validate at API/function boundaries

**Pattern:**
```python
def process_user_data(data: dict) -> Result:
    # Validate FIRST
    if not validate_schema(data):
        raise ValidationError("Invalid input")
    
    # Then process
    return process(data)
```

**Impact:** Prevented 12 injection vulnerabilities across 3 projects

**When to Apply:** Every function that accepts external input

---

### âœ… Use Connection Pooling for Databases
**Learning:** Creating new connections is expensive, pool them

**Pattern:**
```python
# Good: Reuse connections
from sqlalchemy import create_engine, pool

engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20
)
```

**Before:** 450ms average query time  
**After:** 85ms average query time (-80%)

**When to Apply:** Any database-backed application

---

[Continue with more universal patterns...]

---

## 🏗️ Architecture Learnings

### #001: Separate Core from Features âœ…
**Date:** 2025-11-15 | **Iteration:** 1 | **Agent:** Backend Engineer  
**Impact:** High | **Reusability:** Universal

#### Context
Building a new system with multiple features that depend on core infrastructure.

#### What Happened
Initially put everything in a single `services/` directory. As complexity grew, features became tightly coupled to core, making changes difficult.

#### Learning
Always separate core infrastructure from business logic features.

#### Pattern to Follow âœ…
```
src/
├── core/              # Infrastructure everyone depends on
│   ├── runtime/       # Execution engine
│   ├── storage/       # Persistence
│   └── config/        # Configuration
└── features/          # Business logic
    ├── auth/          # Authentication feature
    ├── reporting/     # Reporting feature
    └── analytics/     # Analytics feature
```

**Benefits:**
- Core can evolve independently
- Features don't break each other
- Easier to test in isolation
- Clear dependencies (features → core, never core → features)

#### When to Apply
- Any project with 3+ distinct features
- When planning long-term maintainability
- When multiple agents work on different features

#### Related Learnings
- [#023: Use Dependency Injection](#023)
- [#045: Define Clear Interfaces](#045)

#### Applied In
- Iteration 2: Refactored to this structure (-40% coupling)
- Iteration 3: New features added without core changes
- Project B: Used from day 1 (saved 20+ hours)

---

### #002: Define APIs Before Implementation âœ…
**Date:** 2025-11-16 | **Iteration:** 1 | **Agent:** Backend Engineer  
**Impact:** High | **Reusability:** Universal

#### Context
Two agents needed to integrate: Backend creating API, Feature consuming it.

#### What Happened
Backend started implementing without clear API definition. Feature developer had to wait and then found API didn't match needs. Required rework.

#### Learning
Define interface contracts BEFORE implementation begins.

#### Pattern to Follow âœ…
Create interface/protocol files first:

```python
# core/interfaces.py - Define FIRST
from typing import Protocol, List, Optional

class StorageBackend(Protocol):
    """Storage interface that all implementations must follow"""
    
    def save(self, key: str, value: dict) -> bool:
        """Save data to storage"""
        ...
    
    def load(self, key: str) -> Optional[dict]:
        """Load data from storage"""
        ...
    
    def list_keys(self, prefix: str) -> List[str]:
        """List all keys with prefix"""
        ...
```

Then implement:
```python
# core/storage/file_storage.py - Implement SECOND
class FileStorage:
    """Concrete implementation of StorageBackend"""
    
    def save(self, key: str, value: dict) -> bool:
        # Implementation
        pass
```

**Benefits:**
- Agents can work in parallel
- No rework due to API mismatches
- Clear expectations
- Easy to mock for testing

#### When to Apply
- Before starting work in Phase 4
- When 2+ agents need to integrate
- In Phase 3 (Codex Review) planning

#### Applied In
- Iteration 2: No integration issues (vs 4 issues in It.1)
- Saved: 3 hours of rework time

---

## 🔒 Security Learnings

### #015: Never Store Secrets in Code ❌
**Date:** 2025-11-15 | **Iteration:** 1 | **Agent:** Backend Engineer  
**Impact:** Critical | **Reusability:** Universal

#### Context
Needed API keys for external services during development.

#### What Happened
Developer hardcoded API key in config file for testing. Almost committed to repo. Security scan caught it during Phase 5.5 review.

#### Learning
NEVER put secrets in code, even temporarily.

#### Pattern to Avoid ❌
```python
# BAD: Secret in code
API_KEY = "sk_live_51HxQp2C9F..."  # NEVER DO THIS
```

#### Pattern to Follow âœ…
```python
# GOOD: Load from environment
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

With `.env` file (in `.gitignore`):
```bash
# .env - NEVER commit this file
API_KEY=sk_live_51HxQp2C9F...
```

With `.env.example` (safe to commit):
```bash
# .env.example - Template for developers
API_KEY=your_api_key_here
```

**Prevention:**
- Add to `.gitignore`: `*.env`, `secrets.json`
- Use pre-commit hooks to scan for secrets
- Use environment variables or secret managers

#### When to Apply
- ALWAYS, without exception
- From day 1 of project
- Even in private repos (they can become public)

#### Related Learnings
- [#016: Use Secret Managers in Production](#016)
- [#034: Rotate Secrets Regularly](#034)

#### Applied In
- All subsequent iterations: Zero secrets in code
- Added pre-commit hook to catch violations

---

## ⚡ Performance Learnings

### #028: Profile Before Optimizing âœ…
**Date:** 2025-11-17 | **Iteration:** 2 | **Agent:** Feature Developer  
**Impact:** High | **Reusability:** Universal

#### Context
API endpoint was slow (1.2s response time). Team wanted to optimize.

#### What Happened
Initial instinct was to optimize database queries. Profiling revealed actual bottleneck was JSON serialization (800ms of 1200ms).

#### Learning
Always profile to find actual bottlenecks before optimizing.

#### Pattern to Follow âœ…
```python
# Use profiling to find bottlenecks
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
result = slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest
```

Or use decorators:
```python
import time
from functools import wraps

def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}: {end - start:.4f}s")
        return result
    return wrapper

@profile
def process_data(data):
    # Your code
    pass
```

**Before profiling:** Optimized wrong thing, wasted 3 hours  
**After profiling:** Fixed real issue in 30 minutes, 67% improvement

#### When to Apply
- Before any optimization work
- When users report slow performance
- During performance iteration

#### Related Learnings
- [#029: Optimize Hot Paths First](#029)
- [#030: Cache Expensive Operations](#030)

---

## 🧪 Testing Learnings

### #042: Write Tests Before Fixing Bugs âœ…
**Date:** 2025-11-18 | **Iteration:** 2 | **Agent:** QA Engineer  
**Impact:** High | **Reusability:** Universal

#### Context
Bug reported: User deletion fails when user has active sessions.

#### What Happened
Developer fixed bug, marked as resolved. Bug reappeared 2 weeks later—fix was incomplete.

#### Learning
Write a failing test FIRST, then fix bug, then verify test passes.

#### Pattern to Follow âœ…
```python
# Step 1: Write test that reproduces bug (should FAIL)
def test_user_deletion_with_active_sessions():
    """Bug #123: User deletion should cascade to sessions"""
    user = create_user()
    session = create_session(user)
    
    delete_user(user)
    
    # This should not raise an error
    assert not user_exists(user.id)
    assert not session_exists(session.id)  # BUG: This fails
```

```python
# Step 2: Fix the bug
def delete_user(user):
    # Delete sessions FIRST
    Session.objects.filter(user=user).delete()
    # Then delete user
    user.delete()
```

```python
# Step 3: Verify test now PASSES
# Run: pytest test_users.py::test_user_deletion_with_active_sessions
# Result: PASSED ✅
```

**Benefits:**
- Confirms bug is really fixed
- Prevents regression
- Documents the bug
- Forces understanding of root cause

#### When to Apply
- EVERY bug fix
- During QA phase
- Before merging PR

#### Applied In
- Iteration 3: Zero bug regressions (vs 3 in It.1)
- All bugs now have test coverage

---

## ðŸ"— Integration Learnings

### #056: Use Stub Implementations to Unblock âœ…
**Date:** 2025-11-16 | **Iteration:** 1 | **Agent:** Coordination  
**Impact:** High | **Reusability:** Universal

#### Context
Feature agent blocked waiting for Backend agent to finish API.

#### What Happened
Feature agent waited 2 hours for backend. Lost productivity.

#### Learning
Create stub/mock implementations to unblock dependent work.

#### Pattern to Follow âœ…
```python
# Backend creates stub FIRST (5 minutes)
# core/storage/stub_storage.py
class StubStorage:
    """Stub implementation for development"""
    
    def save(self, key: str, value: dict) -> bool:
        print(f"STUB: Would save {key}")
        return True  # Always succeeds
    
    def load(self, key: str) -> Optional[dict]:
        print(f"STUB: Would load {key}")
        return {"mock": "data"}  # Return mock data
```

```python
# Feature agent uses stub immediately
from core.storage.stub_storage import StubStorage

storage = StubStorage()  # Use stub during development
result = storage.save("user:123", user_data)
```

```python
# Backend implements real version in parallel
# core/storage/file_storage.py
class FileStorage:
    def save(self, key: str, value: dict) -> bool:
        # Real implementation
        with open(f"{key}.json", 'w') as f:
            json.dump(value, f)
        return True
```

```python
# Feature agent swaps to real when ready
from core.storage.file_storage import FileStorage

storage = FileStorage()  # Swap to real implementation
```

**Benefits:**
- No blocking between agents
- Feature agent tests logic independently
- Backend agent has clear interface to implement
- Easy to swap implementations

**Time Saved:** 2 hours per agent = 10 hours total per iteration

#### When to Apply
- Start of Phase 4 (parallel work)
- Whenever one agent depends on another
- During API design phase

#### Applied In
- Iteration 2: Zero blocking issues (vs 3 blocks in It.1)
- All agents productive from hour 1

---

## 📝 Communication Learnings

### #068: Daily Logs > Real-Time Chat âœ…
**Date:** 2025-11-17 | **Iteration:** 2 | **Agent:** Coordination  
**Impact:** Medium | **Reusability:** Universal

#### Context
Tried real-time coordination between 5 agents via chat/messaging.

#### What Happened
Constant interruptions, context switching, lost focus. Overhead outweighed benefits.

#### Learning
Asynchronous daily logs work better than synchronous chat for agent coordination.

#### Pattern to Follow âœ…
Each agent posts to daily log:

```markdown
# DAILY_LOGS/2025-11-17.md

## Agent 1: Backend Engineer
**Status:** ðŸŸ¢ On Track
**Completed:**
- âœ… Implemented FileStorage backend
- âœ… Added connection pooling
- âœ… Unit tests passing (28/28)

**In Progress:**
- ðŸŸ¡ Database migration system (60% done)

**Blocked:**
- None

**Next:**
- Complete migration system
- Integration testing with Agent 2

**Questions:**
- Should migrations be reversible? @Agent2

**Files:**
- `core/storage/file_storage.py`
- `core/db/migrations.py`

---

## Agent 2: Feature Developer
**Status:** ðŸŸ¢ On Track
**Completed:**
- âœ… Auth feature using StorageBackend interface
- âœ… JWT token generation
- âœ… Password hashing

**In Progress:**
- ðŸŸ¡ Session management (40% done)

**Blocked:**
- None (using stub storage)

**Next:**
- Complete session management
- Swap to real storage when ready

**Answers:**
- @Agent1: Yes, migrations should be reversible (rollback safety)

**Files:**
- `features/auth/service.py`
- `features/auth/models.py`
```

**Benefits:**
- No interruptions during deep work
- Clear audit trail
- Easy to catch up after absence
- Searchable history

**Daily Log vs Real-Time:**
- Focus time: 5.5h vs 3.2h (72% more productive)
- Context switches: 2 vs 18 (90% reduction)

#### When to Apply
- Phase 4 (parallel agents)
- Any multi-agent collaboration
- When async > sync

---

## ðŸ› ï¸ Tooling Learnings

### #079: Automate Metrics Collection âœ…
**Date:** 2025-11-18 | **Iteration:** 3 | **Agent:** QA Engineer  
**Impact:** Medium | **Reusability:** Universal

#### Context
Manually collecting coverage, complexity, security metrics took 45 minutes.

#### What Happened
Created automated script. Now takes 2 minutes.

#### Learning
Automate repetitive metrics collection with scripts.

#### Pattern to Follow âœ…
```python
# scripts/collect_metrics.py
import json
import subprocess
from pathlib import Path

def main():
    print("📊 Collecting metrics...")
    
    metrics = {
        "coverage": collect_coverage(),
        "complexity": collect_complexity(),
        "security": collect_security(),
        "lint": collect_lint_issues(),
    }
    
    output = Path("METRICS/raw/latest.json")
    output.parent.mkdir(exist_ok=True, parents=True)
    output.write_text(json.dumps(metrics, indent=2))
    
    print(f"✅ Metrics saved to {output}")
    generate_report(metrics)

def collect_coverage():
    subprocess.run(["pytest", "--cov=.", "--cov-report=json"])
    with open(".coverage.json") as f:
        data = json.load(f)
    return data["totals"]["percent_covered"]

def collect_complexity():
    result = subprocess.run(
        ["radon", "cc", ".", "-a", "-j"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

if __name__ == "__main__":
    main()
```

Add to workflow:
```bash
# After iteration
python scripts/collect_metrics.py
python scripts/update_dashboard.py
```

**Before:** 45 min manual work  
**After:** 2 min automated

#### When to Apply
- End of each iteration
- After major changes
- As part of CI/CD

---

## ðŸ"¤ By Agent Role

### Backend Engineer - Top Learnings
1. [#001: Separate Core from Features](#001)
2. [#002: Define APIs Before Implementation](#002)
3. [#028: Profile Before Optimizing](#028)
4. [Use Connection Pooling](#connection-pooling)
5. [Implement Circuit Breakers](#circuit-breakers)

### Feature Developer - Top Learnings
1. [#042: Write Tests Before Fixing Bugs](#042)
2. [#056: Use Stub Implementations](#056)
3. [Validate at Boundaries](#validate-boundaries)
4. [Handle Edge Cases](#edge-cases)

### QA Engineer - Top Learnings
1. [#042: Write Tests Before Fixing Bugs](#042)
2. [Test Critical Paths First](#critical-paths)
3. [#079: Automate Metrics](#079)
4. [Mock External Dependencies](#mocking)

### Interface Engineer - Top Learnings
1. [User Input Validation](#input-validation)
2. [Progressive Enhancement](#progressive-enhancement)
3. [Accessibility from Start](#a11y)

### Technical Writer - Top Learnings
1. [Code Examples Must Run](#runnable-examples)
2. [Document the Why](#document-why)
3. [Keep Docs Near Code](#docs-location)

---

## 🔄 Learning Lifecycle

### 1. Capture (During Work)
Agents note learnings as they work:
```markdown
<!-- In PR description -->
## Learning
Using connection pooling reduced query time by 80%.
Pattern: Always pool DB connections.
```

### 2. Review (End of Phase)
After Phase 5 (Integration):
- Review all PR descriptions
- Extract learnings
- Categorize and document

### 3. Consolidate (Post-Iteration)
After Phase 5.5 (Quality Audit):
- Add to ITERATION_N_LEARNINGS.md
- Update role-specific files
- Add to MASTER_LEARNINGS.md

### 4. Apply (Next Iteration)
Before Phase 4 (Launch Agents):
- Agents read relevant learnings
- Incorporate into prompts
- Reference in code reviews

### 5. Measure (Metrics)
Track learning application:
- How many learnings applied?
- Did they improve outcomes?
- Any learnings invalidated?

---

## ðŸ'¡ How to Use This System

### For Agents During Work (Phase 4)

**Before Starting:**
```markdown
1. Read MASTER_LEARNINGS.md
2. Read your role-specific learnings (e.g., BACKEND_ENGINEER.md)
3. Note any learnings relevant to your current task
4. Reference them during implementation
```

**While Working:**
```markdown
1. When you discover something useful, note it
2. When you make a mistake, document it
3. When you solve a tricky problem, capture the solution
4. Add to PR description under "## Learnings"
```

**After Completing:**
```markdown
1. Review what you learned
2. Document significant patterns
3. Flag for inclusion in master learnings
```

### For Coordination (Phase 5/5.5)

**During Integration:**
```markdown
1. Review all PR learnings
2. Extract common themes
3. Identify high-impact patterns
4. Note integration issues for learning
```

**During Quality Audit:**
```markdown
1. Document issues as learnings
2. Capture effective solutions
3. Note what should be avoided
4. Update master learnings
```

### For Next Iteration (Phase 3/6)

**When Planning:**
```markdown
1. Review last iteration's learnings
2. Incorporate into agent prompts
3. Set targets based on learnings
4. Flag applicable patterns for agents
```

---

## 📊 Learning Metrics

Track learning effectiveness:

```markdown
# LEARNING_METRICS.md

## Iteration 2 Learning Impact

### Learnings Applied
- Total learnings available: 23
- Learnings applied this iteration: 15 (65%)
- New learnings captured: 8

### Impact Measurement
| Learning | Applied | Time Saved | Quality Impact |
|----------|---------|------------|----------------|
| #001: Core/Feature Separation | Yes | 2h | +15% |
| #002: API-First Design | Yes | 3h | No conflicts |
| #028: Profile First | Yes | 1.5h | +40% perf |
| #042: Test Before Fix | Yes | 0h | 0 regressions |
| #056: Use Stubs | Yes | 10h | Unblocked all |

**Total Time Saved:** 16.5 hours  
**Total Quality Improvement:** +55% across metrics
```

---

## 🌍 Cross-Project Learning

### UNIVERSAL_PATTERNS.md Template
Extract learnings that apply to ALL projects:

```markdown
# Universal Patterns
**Learnings that work across all projects**

## Architecture
1. âœ… Separate core from features
2. âœ… Define interfaces before implementation
3. âœ… Use dependency injection
4. âœ… Single Responsibility Principle
5. âœ… Fail fast, validate early

## Security
1. âœ… Never store secrets in code
2. âœ… Validate all inputs
3. âœ… Use parameterized queries
4. âœ… Principle of least privilege
5. âœ… Log security events

## Performance
1. âœ… Profile before optimizing
2. âœ… Cache expensive operations
3. âœ… Use connection pooling
4. âœ… Lazy load when possible
5. âœ… Optimize hot paths first

## Testing
1. âœ… Write tests before fixing bugs
2. âœ… Test critical paths first
3. âœ… Mock external dependencies
4. âœ… Aim for 70-80% coverage minimum
5. âœ… Integration tests catch more bugs

## Coordination
1. âœ… Async logs > sync chat
2. âœ… Define APIs before coding
3. âœ… Use stubs to unblock
4. âœ… Daily status updates
5. âœ… Document decisions
```

---

## ðŸš€ Quick Start

### Initial Setup
```bash
# Create structure
mkdir -p AGENT_LEARNINGS/{BY_ROLE,BY_CATEGORY,BY_LANGUAGE}
mkdir -p CROSS_PROJECT_LEARNINGS

# Create initial files
touch AGENT_LEARNINGS/MASTER_LEARNINGS.md
touch AGENT_LEARNINGS/ITERATION_1_LEARNINGS.md
touch CROSS_PROJECT_LEARNINGS/UNIVERSAL_PATTERNS.md
```

### After Each Iteration
```bash
# 1. Extract learnings from PRs
grep -A 10 "## Learning" pull_requests/*.md > learnings.txt

# 2. Document in iteration file
vim AGENT_LEARNINGS/ITERATION_N_LEARNINGS.md

# 3. Update master learnings
cat AGENT_LEARNINGS/ITERATION_N_LEARNINGS.md >> AGENT_LEARNINGS/MASTER_LEARNINGS.md

# 4. Update role-specific learnings
# Manually sort by role
```

### Before Next Iteration
```bash
# Agents read relevant learnings
cat AGENT_LEARNINGS/BY_ROLE/BACKEND_ENGINEER.md
cat AGENT_LEARNINGS/BY_CATEGORY/SECURITY.md

# Update agent prompts with top learnings
vim AGENT_PROMPTS/1_backend.md
# Add: "Reference AGENT_LEARNINGS/BY_ROLE/BACKEND_ENGINEER.md"
```

---

## 📈 Success Metrics

This system is successful when:
- âœ… Agents reference learnings in their work
- âœ… Same mistakes aren't repeated across iterations
- âœ… Time to complete iterations decreases
- âœ… Quality metrics improve iteration over iteration
- âœ… New projects start with accumulated knowledge

**Target:** 60%+ of learnings applied in subsequent iterations

---

**Version:** 1.0  
**Last Updated:** November 17, 2025  
**Part of:** Multi-Agent Self-Improving Workflow System
