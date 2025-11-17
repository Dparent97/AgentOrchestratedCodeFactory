# Multi-Agent Coordination Plan

**Project**: Agent-Orchestrated Code Factory
**Date**: 2025-11-17
**Coordinator**: Project Lead
**Agents**: 5 specialized development agents

---

## 📋 Overview

This document coordinates the work of 5 specialized AI agents working in parallel to accelerate the development of the Code Factory project. Each agent has a specific role, branch, and set of deliverables.

## 👥 Agent Team

### Agent 1: Backend Infrastructure Engineer
- **Branch**: `backend-core-infrastructure`
- **Focus**: Orchestrator, runtime, state management
- **Files**: `src/code_factory/core/`
- **Priority**: CRITICAL - Foundation for all other work
- **Dependencies**: None (starts immediately)
- **Estimated Time**: 10-15 hours

### Agent 2: LLM Integration Specialist
- **Branch**: `llm-integration`
- **Focus**: Claude/OpenAI integration, prompt engineering
- **Files**: `src/code_factory/llm/` (new)
- **Priority**: CRITICAL - Enables intelligent agents
- **Dependencies**: Lightweight (can start with Agent 1)
- **Estimated Time**: 15-20 hours

### Agent 3: Agent Implementation Developer
- **Branch**: `agent-implementations`
- **Focus**: Complete remaining 5 agents
- **Files**: `src/code_factory/agents/`
- **Priority**: HIGH - Enables end-to-end functionality
- **Dependencies**: Agent 2 (LLM client)
- **Estimated Time**: 12-18 hours

### Agent 4: Testing & Quality Engineer
- **Branch**: `testing-infrastructure`
- **Focus**: Comprehensive tests, CI/CD
- **Files**: `tests/`, `.github/workflows/`
- **Priority**: HIGH - Ensures reliability
- **Dependencies**: Agents 1, 2, 3 (needs working code)
- **Estimated Time**: 18-24 hours

### Agent 5: Templates & Documentation Specialist
- **Branch**: `templates-and-docs`
- **Focus**: Blue-collar templates, tutorials, examples
- **Files**: `templates/`, `examples/`, `docs/`
- **Priority**: MEDIUM - Delivers user value
- **Dependencies**: Agents 1, 2, 3 (needs working factory)
- **Estimated Time**: 20-30 hours

---

## 🔄 Integration Points

### Backend → LLM Integration
- **Interface**: Agent 2 uses Agent 1's `AgentRuntime`
- **Status**: ✅ Compatible (minimal coupling)
- **Integration**: Agent 2 registers agents with runtime

### LLM → Agent Implementation
- **Interface**: Agent 3 uses `LLMClient` and `PromptLibrary` from Agent 2
- **Status**: 🔄 Sequential dependency
- **Integration**: Agent 3 imports from `code_factory.llm.client`

### Backend + LLM + Agents → Testing
- **Interface**: Agent 4 tests all modules from Agents 1, 2, 3
- **Status**: 🔄 Must wait for implementations
- **Integration**: Agent 4 imports and tests everything

### All → Templates
- **Interface**: Agent 5 uses complete working factory
- **Status**: 🔄 Must wait for Agents 1, 2, 3
- **Integration**: Agent 5 runs factory to generate examples

---

## 📊 Dependency Graph

```
┌─────────────────────────────────────────────────────┐
│                    START                            │
└─────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   Agent 1    │        │   Agent 2    │
│   Backend    │        │   LLM        │
│ (No deps)    │        │ (Lightweight)│
└──────────────┘        └──────────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
            ┌──────────────┐
            │   Agent 3    │
            │  Agents      │
            │ (Needs 2)    │
            └──────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   Agent 4    │        │   Agent 5    │
│  Testing     │        │ Templates    │
│(Needs 1,2,3) │        │(Needs 1,2,3) │
└──────────────┘        └──────────────┘
```

---

## 📅 Phase Breakdown

### Phase 1: Foundation (Week 1-2)
**Agents Working**: 1, 2 (in parallel)

