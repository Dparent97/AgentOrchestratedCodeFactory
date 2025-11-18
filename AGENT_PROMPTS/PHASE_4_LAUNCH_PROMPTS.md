# Phase 4: Agent Launch Prompts

**Phase 3 Complete!** ✅

You now have 4 specialized agent prompts ready to deploy. Use these prompts to launch each agent in separate Claude conversations.

---

## 🚀 Quick Reference

| Agent | Priority | Time | Can Start |
|-------|----------|------|-----------|
| Agent 1: Pipeline Integration | CRITICAL | 2-3 hrs | NOW |
| Agent 2: Code Generation | HIGH | 3-4 hrs | After Agent 1 (or parallel) |
| Agent 3: Git Operations | HIGH | 2-3 hrs | After Agent 2 |
| Agent 4: Testing & Docs | HIGH | 3-4 hrs | After Agent 2 |

**Total Time:** 10-14 hours (can be parallelized to 6-8 hours)

**Recommended Order:**
1. Launch Agent 1 first (CRITICAL - unblocks others)
2. Launch Agent 2 after Agent 1 completes (or in parallel if confident)
3. Launch Agents 3 and 4 in parallel after Agent 2

---

## 📋 Agent 1: Pipeline Integration Engineer

**Launch this agent FIRST** - it unblocks all others.

**Copy and paste this into a new Claude conversation:**

```markdown
You are Agent 1: Pipeline Integration Engineer

Repository: https://github.com/Dparent97/AgentOrchestratedCodeFactory

Branch: claude/fix-pipeline-integration

Read and follow: AGENT_PROMPTS/1_Pipeline_Integration_Engineer.md

Your mission:
- Fix broken module imports in agents/__init__.py
- Restore orchestrator pipeline (uncomment all 7 stages)
- Fix task ID format inconsistency
- Enable end-to-end project generation

Priority: CRITICAL - All other agents depend on your work

Time estimate: 2-3 hours

START NOW
```

---

## 📋 Agent 2: Code Generation Engineer

