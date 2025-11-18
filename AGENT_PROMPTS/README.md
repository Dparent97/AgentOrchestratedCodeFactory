# Iteration 2: Multi-Agent Development - Agent Implementation

**Project:** Agent-Orchestrated Code Factory
**Phase:** Iteration 2 - Implement Agent Logic
**Timeline:** 2-3 weeks (November 18 - December 8, 2025)
**Approach:** 3-Wave Multi-Agent Development

---

## 🎯 Mission

Implement the 7 specialized agents that form the core intelligence of the Code Factory:
1. **PlannerAgent** - Break ideas into actionable tasks
2. **ArchitectAgent** - Design project structure and tech stack
3. **ImplementerAgent** - Generate source code
4. **TesterAgent** - Create and run tests
5. **DocWriterAgent** - Generate documentation
6. **GitOpsAgent** - Manage version control
7. **BlueCollarAdvisor** - Ensure field-practical design

---

## 🌊 Wave-Based Development

### Wave 1: Foundation (Week 1 - Nov 18-22)
**Goal:** Core agent foundation + testing infrastructure

**Active Agents:**
- **Agent Foundation Developer** - Implements PlannerAgent + ArchitectAgent
- **QA Engineer** - Creates agent test harness and integration tests
- **Technical Writer** - Establishes agent documentation framework

**Success Criteria:**
- [ ] PlannerAgent converts Ideas into Task lists
- [ ] ArchitectAgent generates ProjectSpec from Ideas + Tasks
- [ ] Integration test: Idea → Tasks → ProjectSpec works end-to-end
- [ ] Test harness ready for testing all agents
- [ ] Agent API documentation framework exists

**Demo:** `code-factory plan "Build a log parser"` generates valid task breakdown

---

### Wave 2: Code Generation (Week 2 - Nov 25-29)
**Goal:** Code generation + supporting agents

**Active Agents:**
- **Code Generation Developer** - Implements ImplementerAgent
- **Support Agents Developer** - Implements TesterAgent + DocWriterAgent
- **QA Engineer** (continues) - Integration tests for code generation
- **Technical Writer** (continues) - Usage examples and tutorials

**Success Criteria:**
- [ ] ImplementerAgent generates working code from ProjectSpec
- [ ] TesterAgent creates test files
- [ ] DocWriterAgent generates README and docs
- [ ] End-to-end: Idea → Tasks → Spec → Code → Tests → Docs
- [ ] All agents have comprehensive tests
- [ ] Complete usage documentation

**Demo:** Generate a simple CLI tool end-to-end

---

### Wave 3: GitOps & Polish (Week 3 - Dec 2-8)
**Goal:** Complete orchestration + field-practical enhancements

**Active Agents:**
- **Support Agents Developer** (continues) - GitOpsAgent + BlueCollarAdvisor enhancement
- **QA Engineer** (continues) - End-to-end orchestration tests
- **Technical Writer** (continues) - Complete documentation, tutorials, examples

**Success Criteria:**
- [ ] GitOpsAgent initializes repos and manages commits
- [ ] BlueCollarAdvisor reviews for blue-collar usability
- [ ] Full orchestration: Idea → Working GitHub repository
- [ ] SafetyGuard integration verified
- [ ] Comprehensive test suite (>85% coverage)
- [ ] Production-ready documentation

**Demo:** `code-factory create "Marine equipment log analyzer"` → Full working project

---

## 📁 Directory Structure

```
AGENT_PROMPTS/
├── README.md                    # This file - overview and mission
├── COORDINATION.md              # Integration points and dependencies
├── WAVE_1/                      # Wave 1 role prompts
│   ├── 1_agent_foundation_dev.md
│   ├── 2_qa_engineer.md
│   └── 3_technical_writer.md
├── WAVE_2/                      # Wave 2 role prompts
│   ├── 1_code_generation_dev.md
│   ├── 2_support_agents_dev.md
│   └── [QA and Writer continue]
├── WAVE_3/                      # Wave 3 role prompts
│   └── [GitOps and polish]
├── daily_logs/                  # Daily progress updates
│   ├── 2025-11-18.md
│   ├── 2025-11-19.md
│   └── ...
├── issues/                      # Coordination issues and blockers
│   └── [Issue tracking]
└── questions.md                 # Q&A between agents
```

---

## 🤝 Agent Coordination

### Communication Protocol
1. **Daily Logs**: Each agent posts progress to `daily_logs/YYYY-MM-DD.md`
2. **Questions**: Post to `questions.md` for other agents to answer
3. **Blockers**: Create issue in `issues/` directory
4. **Integration**: See `COORDINATION.md` for API contracts

### Git Workflow
```
main (protected)
├── wave-1/agent-foundation     # Agent Foundation Developer
├── wave-1/qa-infrastructure    # QA Engineer
├── wave-1/docs-framework       # Technical Writer
├── wave-2/code-generation      # Code Generation Developer
├── wave-2/support-agents       # Support Agents Developer
└── wave-3/gitops-polish        # Final wave
```

### Merge Policy
- ✅ All tests passing
- ✅ Code reviewed by QA Engineer
- ✅ Documentation updated
- ✅ No merge conflicts
- ✅ Integration points verified

---

## 📊 Current State

### Infrastructure (Phase 5 - Complete ✅)
- ✅ Configuration system (FactoryConfig)
- ✅ SafetyGuard (multi-layer security)
- ✅ Checkpoint system (pipeline recovery)
- ✅ Transaction system (safe file operations)
- ✅ Agent runtime (execution, timeout, isolation)
- ✅ Test coverage: 83.81%