**Goals**:
- [ ] Complete orchestrator pipeline (Agent 1)
- [ ] LLM client infrastructure (Agent 2)
- [ ] 3 core agents with LLM (Agent 2: SafetyGuard, PlannerAgent, ArchitectAgent)

**Merge Criteria**:
- Tests pass
- Code reviewed
- No breaking changes
- Documentation updated

**Deliverables**:
- Working orchestrator
- LLM client
- 3 intelligent agents

---

### Phase 2: Agent Implementation (Week 2-3)
**Agents Working**: 3, (1 and 2 polish)

**Goals**:
- [ ] Complete TesterAgent, DocWriterAgent, GitOpsAgent (Agent 3)
- [ ] Enhance BlueCollarAdvisor (Agent 3)
- [ ] Bug fixes from Phase 1

**Merge Criteria**:
- All agents work independently
- Integration test passes
- No regressions

**Deliverables**:
- 8 fully functional agents
- Working end-to-end pipeline

---

### Phase 3: Quality & Testing (Week 3-4)
**Agents Working**: 4

**Goals**:
- [ ] Comprehensive unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] E2E test generates real project
- [ ] CI/CD pipeline configured

**Merge Criteria**:
- All tests pass
- Coverage ≥ 80%
- CI configured and passing
- No flaky tests

**Deliverables**:
- Complete test suite
- GitHub Actions CI/CD
- Quality gates

---

### Phase 4: Templates & Documentation (Week 4-5)
**Agents Working**: 5

**Goals**:
- [ ] 5 blue-collar templates
- [ ] 3 example projects
- [ ] User tutorials
- [ ] API reference
- [ ] Contributing guide

**Merge Criteria**:
- Templates generate working code
- Examples tested
- Documentation reviewed
- No errors or typos

**Deliverables**:
- Template library
- Example projects
- Complete documentation

---

## 🔧 Integration Checklist

Before merging any branch, verify:

### Agent 1 (Backend)
- [ ] `Orchestrator.run_factory()` executes all 8 stages
- [ ] State management works
- [ ] Error handling complete
- [ ] Integration test passes
- [ ] No TODO comments remaining

### Agent 2 (LLM)
- [ ] LLMClient works with Claude API
- [ ] All 8 agent prompts written
- [ ] SafetyGuard, PlannerAgent, ArchitectAgent use LLM
- [ ] Token tracking implemented
- [ ] Unit tests pass

### Agent 3 (Agents)
- [ ] TesterAgent generates and runs tests
- [ ] DocWriterAgent creates documentation
- [ ] GitOpsAgent initializes repos
- [ ] BlueCollarAdvisor provides feedback
- [ ] All agents tested individually

### Agent 4 (Testing)
- [ ] 80%+ code coverage achieved
- [ ] Integration tests pass
- [ ] E2E test generates project
- [ ] CI/CD configured
- [ ] Pre-commit hooks work

### Agent 5 (Templates)
- [ ] 5 templates created
- [ ] Templates generate working code
- [ ] 3 example projects work
- [ ] Tutorials complete
- [ ] API reference accurate

---

## 📝 Daily Coordination

### Daily Logs Location
`AGENT_PROMPTS/daily_logs/YYYY-MM-DD_[agent_name].md`

### Log Format
```markdown
## [Agent Name] - [Date]

### Completed Today
- Implemented StateManager class
- Added unit tests for orchestrator
- Fixed bug in agent registration

### In Progress
- Working on error handling
- Testing integration with LLM

### Blockers
- Waiting for LLM client from Agent 2
- Need clarification on state persistence format

### Next Steps
- Complete error recovery
- Write integration tests
- Update documentation

### Questions
- Should state be JSON or SQLite?
- What's the timeout for LLM calls?
```

### Review Schedule
- **Daily**: Check logs for blockers
- **Weekly**: Integration meeting (async via logs)
- **Per Phase**: Merge and integration testing

---

## 🚨 Blockers & Resolution

### Current Blockers
None - Phase 1 starting

### Resolution Process
1. **Post Blocker**: Agent posts in `AGENT_PROMPTS/issues/blocker_[topic].md`
2. **Notify**: Coordinator reviews daily
3. **Resolve**: Answer questions, provide clarification, or adjust plan
4. **Update Status**: Mark as resolved in coordination doc

