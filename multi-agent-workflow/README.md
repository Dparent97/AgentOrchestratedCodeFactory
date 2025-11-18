# Multi-Agent Workflow Skills Package

**8 Claude Skills that make the multi-agent workflow actually usable.**

## What You Get

This package contains 8 skills that transform your multi-agent workflow from "comprehensive but complex" to "simple and powerful":

1. **workflow-state** - "Where am I in the workflow?"
2. **phase1-planning** - "Plan my project structure"
3. **phase2-framework** - "Build the initial framework"
4. **phase3-codex-review** - "Identify improvements and create agent prompts"
5. **phase4-agent-launcher** - "Launch agents and manage progress"
6. **phase5-integration** - "Review and merge all PRs"
7. **phase5-quality-audit** - "Comprehensive code review after merge"
8. **phase6-iteration** - "Should we iterate or deploy?"

## Installation

### Step 1: Download All Skills

You should have 8 `.skill` files:
- workflow-state.skill
- phase1-planning.skill
- phase2-framework.skill
- phase3-codex-review.skill
- phase4-agent-launcher.skill
- phase5-integration.skill
- phase5-quality-audit.skill
- phase6-iteration.skill

### Step 2: Add to Claude

In Claude.ai:
1. Go to your Project settings
2. Click "Add Skill" or "Custom Skills"
3. Upload each `.skill` file
4. Skills will appear in your project

**Note:** Skills are project-specific. Add them to the project where you want to use the workflow.

## How It Works

### The State File

All skills read/write a `WORKFLOW_STATE.json` file in your project root. This tracks:
- Current phase
- Iteration number
- Agent status
- History

**You never edit this file directly** - the skills manage it.

### Auto-Advancement

Skills automatically suggest the next phase:
```
✅ Phase 3 Complete!
➡️ Next: Copy these 3 prompts to start Phase 4
```

You just follow the instructions.

## Quick Start Guide

### For New Projects

**Step 1: Planning**
```
You: "phase1-planning for my marine diesel analyzer"

Claude: [Asks about project goals, recommends tech stack, creates structure]

Result: Project scaffolded, WORKFLOW_STATE.json created
```

**Step 2: Framework**
```
You: "phase2-framework"

Claude: [Creates skeleton code based on Phase 1 plan]

Result: Working Hello World app
```

**Step 3: Continue to existing project flow** ↓

### For Existing Projects (START HERE)

**Step 1: Check Status**
```
You: "workflow-state for ship-MTA-draft"

Claude: Shows current phase, completed work, next steps
```

**Step 2: Codex Review**
```
You: "phase3-codex-review for ship-MTA-draft"

Claude: 
- Analyzes codebase
- Identifies 3-5 improvements
- Creates agent prompts
- Gives you copy-paste prompts

Result: AGENT_PROMPTS/ directory created
```

**Step 3: Launch Agents**
```
You: "phase4-agent-launcher for ship-MTA-draft"

Claude: Displays 3-4 prompts to copy to separate chats

You: [Copy each to new Claude chat]
Agents: [Work for 30-60 min]

You: [Ask agents for progress reports]
You: [Paste reports back to Phase 4 skill]

Claude: Analyzes progress, provides updated prompts
```

**Step 4: Integration**
```
You: "phase5-integration for ship-MTA-draft"

Claude: 
- Lists all PRs
- Determines merge order
- Provides merge commands
- Verifies after each merge

Result: All agent work merged to dev branch
```

**Step 5: Quality Audit (Optional)**
```
You: "phase5-quality-audit for ship-MTA-draft"

Claude: Comprehensive code review with GO/NO-GO recommendation

Result: Quality report, deployment decision
```

**Step 6: Iteration Decision**
```
You: "phase6-iteration for ship-MTA-draft"

Claude: Analyzes state, recommends:
- Deploy to production
- Fix issues then deploy
- Start Iteration 2 (more improvements)
- Add new features

If iterating: Automatically sets up for Phase 3
```

## Real-World Example

