# Multi-Agent Development Prompts

**Project**: Agent-Orchestrated Code Factory
**Approach**: 5 specialized AI agents working in parallel
**Status**: Ready to launch
**Date**: 2025-11-17

---

## 🎯 Quick Start

### For Coordinators

1. **Read** this README
2. **Review** `COORDINATION.md` for the master plan
3. **Check** `GIT_WORKFLOW.md` for Git procedures
4. **Launch** agents using prompts below
5. **Monitor** progress in `daily_logs/`

### For Agents

1. **Read** your assigned prompt file (1-5 below)
2. **Create** your feature branch
3. **Complete** your tasks
4. **Post** daily updates to `daily_logs/`
5. **Submit** for merge when done

---

## 👥 The Agent Team

### 🔧 Agent 1: Backend Infrastructure Engineer
**Prompt File**: `1_Backend_Infrastructure_Engineer.md`
**Branch**: `backend-core-infrastructure`
**Mission**: Build the foundational orchestration and runtime systems

**Key Tasks**:
- Complete `Orchestrator.run_factory()` pipeline
- Add state management system
- Enhance runtime with resource management
- Implement comprehensive logging
- Write integration tests

**Priority**: 🔴 CRITICAL - Foundation for all other work
**Timeline**: 10-15 hours (Week 1-2)
**Dependencies**: None (start immediately)

---

### 🤖 Agent 2: LLM Integration Specialist
**Prompt File**: `2_LLM_Integration_Specialist.md`
**Branch**: `llm-integration`
**Mission**: Integrate Claude/OpenAI APIs to power intelligent code generation

**Key Tasks**:
- Create `LLMClient` infrastructure
- Build prompt template library
- Integrate LLM into SafetyGuard, PlannerAgent, ArchitectAgent
- Add token tracking and cost estimation
- Implement streaming and error handling

**Priority**: 🔴 CRITICAL - Enables intelligent agents
**Timeline**: 15-20 hours (Week 1-2)
**Dependencies**: Lightweight (can start with Agent 1)

---

### ⚙️ Agent 3: Agent Implementation Developer
**Prompt File**: `3_Agent_Implementation_Developer.md`
**Branch**: `agent-implementations`
**Mission**: Complete the remaining 5 specialized agents

**Key Tasks**:
- Implement TesterAgent (test generation and execution)
- Implement DocWriterAgent (documentation generation)
- Implement GitOpsAgent (Git operations)
- Enhance BlueCollarAdvisor with LLM
- Complete ImplementerAgent (if needed)

**Priority**: 🟠 HIGH - Enables end-to-end functionality
**Timeline**: 12-18 hours (Week 2-3)
**Dependencies**: Agent 2 (needs LLMClient)

---

### 🧪 Agent 4: Testing & Quality Engineer
**Prompt File**: `4_Testing_Quality_Engineer.md`
**Branch**: `testing-infrastructure`
**Mission**: Build comprehensive test suite and CI/CD pipeline

**Key Tasks**:
- Create unit tests for all modules (80%+ coverage)
- Create shared test fixtures
- Write integration and E2E tests
- Set up GitHub Actions CI/CD
- Configure pre-commit hooks

**Priority**: 🟠 HIGH - Ensures reliability
**Timeline**: 18-24 hours (Week 3-4)
**Dependencies**: Agents 1, 2, 3 (needs working code to test)

---

### 📚 Agent 5: Templates & Documentation Specialist
**Prompt File**: `5_Templates_Documentation_Specialist.md`
**Branch**: `templates-and-docs`
**Mission**: Create template library and comprehensive documentation

**Key Tasks**:
- Build 5-10 blue-collar project templates
- Generate 3-5 example projects
- Write user tutorials
- Create API reference documentation
- Write contributing guide

**Priority**: 🟡 MEDIUM - Delivers user value
**Timeline**: 20-30 hours (Week 4-5)
**Dependencies**: Agents 1, 2, 3 (needs working factory)

---

## 📋 Coordination Files

### `COORDINATION.md`
**Purpose**: Master coordination plan
**Contains**:
- Agent roles and responsibilities
- Dependency graph
- Integration points
- Phase breakdown
- Merge strategy
- Success metrics

📖 [Read COORDINATION.md](./COORDINATION.md)

---

### `GIT_WORKFLOW.md`
**Purpose**: Git workflow and branch management
**Contains**:
- Branch structure
- Commit message conventions
- Merge procedures
- Conflict resolution
- Best practices

📖 [Read GIT_WORKFLOW.md](./GIT_WORKFLOW.md)

