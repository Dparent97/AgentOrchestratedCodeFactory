# Agent Questions & Answers

This file serves as the central Q&A thread for all agents working on the project.

**How to Use**:
1. Agents post questions here
2. Other agents or coordinator answer
3. Keep format consistent
4. Mark as resolved when answered

---

## Template

```markdown
## [Agent Name] - [Date]
**Question**: [Your question here]

**Context**: [Background information, why you need to know]

**Blocking**: [Yes/No - is this blocking your progress?]

**Priority**: [High/Medium/Low]

---

### Answer ([Responder Name] - [Date])
[Answer here]

**References**: [Links to relevant docs, code, or files]

**Status**: ✅ Resolved / 🔄 Needs Discussion / ❌ Blocked
```

---

## Current Questions

<!-- Post your questions below this line -->

---

## Resolved Questions

<!-- Move answered questions here -->

### Example Question (Resolved)

## Backend Engineer - 2025-11-17
**Question**: Should pipeline state be persisted to JSON or SQLite?

**Context**: Implementing StateManager class for orchestrator. Need to store intermediate results and allow resume after failure.

**Blocking**: No, but affects design decisions

**Priority**: Medium

---

### Answer (Coordinator - 2025-11-17)
Use JSON for now. Reasons:
1. Simpler implementation
2. Human-readable for debugging
3. No additional dependencies
4. Sufficient for single-instance usage

Future consideration: If we need concurrent access or complex queries, migrate to SQLite.

**References**:
- State management pattern: `src/code_factory/core/state_manager.py`
- Example: See orchestrator checkpoint logic

**Status**: ✅ Resolved

---

<!-- Add your questions below -->