```
You: "workflow-state for ship-MTA-draft"

Claude: 
📊 ship-MTA-draft
Phase: 0 | Iteration: 0
Status: not_started

You: "phase3-codex-review for ship-MTA-draft"

Claude: [Analyzes code]
✅ Found 4 improvements
🤖 Created 4 agent prompts

Copy these to separate chats:

💬 Agent 1: Backend Performance
You are Agent 1: Backend Performance Engineer
Repository: github.com/Dparent97/ship-MTA-draft
Read and follow: AGENT_PROMPTS/1_Backend_Performance.md
START NOW

💬 Agent 2: Security Hardening
[Similar prompt]

💬 Agent 3: UI Modernization
[Similar prompt]

💬 Agent 4: Testing Infrastructure
[Similar prompt]

---

[You copy each to separate chat, agents work]

[After 60 minutes]

You: "Give me progress reports" [to each agent]

Agent 1: ✅ Done: Database optimization
Agent 2: 🔄 Working on: Input validation
Agent 3: ✅ Done: CSS modernization
Agent 4: ⚠️ Blocked by: Need schema info

You: [Paste all reports to phase4 skill]

Claude: 
📊 Progress Analysis
Agent 1: ✅ Ahead - adding cache layer
Agent 2: ✅ Good - continue
Agent 3: ✅ Done early - start responsive design
Agent 4: ⚠️ Unblocked - here's schema, continue

Updated prompts for next sprint:
[New prompts for each agent]

---

[Agents finish]

You: "phase5-integration for ship-MTA-draft"

Claude: 
🔀 Integration Review
PR #45: Backend (Agent 1) ✅
PR #46: Security (Agent 2) ✅
PR #47: UI (Agent 3) ✅
PR #48: Testing (Agent 4) ✅

Merge order:
1. PR #48 (tests) - safe first
2. PR #45 (backend) - no conflicts
3. PR #46 (security) - depends on backend
4. PR #47 (UI) - depends on backend

[Provides git commands]

✅ All merged! Tests passing.

---

You: "phase6-iteration for ship-MTA-draft"

Claude:
🎯 Decision Analysis

Completed: 4 improvements
Quality: 8/10
Tests: Passing
Issues: None

✅ RECOMMENDATION: DEPLOY

Ready for production!
```

## Tips

### Context Management

**Problem:** "Alpha" chat runs out of context during integration

**Solution:** Skills maintain state in files, not context
- Each phase is independent
- State persists in WORKFLOW_STATE.json
- Start fresh chat, use workflow-state to catch up

### Lost Track?

```
You: "workflow-state for my-project"

Claude: Shows exactly where you are, what's done, what's next
```

### Multiple Projects

Each project has its own WORKFLOW_STATE.json. Skills work on whatever project you specify.

### Agent Count Flexibility

Phase 3 skill decides optimal agent count (3-5) based on project scope. Not always 5.

### Git Confusion

Phase 5 skill gives you exact git commands to copy-paste. No need to remember git workflow.

## Troubleshooting

### "Skill not triggering"

Make sure you're in the right project and saying the trigger phrase:
- "workflow-state for ship-MTA-draft" ✅
- "check workflow status" ❌ (too vague)

### "State file not found"

Skills create it automatically. If missing:
```
You: "phase3-codex-review for my-project"

Claude: [Creates WORKFLOW_STATE.json and proceeds]
```

### "Lost agent prompts"

They're in your project's AGENT_PROMPTS/ directory. Use Phase 4 skill to re-display them.

### "Can't remember where I left off"

```
You: "workflow-state for my-project"
```

## What Makes This Better

**Before (Manual Process):**
- ❌ 7 phases to remember
- ❌ Lost track between chats
- ❌ Had to find/read long documentation
- ❌ Unclear what to do next
- ❌ Git commands confusing
- ❌ Context overflow in one chat

**After (With Skills):**
- ✅ Simple trigger phrases
- ✅ State tracked automatically
- ✅ Skills reference docs for you
- ✅ Clear next steps always shown
- ✅ Git commands provided
- ✅ Each phase in fresh context

## Advanced Usage

### Custom Agent Sprint Times

In Phase 4, you can vary sprint duration:
```
You: "Give me updated prompts for 90-minute sprint"

Claude: [Adjusts scope for longer sprint]
```

### Quick vs Comprehensive

Phase 5 and 5.5 have quick and comprehensive modes:
```
You: "phase5-integration quick merge"
You: "phase5-quality-audit comprehensive"
```

### Skipping Phases

Skip Phase 5.5 for low-risk projects:
```
Phase 5 complete → Go directly to Phase 6
```

### Multiple Iterations

Phase 6 automatically sets up Iteration 2:
```
You: "phase6-iteration"

Claude: Recommending Iteration 2

You: "phase3-codex-review"

Claude: [Finds next set of improvements for Iteration 2]
```

## File Structure After Using Skills

```
your-project/
├── WORKFLOW_STATE.json         ← State tracking
├── AGENT_PROMPTS/               ← Created by Phase 3
│   ├── 1_Backend_Engineer.md
│   ├── 2_Frontend_Engineer.md
│   └── 3_Testing_Engineer.md
├── src/                         ← Your code
├── tests/
└── ...
```

## Support

If something's not working:
1. Check workflow-state first
2. Verify you're in correct project directory
3. Make sure .skill files are installed in project
4. Use exact trigger phrases

## What's Next

You now have a complete skill-based workflow system that:
- Tracks your progress automatically
- Tells you exactly what to do next
- Makes agent coordination simple
- Manages git operations for you
- Decides when to deploy or iterate

**Start with Phase 3 on your next project and see the difference!**

---

**Created:** November 2025
**Version:** 1.0
**Skills:** 8 total (1 state checker + 7 phases)
