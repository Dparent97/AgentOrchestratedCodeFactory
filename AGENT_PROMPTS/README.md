# Agent Coordination Center

**Project**: Agent-Orchestrated Code Factory
**Approach**: Multi-Agent Development (5 specialized agents)
**Current Phase**: Phase 1 - Backend Infrastructure Setup

---

## Quick Navigation

- **[MULTI_AGENT_KICKSTART_SUMMARY.md](../MULTI_AGENT_KICKSTART_SUMMARY.md)** - Agent 1 role and tasks (START HERE!)
- **[COORDINATION.md](COORDINATION.md)** - Integration points and dependencies
- **[questions.md](questions.md)** - Q&A between agents
- **[daily_logs/](daily_logs/)** - Progress tracking
- **[issues/](issues/)** - Technical decisions and problems

---

## The 5-Agent Team

### 🔧 Agent 1: Backend Infrastructure Engineer (ACTIVE NOW!)
**Status**: 🔄 In Progress
**Focus**: Core orchestration, runtime, file utilities
**Files**: `src/code_factory/core/*`
**See**: [MULTI_AGENT_KICKSTART_SUMMARY.md](../MULTI_AGENT_KICKSTART_SUMMARY.md)

### 🤖 Agent 2: Agent Implementation Specialist
**Status**: ⏸️ Blocked (waiting for Agent 1)
**Focus**: Implement all 8 specialized agents
**Files**: `src/code_factory/agents/*`

### 💻 Agent 3: CLI/Interface Engineer
**Status**: ⏸️ Blocked (waiting for Agents 1 & 2)
**Focus**: Command-line interface and user experience
**Files**: `src/code_factory/cli/*`

### 🧪 Agent 4: QA/Testing Engineer
**Status**: ⏸️ Blocked (waiting for implementations)
**Focus**: Comprehensive testing and quality assurance
**Files**: `tests/*`

### 📝 Agent 5: Technical Writer
**Status**: ⏸️ Blocked (waiting for features)
**Focus**: Documentation, examples, guides
**Files**: `docs/*`, `README.md`

---

## Current Phase: Foundation

**Goal**: Build the core infrastructure that all other agents depend on

**Active Work**:
- Agent 1 is implementing the complete orchestration pipeline
- Other agents are waiting for foundational APIs

**Phase 1 Complete When**:
- [ ] Orchestrator.run_factory() works end-to-end
- [ ] File utilities created and tested
- [ ] Logging system configured
- [ ] Error handling implemented
- [ ] 80%+ test coverage
- [ ] Code committed and pushed

---

## How This Works

### 1. Agent 1 (Backend) - Builds Foundation
- Creates core APIs and infrastructure
- No dependencies - starts immediately
- Provides APIs for other agents

### 2. Agent 2 (Agents) - Implements Intelligence
- Uses Agent 1's runtime and orchestrator
- Implements all 8 specialized agents
- Provides complete agent system

### 3. Agent 3 (CLI) - Builds Interface
- Uses Agent 1's orchestrator + Agent 2's agents
- Creates user-facing commands
- Provides CLI for end users

### 4. Agent 4 (QA) - Ensures Quality
- Tests all code from Agents 1, 2, 3
- Ensures 80%+ coverage
- Prevents regressions

### 5. Agent 5 (Docs) - Documents Everything
- Documents all features
- Creates examples and guides
- Ensures users can actually use the system

---

## Coordination Mechanisms

### Daily Progress Logs
Every agent posts updates to `daily_logs/YYYY-MM-DD.md`:
- What was completed
- What's in progress
- Any blockers
- Next steps

**Format**: See [MULTI_AGENT_WORKFLOW_GUIDE.md](../MULTI_AGENT_WORKFLOW_GUIDE.md)

### Questions & Answers
For cross-agent questions, use `questions.md`:
- Ask clear, specific questions
- Mark if blocking
- Other agents answer
- Archive when resolved

### Integration Points
`COORDINATION.md` defines:
- What each agent provides to others
- API contracts
- Dependencies
- File ownership

---

## Git Workflow

**Current Branch**: `claude/backend-infrastructure-setup-019sQjcXLBdXcRx854o6WQo4`

**Commit Requirements**:
- Clear, descriptive messages
- Tests must pass
- Documentation updated
- No secrets in code

**Push Strategy**:
- Agent 1 will push when Phase 1 complete
- Other agents will work on feature branches
- All code reviewed before merge to main

---

## Success Metrics

### Phase 1 (Current)
- Backend infrastructure complete and tested
- Other agents unblocked

### Phase 2 (Next)
- All 8 agents fully implemented
- End-to-end project generation works

### Phase 3 (Future)
- Complete CLI with all commands
- Full documentation
- Example projects generated

---

## Getting Started as Agent 1

### 1. Read Your Role
Open [MULTI_AGENT_KICKSTART_SUMMARY.md](../MULTI_AGENT_KICKSTART_SUMMARY.md)
- Your complete task list
- What you're building
- Who depends on you

### 2. Review Current Code
```bash
# Read the skeleton implementations:
cat src/code_factory/core/orchestrator.py
cat src/code_factory/core/agent_runtime.py
cat src/code_factory/core/models.py
```

### 3. Check TODO List
9 tasks tracked in todo list:
1. Implement Orchestrator.run_factory()
2. Create file_utils.py
3. Create logging_config.py
4. Implement error recovery
5-7. Write unit tests
8. Test end-to-end
9. Commit and push

### 4. Start Coding!
Begin with Task 1: Implement the full orchestration pipeline in `orchestrator.py`

---

## Communication Guidelines

### ✅ DO:
- Post daily progress logs
- Ask questions when blocked
- Update COORDINATION.md if APIs change
- Document design decisions
- Mark tasks in todo list

### ❌ DON'T:
- Edit files owned by other agents
- Skip documentation
- Commit without tests
- Leave TODOs unaddressed
- Forget to log progress

---

## Resources

- **[MULTI_AGENT_WORKFLOW_GUIDE.md](../MULTI_AGENT_WORKFLOW_GUIDE.md)** - The meta-pattern
- **[PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md)** - Project mission and goals
- **[docs/architecture.md](../docs/architecture.md)** - System design
- **[docs/safety.md](../docs/safety.md)** - Safety guidelines
- **[STEP1_COMPLETE.md](../STEP1_COMPLETE.md)** - What's been built so far

---

## Need Help?

1. Check `questions.md` for similar questions
2. Review `COORDINATION.md` for integration details
3. Read the workflow guide for best practices
4. Post a new question if needed

---

**Let's build this! Agent 1, you're up! 🚀**
