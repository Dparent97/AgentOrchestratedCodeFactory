# Multi-Agent Workflow - Complete Phase Reference

## 🎯 All 7 Phases at a Glance

```
Phase 1: Planning          → "Plan my project structure"
Phase 2: Framework         → "Build the initial framework"
Phase 3: Codex Review      → "Identify 5 improvements"
Phase 4: Parallel Agents   → "You are Agent [N], follow your prompt"
Phase 5: Integration       → "Review and merge all PRs"
Phase 5.5: Quality Audit   → "Comprehensive code review after merge"
Phase 6: Iteration         → "Should we iterate or deploy?"
```

---

## 📋 What to Say for Each Phase

### Phase 1: Planning (New Projects Only)
```markdown
I want to build [PROJECT DESCRIPTION].

Please help me:
1. Create project structure
2. Choose tech stack
3. Set up repository
4. Define initial architecture

START PLANNING NOW
```

---

### Phase 2: Framework Build (New Projects Only)
```markdown
Build the framework according to the plan.

Follow the structure we defined.
Create initial files and setup.
Push to GitHub when complete.

START BUILDING NOW
```

---

### Phase 3: Codex Review (START HERE for Existing Projects)
```markdown
I have the Multi-Agent Workflow system in this project.

Please:
1. Analyze this codebase
2. Identify 5 high-impact improvements
3. Create 5 specialized agent roles
4. Generate complete agent prompts in AGENT_PROMPTS/[1-5]_[Role].md
5. Update COORDINATION.md and GIT_WORKFLOW.md
6. Give me 5 simple prompts to launch agents

Reference: MULTI_AGENT_WORKFLOW_GUIDE.md

START NOW
```

**Or simply:**
```markdown
Comprehensive code review - identify 5 improvements and generate agent prompts.
```

---

### Phase 4: Launch 5 Parallel Agents
**For each of 5 agents, create a separate chat:**

```markdown
You are Agent [NUMBER]: [ROLE NAME]

Repository: https://github.com/[USERNAME]/[REPO]

Read and follow: AGENT_PROMPTS/[NUMBER]_[ROLE].md

START NOW
```

**Example:**
```markdown
You are Agent 1: iOS Core Engineer

Repository: https://github.com/Dparent97/AR-Facetime-App

Read and follow: AGENT_PROMPTS/1_iOS_Core_Engineer.md

START NOW
```

---

### Phase 5: Integration & Merge
```markdown
# PHASE 5: INTEGRATION & MERGE REVIEW

I've completed Phase 4 with 5 parallel agents.
All agents have finished and created pull requests.

Repository: https://github.com/[USERNAME]/[REPO]
Base Branch: dev

Please:
1. List all open PRs from agents
2. Review each PR for quality and conflicts
3. Determine safe merge order
4. Merge PRs one by one with verification
5. Run full test suite
6. Provide next steps recommendation

START INTEGRATION NOW
```

**Or simply:**
```markdown
Review and merge all 5 agent PRs.
```

---

### Phase 5.5: Post-Integration Quality Audit (Optional but Recommended)

**Comprehensive:**
```markdown
Comprehensive post-integration code review.

Just merged 5 agent branches.
Please review the entire codebase for:
- Code quality
- Security issues
- Performance problems
- Test coverage
- Documentation
- Risks

Repository: https://github.com/[USERNAME]/[REPO]
Branch: dev

START COMPREHENSIVE REVIEW NOW
```

**Quick:**
```markdown
Quick post-integration sanity check.

Just merged all agent work.
Check for:
- Critical issues
- Obvious bugs
- Test status
- Security problems

GO/NO-GO for deployment?

START QUICK REVIEW NOW
```

---

### Phase 6: Iteration Decision
```markdown
# ITERATION PLANNING

Repository: https://github.com/[USERNAME]/[REPO]
Branch: dev (all improvements merged)

Current state: [Brief description]

Please analyze and recommend:
- Should we do another iteration? (more improvements)
- Should we deploy to production?
- Should we add new features?

If iterating, identify next 5 improvements.

START ANALYSIS NOW
```

**Or simply:**
```markdown
Should we iterate again or deploy?
```

---

## 🎯 Quick Decision Tree

```
Starting New Project?
    Yes → Phase 1 (Planning)
    No → Phase 3 (Codex Review)
        ↓
    Phase 3: Get 5 improvements
        ↓
    Phase 4: Launch 5 agents (separate chats)
        ↓
    Phase 5: Merge all PRs
        ↓
    Phase 5.5: Quality check (recommended)
        ↓
    Ready to deploy?
        Yes → Deploy!
        No → Phase 6 (Iterate)
```

---

## 💬 Ultra-Short Versions