### Agent Implementation (Iteration 2 - In Progress 🔄)

| Agent | Status | Implementer | Branch | Tests |
|-------|--------|-------------|--------|-------|
| PlannerAgent | 🔄 Scaffolding | Wave 1: Foundation Dev | TBD | ❌ |
| ArchitectAgent | 🔄 Scaffolding | Wave 1: Foundation Dev | TBD | ❌ |
| ImplementerAgent | 🔄 Scaffolding | Wave 2: Code Gen Dev | TBD | ❌ |
| TesterAgent | 🔄 Scaffolding | Wave 2: Support Dev | TBD | ❌ |
| DocWriterAgent | 🔄 Scaffolding | Wave 2: Support Dev | TBD | ❌ |
| GitOpsAgent | 🔄 Scaffolding | Wave 3: Support Dev | TBD | ❌ |
| BlueCollarAdvisor | 🔄 Partial | Wave 3: Support Dev | TBD | ❌ |
| SafetyGuard | ✅ Complete | Phase 5 | main | ✅ |

---

## 🚀 Getting Started

### For Agent Developers

1. **Read your role prompt** in `WAVE_X/Y_your_role.md`
2. **Review COORDINATION.md** to understand integration points
3. **Check existing code**:
   ```bash
   # See current agent scaffolding
   cat src/code_factory/agents/planner.py
   cat src/code_factory/agents/architect.py
   # etc.
   ```
4. **Create your branch**:
   ```bash
   git checkout -b wave-1/agent-foundation
   ```
5. **Start implementing** based on your role prompt
6. **Post daily updates** to `daily_logs/`
7. **Ask questions** in `questions.md`

### For QA Engineer

1. **Read your role prompt** in `WAVE_1/2_qa_engineer.md`
2. **Review existing tests**:
   ```bash
   ls tests/unit/
   pytest tests/ -v
   ```
3. **Create test harness** for agent testing
4. **Monitor all agent work** for quality
5. **Review PRs** before merge

### For Technical Writer

1. **Read your role prompt** in `WAVE_1/3_technical_writer.md`
2. **Review existing docs**:
   ```bash
   ls docs/
   cat docs/architecture.md
   ```
3. **Create documentation framework** for agents
4. **Document APIs** as they're implemented
5. **Write usage examples**

---

## 📋 Daily Workflow

### Morning (15 minutes)
1. Read yesterday's logs from all agents
2. Check `questions.md` for unanswered questions
3. Review `issues/` for blockers
4. Plan your day's work

### During Day
1. Implement your assigned tasks
2. Write tests as you code
3. Document your APIs
4. Commit frequently with clear messages

### Evening (10 minutes)
1. Post daily log to `daily_logs/YYYY-MM-DD.md`
2. Answer questions from other agents
3. Update your branch status
4. Prepare for tomorrow

---

## 🎯 Success Metrics

### Wave 1 Complete When:
- [ ] PlannerAgent + ArchitectAgent working
- [ ] Integration test passing
- [ ] Test harness ready
- [ ] Documentation framework exists
- [ ] All Wave 1 branches merged to main

### Wave 2 Complete When:
- [ ] ImplementerAgent generating code
- [ ] TesterAgent + DocWriterAgent working
- [ ] End-to-end pipeline functional
- [ ] Test coverage >85%
- [ ] Usage examples published

### Wave 3 Complete When:
- [ ] GitOpsAgent managing version control
- [ ] BlueCollarAdvisor reviewing designs
- [ ] Full orchestration working
- [ ] Production-ready documentation
- [ ] Ready for v0.2.0 release

### Iteration 2 Complete When:
- [ ] All 7 agents implemented
- [ ] End-to-end: Idea → GitHub repo works
- [ ] Test coverage >85%
- [ ] Complete documentation
- [ ] Example projects generated successfully
- [ ] SafetyGuard integration verified
- [ ] Blue-collar focus maintained

---

## ⚠️ Important Reminders

### Safety First
- All agent outputs must pass through SafetyGuard
- No bypassing safety checks
- Test dangerous operation blocking
- Maintain audit trail

### Blue-Collar Focus
- Generated tools must be practical for field workers
- Offline-capable where possible
- Simple CLI interfaces
- Clear error messages
- Rugged, reliable code

### Quality Standards
- 80%+ test coverage required
- Type hints on all functions
- Docstrings following Google style
- No TODOs without tracking issues
- Code follows project style (ruff, black)

### Integration Testing
- Test agent-to-agent communication
- Test full orchestration pipeline
- Test with real-world ideas
- Test edge cases and failures
- Test SafetyGuard integration

---

## 📞 Coordination

### Questions?
Post to `questions.md` with:
- Your agent name
- Question context
- Whether it's blocking
- Who should answer

### Blocked?
Create issue in `issues/` with:
- Issue title
- Description
- What you need to unblock
- Who can help

### Integration Issues?
Update `COORDINATION.md` with:
- What's not working
- Expected vs actual behavior
- Proposed solution

---

## 🎉 Let's Build!

Infrastructure is ready. Tests are in place. Safety is enforced.

**Now it's time to bring these agents to life!**

Each wave builds on the last. Each agent enables the next.

By the end of Iteration 2, we'll have a working system that can take plain-language ideas and generate complete, tested, documented software projects.

**Wave 1 starts: November 18, 2025**

Good luck, agents! 🚀

---

*Last Updated: November 17, 2025*
*Next Review: End of Wave 1 (November 22, 2025)*