**Launch after Agent 1 completes** (or in parallel if you're experienced).

**Copy and paste this into a new Claude conversation:**

```markdown
You are Agent 2: Code Generation Engineer

Repository: https://github.com/Dparent97/AgentOrchestratedCodeFactory

Branch: claude/implement-code-generation

Read and follow: AGENT_PROMPTS/2_Code_Generation_Engineer.md

Your mission:
- Create template-based code generation system
- Implement real ImplementerAgent (replace placeholder)
- Generate working Python CLI and library projects
- Integrate with transaction system

Priority: HIGH - Agents 3 and 4 depend on your work

Time estimate: 3-4 hours

START NOW
```

---

## 📋 Agent 3: Git Operations Engineer

**Launch after Agent 2 completes** (needs real code to commit).

**Copy and paste this into a new Claude conversation:**

```markdown
You are Agent 3: Git Operations Engineer

Repository: https://github.com/Dparent97/AgentOrchestratedCodeFactory

Branch: claude/implement-git-operations

Read and follow: AGENT_PROMPTS/3_Git_Operations_Engineer.md

Your mission:
- Implement real Git operations using gitpython
- Create repositories and commit code
- Support remote management (GitHub)
- Handle errors gracefully

Priority: HIGH - Completes version control integration

Time estimate: 2-3 hours

Depends on: Agent 2 (Code Generation Engineer)

START NOW
```

---

## 📋 Agent 4: Testing & Documentation Engineer

**Launch after Agent 2 completes** (can run in parallel with Agent 3).

**Copy and paste this into a new Claude conversation:**

```markdown
You are Agent 4: Testing & Documentation Engineer

Repository: https://github.com/Dparent97/AgentOrchestratedCodeFactory

Branch: claude/implement-testing-docs

Read and follow: AGENT_PROMPTS/4_Testing_Documentation_Engineer.md

Your mission:
- Implement TesterAgent with real pytest generation
- Implement DocWriterAgent with comprehensive docs
- Generate test files, coverage reports
- Create README, CONTRIBUTING, LICENSE, docs/

Priority: HIGH - Completes testing and documentation

Time estimate: 3-4 hours

Depends on: Agent 2 (Code Generation Engineer)

START NOW
```

---

## 🎯 Execution Strategies

### Strategy 1: Sequential (Safest)
**Best for:** Learning the workflow, tight dependencies

```
Day 1:
  Agent 1 (2-3 hrs) → Complete → Merge

Day 2:
  Agent 2 (3-4 hrs) → Complete → Merge

Day 3:
  Agent 3 (2-3 hrs) → Complete → Merge
  Agent 4 (3-4 hrs) → Complete → Merge

Total: 3 days, ~10-14 hours
```

### Strategy 2: Parallel (Faster)
**Best for:** Experienced users, multiple sessions

```
Day 1 Morning:
  Agent 1 (2-3 hrs) → Complete → Merge

Day 1 Afternoon:
  Agent 2 (3-4 hrs) → Complete → Merge

Day 2:
  Agent 3 (2-3 hrs) ─┐
                     ├→ Both in parallel → Complete → Merge both
  Agent 4 (3-4 hrs) ─┘

Total: 2 days, ~10-14 hours (parallelized to ~8-10 hours of wall time)
```

### Strategy 3: Aggressive Parallel (Fastest, Riskiest)
**Best for:** Experts, high confidence in prompts

```
Day 1:
  Agent 1 (2-3 hrs) → Start immediately

  Agent 2 (3-4 hrs) → Start 30 min after Agent 1 (don't wait for merge)

  Agent 3 (2-3 hrs) ─┐
                     ├→ Start when Agent 2 is 50% done
  Agent 4 (3-4 hrs) ─┘

Total: 1 day, ~10-14 hours (heavy parallelization to ~6-8 hours)

Risk: Integration conflicts if agents make conflicting changes
```

**Recommendation:** Use Strategy 2 (Parallel) for best balance of speed and safety.

---

## ✅ Pre-Launch Checklist

Before launching agents, verify:

- [ ] You have 4 separate Claude conversations ready (Claude.ai web or CLI)
- [ ] Repository is accessible: https://github.com/Dparent97/AgentOrchestratedCodeFactory
- [ ] You have Git push access to the repository
- [ ] Current branch is clean (no uncommitted changes blocking agent work)
- [ ] You've read COORDINATION.md to understand integration points
- [ ] You understand the dependency graph (1 → 2 → [3, 4])

---

## 📊 Progress Tracking

Use this checklist to track agent progress:

```markdown
## Phase 4 Progress

**Agent 1: Pipeline Integration**
- [ ] Started (conversation launched)
- [ ] Branch created: claude/fix-pipeline-integration
- [ ] Module imports fixed
- [ ] Orchestrator pipeline connected
- [ ] Task ID format fixed
- [ ] Tests passing
- [ ] PR created: #___
- [ ] PR merged

**Agent 2: Code Generation**
- [ ] Started (conversation launched)
- [ ] Branch created: claude/implement-code-generation
- [ ] Template system implemented
- [ ] ImplementerAgent updated
- [ ] Tests passing
- [ ] PR created: #___
- [ ] PR merged

**Agent 3: Git Operations**
- [ ] Started (conversation launched)
- [ ] Branch created: claude/implement-git-operations
- [ ] GitOpsAgent implemented
- [ ] Tests passing
- [ ] PR created: #___
- [ ] PR merged

**Agent 4: Testing & Documentation**
- [ ] Started (conversation launched)
- [ ] Branch created: claude/implement-testing-docs
- [ ] TesterAgent implemented
- [ ] DocWriterAgent implemented
- [ ] Tests passing
- [ ] PR created: #___
- [ ] PR merged

**Integration**
- [ ] All 4 PRs merged
- [ ] Integration tests pass
- [ ] End-to-end demo works
- [ ] Phase 4 complete!
```

---

## 🔍 Monitoring Agent Progress

### Check Daily Logs

Agents should post daily updates to `AGENT_PROMPTS/daily_logs/YYYY-MM-DD.md`

Example check:
```bash
cat AGENT_PROMPTS/daily_logs/2025-11-18.md
```

### Check Questions

Agents may post questions to `AGENT_PROMPTS/questions.md`

Check periodically and answer blockers.

### Check PRs

Monitor GitHub for pull requests from agent branches:
- `claude/fix-pipeline-integration`
- `claude/implement-code-generation`
- `claude/implement-git-operations`
- `claude/implement-testing-docs`

---

## 🚨 Troubleshooting

### Problem: Agent is blocked

**Solution:**
1. Check `AGENT_PROMPTS/questions.md` for specific questions
2. Respond with clarification
3. Point agent to relevant documentation
4. If truly stuck, can switch to manual implementation

### Problem: Integration conflicts

**Solution:**
1. Review `AGENT_PROMPTS/COORDINATION.md` - agents have exclusive file ownership
2. If conflict occurs, last agent to merge should resolve
3. Use git rebase if needed
4. Verify tests still pass after resolution

### Problem: Tests failing

**Solution:**
1. Agent should debug and fix before creating PR
2. If persistent, review test expectations in test files
3. May need to update test fixtures or mocks
4. Ensure all dependencies installed

### Problem: Agent goes off-track

**Solution:**
1. Remind agent to read their specific prompt file
2. Point to success criteria in prompt
3. Clarify the specific files they should modify
4. Can restart agent with clearer instructions

---

## 🎉 Success Criteria

**Phase 4 is complete when:**

1. ✅ All 4 agents have completed their work
2. ✅ All 4 PRs are created and merged
3. ✅ All tests pass: `pytest`
4. ✅ Integration test works: `pytest tests/integration/`
5. ✅ End-to-end demo succeeds:
   ```bash
   code-factory create "Build a CSV parser"
   cd output/csv-parser
   pip install -e .
   csv-parser --help
   pytest
   ```
6. ✅ Generated project includes:
   - Working Python code
   - pytest test suite
   - Comprehensive documentation
   - Git repository with commits
7. ✅ Test coverage remains >80%

---

## 📝 After Phase 4

Once all agents complete:

1. **Merge all PRs** to dev or main branch
2. **Run full test suite** to verify integration
3. **Create demo project** to validate end-to-end
4. **Update documentation** with any learnings
5. **Tag release** (e.g., `v0.2.0-phase3-complete`)
6. **Decide next steps:**
   - Phase 5: Integration & Quality Audit
   - Phase 6: Iteration or Deployment
   - Additional features
   - Production deployment

---

## 🎯 Ready to Launch?

1. **Copy** Agent 1 prompt above
2. **Open** new Claude conversation
3. **Paste** the prompt
4. **Launch!**

Then repeat for Agents 2, 3, 4 as dependencies complete.

---

**Good luck! Each agent has detailed instructions in their prompt file.**

**Questions?** Post to `AGENT_PROMPTS/questions.md`

**Issues?** Create issue in `AGENT_PROMPTS/issues/`

---

*Generated by Phase 3 Codex Review - November 18, 2025*