### Phase 3:
```
"Analyze codebase, identify 5 improvements, create agent prompts"
```

### Phase 4 (×5):
```
"You are Agent [N], follow AGENT_PROMPTS/[N]_[Role].md"
```

### Phase 5:
```
"Review and merge all agent PRs"
```

### Phase 5.5:
```
"Comprehensive code review after merge"
```

### Phase 6:
```
"Should we iterate or deploy?"
```

---

## 📂 File Usage Guide

| Phase | File to Use | Action |
|-------|-------------|--------|
| 3 | MULTI_AGENT_WORKFLOW_GUIDE.md | Read for context |
| 4 | AGENT_PROMPTS/1-5_*.md | One per agent chat |
| 5 | INTEGRATION_PROMPT.md | Paste into review chat |
| 5.5 | POST_INTEGRATION_REVIEW.md | Paste into review chat |
| 6 | (Use short prompt) | Simple question |

---

## 🎨 Real Example: Complete Flow

### Starting with Existing Project:

**Phase 3:**
```
"I have Multi-Agent Workflow set up. Analyze my AR app and create 5 agent prompts."
```
*→ Gets 5 agent prompts saved to AGENT_PROMPTS/*

**Phase 4:** (5 separate chats)
```
Chat 1: "You are Agent 1: iOS Core Engineer, follow AGENT_PROMPTS/1_iOS_Core_Engineer.md"
Chat 2: "You are Agent 2: 3D Engineer, follow AGENT_PROMPTS/2_3D_Assets_Animation_Engineer.md"
Chat 3: "You are Agent 3: UI Engineer, follow AGENT_PROMPTS/3_UI_UX_Engineer.md"
Chat 4: "You are Agent 4: QA Engineer, follow AGENT_PROMPTS/4_QA_Engineer.md"
Chat 5: "You are Agent 5: Writer, follow AGENT_PROMPTS/5_Technical_Writer.md"
```
*→ Each creates a PR*

**Phase 5:**
```
"Review and merge all 5 PRs. Repository: github.com/Dparent97/AR-Facetime-App"
```
*→ All merged to dev*

**Phase 5.5:**
```
"Comprehensive post-integration code review. Just merged 5 branches."
```
*→ Quality report generated*

**Phase 6:**
```
"Based on the review, should we iterate or deploy?"
```
*→ Recommendation provided*

---

## 📊 Time Estimates

| Phase | Time | Can Run In |
|-------|------|------------|
| 3: Codex Review | 30-60 min | Web/CLI |
| 4: 5 Agents | 2-6 hours (parallel) | Web (5 chats) |
| 5: Integration | 1-2 hours | Web/CLI |
| 5.5: Quality Audit | 30 min - 2 hours | Web/CLI |
| 6: Decision | 15-30 min | Web/CLI |

**Total for 1 iteration:** ~4-8 hours

---

## 💰 Cost Estimates (Web Sessions)

| Phase | Estimated Cost | From $931 |
|-------|---------------|-----------|
| 3: Codex Review | $5-15 | Remaining: $916-926 |
| 4: 5 Agents | $50-150 | Remaining: $766-876 |
| 5: Integration | $10-30 | Remaining: $736-866 |
| 5.5: Quality Audit | $10-40 | Remaining: $696-856 |
| 6: Decision | $2-10 | Remaining: $686-854 |

**Total per iteration:** $77-245
**You can do:** 3-12 iterations with $931

---

## ✅ Checklist Format

Use this for tracking:

```markdown
## Iteration 1 Progress

- [ ] Phase 3: Codex Review complete
- [ ] Phase 4: Agent 1 (iOS Core) - PR #42
- [ ] Phase 4: Agent 2 (3D Assets) - PR #43
- [ ] Phase 4: Agent 3 (UI/UX) - PR #44
- [ ] Phase 4: Agent 4 (QA) - PR #45
- [ ] Phase 4: Agent 5 (Writer) - PR #46
- [ ] Phase 5: All PRs merged
- [ ] Phase 5.5: Quality audit complete
- [ ] Phase 6: Decision made

Next: [Iterate / Deploy / Features]
```

---

## 🚀 Quick Start Card

**Print this and keep handy:**

```
┌─────────────────────────────────────────┐
│   MULTI-AGENT WORKFLOW QUICK START     │
├─────────────────────────────────────────┤
│ 1. Review: "Identify 5 improvements"   │
│ 2. Agents: 5 chats, each follows file  │
│ 3. Merge: "Review and merge all PRs"   │
│ 4. Audit: "Code review after merge"    │
│ 5. Decide: "Iterate or deploy?"        │
└─────────────────────────────────────────┘
```

---

**Save this file as your quick reference!**