---

## 🚀 How to Launch an Agent

### Option 1: Using Claude Code Web Interface

1. Open Claude Code in browser
2. Load the project: `AgentOrchestratedCodeFactory`
3. Copy the entire agent prompt file
4. Paste into Claude Code chat
5. Say: "I'm ready to start. Please confirm you understand your role and begin with Task 1."

### Option 2: Using Claude Code CLI

```bash
# Start a new Claude Code session
claude-code start --project=/path/to/AgentOrchestratedCodeFactory

# Load the agent prompt
@file AGENT_PROMPTS/1_Backend_Infrastructure_Engineer.md

# Begin
"I'm ready to start on Agent 1: Backend Infrastructure Engineer. Please proceed with Task 1."
```

### Option 3: Copy-Paste Launch Prompts

Use these simplified prompts to start each agent:

#### 🚀 Launch Agent 1: Backend Infrastructure Engineer
```
I am Agent 1: Backend Infrastructure Engineer for the Agent-Orchestrated Code Factory project.

My mission: Build the foundational orchestration and runtime infrastructure.

Please read my complete role definition at:
AGENT_PROMPTS/1_Backend_Infrastructure_Engineer.md

I will work on branch: backend-core-infrastructure
My files: src/code_factory/core/

I'm ready to start with Task 1: Complete Orchestrator Pipeline.

Please confirm you understand the role and begin implementing the orchestrator.
```

#### 🚀 Launch Agent 2: LLM Integration Specialist
```
I am Agent 2: LLM Integration Specialist for the Agent-Orchestrated Code Factory project.

My mission: Integrate Claude/OpenAI APIs to power intelligent code generation.

Please read my complete role definition at:
AGENT_PROMPTS/2_LLM_Integration_Specialist.md

I will work on branch: llm-integration
My files: src/code_factory/llm/ (new directory)

I'm ready to start with Task 1: Create LLM Client Infrastructure.

Please confirm you understand the role and begin creating the LLM client.
```

#### 🚀 Launch Agent 3: Agent Implementation Developer
```
I am Agent 3: Agent Implementation Developer for the Agent-Orchestrated Code Factory project.

My mission: Complete the remaining 5 specialized agents using LLM infrastructure.

Please read my complete role definition at:
AGENT_PROMPTS/3_Agent_Implementation_Developer.md

I will work on branch: agent-implementations
My files: src/code_factory/agents/

First, verify that Agent 2 has completed the LLM client infrastructure.
Then start with Task 1: Implement TesterAgent.

Please confirm you understand the role and begin.
```

#### 🚀 Launch Agent 4: Testing & Quality Engineer
```
I am Agent 4: Testing & Quality Engineer for the Agent-Orchestrated Code Factory project.

My mission: Build comprehensive test suite and CI/CD pipeline.

Please read my complete role definition at:
AGENT_PROMPTS/4_Testing_Quality_Engineer.md

I will work on branch: testing-infrastructure
My files: tests/, .github/workflows/

Wait for Agents 1, 2, and 3 to complete their work first.
Then start with Task 2: Create Shared Test Fixtures.

Please confirm you understand the role and begin.
```

#### 🚀 Launch Agent 5: Templates & Documentation Specialist
```
I am Agent 5: Templates & Documentation Specialist for the Agent-Orchestrated Code Factory project.

My mission: Create template library and comprehensive documentation.

Please read my complete role definition at:
AGENT_PROMPTS/5_Templates_Documentation_Specialist.md

I will work on branch: templates-and-docs
My files: templates/, examples/, docs/

Wait for Agents 1, 2, and 3 to complete their work first.
Then start with Task 1: Create Blue-Collar Template Library.

Please confirm you understand the role and begin.
```

---

## 📊 Progress Tracking

### Daily Logs

Each agent should post daily progress logs:

**Location**: `AGENT_PROMPTS/daily_logs/YYYY-MM-DD_[agent_name].md`

**Format**:
```markdown
## [Agent Name] - [Date]

### Completed Today
- Implemented feature X
- Fixed bug Y
- Added tests for Z

### In Progress
- Working on feature A (70% complete)

### Blockers
- Waiting for API from Agent 2
- Question about state persistence format

### Next Steps
- Complete feature A
- Start feature B
- Update documentation

### Questions
- Should I use JSON or SQLite for state?
```

### Checking Progress

Coordinator can check progress:
```bash
# View all daily logs
ls -lt AGENT_PROMPTS/daily_logs/

# Check latest log for Agent 1
cat AGENT_PROMPTS/daily_logs/$(ls -t AGENT_PROMPTS/daily_logs/*backend* | head -1)
```