### Common Blocker Types
- **API Unavailable**: Agent depends on unfinished work
  - Solution: Create stub/mock, or adjust timeline
- **Unclear Spec**: Integration point not defined
  - Solution: Clarify in COORDINATION.md
- **Conflicting Changes**: Two agents modify same file
  - Solution: Coordinate via issues/, adjust file ownership

---

## 🔀 Merge Strategy

### Merge Order (Important!)
1. **Agent 1** (Backend) - Merge first
2. **Agent 2** (LLM) - Merge second (depends lightly on Agent 1)
3. **Agent 3** (Agents) - Merge third (depends on Agent 2)
4. **Agent 4** (Testing) - Merge fourth (tests everything)
5. **Agent 5** (Templates) - Merge last (uses everything)

### Before Merging
1. Run all tests: `pytest tests/ -v`
2. Check code style: `black src/ && ruff check src/`
3. Verify no TODOs: `grep -r "TODO" src/`
4. Update CHANGELOG
5. Get coordinator approval

### Merge Command
```bash
git checkout main
git pull origin main
git merge --no-ff [branch-name]
git push origin main
```

---

## 💰 Budget & Timeline

### Total Estimated Effort
- Agent 1: 10-15 hours
- Agent 2: 15-20 hours
- Agent 3: 12-18 hours
- Agent 4: 18-24 hours
- Agent 5: 20-30 hours
- **Total**: 75-107 hours

### Timeline (Part-Time, 2-3 hrs/day)
- **Phase 1**: Weeks 1-2 (Foundation)
- **Phase 2**: Weeks 2-3 (Agents)
- **Phase 3**: Weeks 3-4 (Testing)
- **Phase 4**: Weeks 4-5 (Templates)
- **Total**: 4-6 weeks

### Budget (Claude Code Credits)
- Starting: $931 credits
- Estimated usage: $100-200 (depending on agent efficiency)
- Buffer: $731-831 remaining

---

## ✅ Success Metrics

### Phase 1 Complete When:
- [ ] Orchestrator runs all 8 stages
- [ ] LLM client works
- [ ] 3 agents use LLM
- [ ] Basic integration test passes

### Phase 2 Complete When:
- [ ] All 8 agents implemented
- [ ] End-to-end pipeline works
- [ ] Can generate a simple project

### Phase 3 Complete When:
- [ ] 80%+ code coverage
- [ ] CI/CD passing
- [ ] No failing tests

### Phase 4 Complete When:
- [ ] 5 templates ready
- [ ] 3 examples working
- [ ] Documentation complete

### Project Complete When:
- [ ] All phases done
- [ ] Can generate real blue-collar tools
- [ ] Documentation complete
- [ ] Ready for users

---

## 📞 Communication Channels

- **Daily Updates**: `AGENT_PROMPTS/daily_logs/`
- **Questions**: `AGENT_PROMPTS/questions.md`
- **Blockers**: `AGENT_PROMPTS/issues/`
- **Decisions**: Document in this file
- **Code Reviews**: Git commit comments

---

## 🎯 Key Decisions

### Decision Log
| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| 2025-11-17 | Use Claude as primary LLM | Better code quality than GPT-4 | Agent 2 |
| 2025-11-17 | JSON for state (not SQLite) | Simpler, human-readable | Agent 1 |
| 2025-11-17 | pytest for all tests | Industry standard, rich ecosystem | Agent 4 |

---

**Last Updated**: 2025-11-17
**Next Review**: After Phase 1 completion

---

## Quick Reference

**Agent 1**: backend-core-infrastructure → core/
**Agent 2**: llm-integration → llm/
**Agent 3**: agent-implementations → agents/
**Agent 4**: testing-infrastructure → tests/
**Agent 5**: templates-and-docs → templates/, examples/, docs/

**Merge Order**: 1 → 2 → 3 → 4 → 5

**Communication**: Daily logs in `AGENT_PROMPTS/daily_logs/`
