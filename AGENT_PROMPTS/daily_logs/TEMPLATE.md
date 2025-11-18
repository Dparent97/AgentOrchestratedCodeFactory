# Daily Log Template

**Copy this template for each day's log:** `YYYY-MM-DD.md`

---

## [Agent Name] - [Date]

### Completed Today
- ✅ [Specific accomplishment with file/function names]
- ✅ [Specific accomplishment]
- ✅ [Specific accomplishment]

### In Progress
- 🔄 [Current task, % complete if applicable]
- 🔄 [Current task]

### Blockers
[List blockers or write "None"]
- ❌ [Blocker description, who can help]

### Questions
[Tag other agents with questions or write "None"]
- @[Agent-Name]: [Question]

### Next Steps
- [ ] [Tomorrow's first task]
- [ ] [Tomorrow's second task]
- [ ] [Tomorrow's third task]

### Metrics (if applicable)
- Test Coverage: [X]%
- Files Changed: [N]
- Tests Written: [N]
- Lines of Code: +[N]

---

## Example Daily Log

```markdown
## Agent Foundation Developer - 2025-11-18

### Completed Today
- ✅ Implemented PlanResult model in core/models.py
- ✅ Created PlannerAgent.execute() skeleton in agents/planner.py
- ✅ Wrote first 5 unit tests in tests/unit/test_planner.py

### In Progress
- 🔄 Implementing task decomposition logic (60% complete)
- 🔄 Building dependency graph generation

### Blockers
None

### Questions
@QA-Engineer: Should PlannerAgent raise ValueError for vague ideas or generate minimal task list?

### Next Steps
- [ ] Complete task decomposition algorithm
- [ ] Implement complexity estimation
- [ ] Reach 15 unit tests by EOD tomorrow
- [ ] Achieve 80% test coverage

### Metrics
- Test Coverage: 65% (need 80%)
- Files Changed: 3
- Tests Written: 5
- Lines of Code: +245
```