---

## 🔄 Phases & Milestones

### Phase 1: Foundation (Week 1-2)
**Agents**: 1, 2
**Goal**: Working orchestrator + LLM integration
**Success**: 3 intelligent agents operational

### Phase 2: Agents (Week 2-3)
**Agents**: 3
**Goal**: All 8 agents implemented
**Success**: End-to-end pipeline works

### Phase 3: Quality (Week 3-4)
**Agents**: 4
**Goal**: Comprehensive testing + CI/CD
**Success**: 80%+ coverage, all tests pass

### Phase 4: Templates (Week 4-5)
**Agents**: 5
**Goal**: Templates + documentation
**Success**: Ready for users

---

## ❓ Communication

### Questions
**File**: `AGENT_PROMPTS/questions.md`
**Format**:
```markdown
## [Agent Name] - [Date]
**Question**: [Your question]
**Context**: [Background info]
**Blocking**: [Yes/No]
```

### Blockers
**Directory**: `AGENT_PROMPTS/issues/`
**Create file**: `blocker_[topic].md`

### Merge Requests
**Directory**: `AGENT_PROMPTS/issues/`
**Create file**: `merge_request_agent[N].md`

---

## ✅ Success Criteria

### Per-Agent Success
- [ ] All tasks completed
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Daily logs submitted
- [ ] Ready for merge

### Overall Success
- [ ] All 5 agents complete
- [ ] End-to-end pipeline works
- [ ] Can generate real projects
- [ ] 80%+ test coverage
- [ ] Documentation complete
- [ ] Ready for users

---

## 📅 Timeline Summary

| Week | Phase | Agents | Deliverables |
|------|-------|--------|--------------|
| 1-2 | Foundation | 1, 2 | Orchestrator + LLM |
| 2-3 | Agents | 3 | All 8 agents working |
| 3-4 | Quality | 4 | Tests + CI/CD |
| 4-5 | Templates | 5 | Templates + docs |

**Total**: 4-6 weeks (part-time, 2-3 hrs/day)

---

## 💰 Budget

**Starting Credits**: $931
**Estimated Usage**: $100-200
**Buffer**: $731-831 remaining

---

## 📚 Additional Resources

### Files in This Directory
```
AGENT_PROMPTS/
├── README.md                                  # This file
├── COORDINATION.md                            # Master coordination plan
├── GIT_WORKFLOW.md                            # Git procedures
├── 1_Backend_Infrastructure_Engineer.md       # Agent 1 prompt
├── 2_LLM_Integration_Specialist.md            # Agent 2 prompt
├── 3_Agent_Implementation_Developer.md        # Agent 3 prompt
├── 4_Testing_Quality_Engineer.md              # Agent 4 prompt
├── 5_Templates_Documentation_Specialist.md    # Agent 5 prompt
├── questions.md                               # Q&A thread
├── daily_logs/                                # Progress logs
│   └── YYYY-MM-DD_[agent].md
└── issues/                                    # Blockers and merge requests
    ├── blocker_[topic].md
    └── merge_request_agent[N].md
```

### Project Documentation
- [Architecture](../docs/architecture.md)
- [Agent Roles](../docs/agent_roles.md)
- [Safety Guidelines](../docs/safety.md)
- [CLI Usage](../docs/cli_usage.md)

### External Resources
- [Multi-Agent Workflow Guide](../MULTI_AGENT_WORKFLOW_GUIDE.md)
- [Git Best Practices](https://www.atlassian.com/git/tutorials)
- [Python Testing](https://docs.pytest.org/)
- [Claude API Docs](https://docs.anthropic.com/)

---

## 🆘 Getting Help

**Stuck?**
1. Check your agent prompt file
2. Review COORDINATION.md
3. Post in questions.md
4. Ask coordinator

**Git Issues?**
- Review GIT_WORKFLOW.md
- Check [Git troubleshooting section](GIT_WORKFLOW.md#-troubleshooting)

**Integration Issues?**
- Check COORDINATION.md integration points
- Post in issues/

---

## 🎉 Ready to Begin!

**Next Steps**:

1. **Coordinator**:
   - Review all files in AGENT_PROMPTS/
   - Choose which agents to launch
   - Use launch prompts above

2. **Agents**:
   - Wait for launch prompt
   - Read your role definition
   - Start with Task 1
   - Post daily updates

---

**Let's build something amazing! 🚀**

---

*Last Updated: 2025-11-17*
*Version: 1.0*
*Status: Ready for Launch*
