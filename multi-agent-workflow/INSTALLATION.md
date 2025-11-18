# Installation & Setup Guide

## What Was Built

✅ **8 Claude Skills** for the multi-agent workflow:

1. **workflow-state.skill** (3.0 KB) - Check current status
2. **phase1-planning.skill** (3.4 KB) - Plan new projects
3. **phase2-framework.skill** (3.3 KB) - Build skeleton code
4. **phase3-codex-review.skill** (4.2 KB) - Analyze & create agents ⭐
5. **phase4-agent-launcher.skill** (4.3 KB) - Manage agent sprints
6. **phase5-integration.skill** (4.1 KB) - Merge PRs
7. **phase5-quality-audit.skill** (4.3 KB) - Post-merge review
8. **phase6-iteration.skill** (4.2 KB) - Decide next steps

**Total Package Size:** ~35 KB

## Installation Steps

### 1. Download All Files

Download these files from this conversation:
- All 8 `.skill` files
- `README.md` (comprehensive guide)
- `QUICK_REFERENCE.md` (cheat sheet)

### 2. Add Skills to Claude Project

**In claude.ai:**

1. Open the project where you want the multi-agent workflow
2. Click **Settings** (gear icon)
3. Go to **Skills** or **Custom Skills**
4. Click **Add Skill** or **Upload**
5. Upload each `.skill` file one by one

All 8 skills should appear in your project skills list.

### 3. Verify Installation

Create a test to verify:

**In Claude chat (in your project):**
```
You: "workflow-state for test"

Expected: Claude uses the workflow-state skill and shows state info
```

If it works, you're ready!

## First Run

### For Existing Project

```
You: "phase3-codex-review for [your-project-name]"

Claude will:
1. Analyze your codebase
2. Identify 3-5 improvements
3. Create agent prompts
4. Give you copy-paste prompts for agents
```

This creates `WORKFLOW_STATE.json` and `AGENT_PROMPTS/` in your project.

### For New Project

```
You: "phase1-planning for my awesome project"

Claude will:
1. Ask about your goals
2. Recommend tech stack
3. Create directory structure
4. Initialize git and state tracking
```

Then proceed with phase2, phase3, etc.

## Project Structure

After first skill use, your project will have:

```
your-project/
├── WORKFLOW_STATE.json         ← Automatically created
├── AGENT_PROMPTS/               ← Created by Phase 3
│   ├── 1_Role_Name.md
│   ├── 2_Role_Name.md
│   └── 3_Role_Name.md
├── [your existing code]
└── [your existing files]
```

**Never edit WORKFLOW_STATE.json directly** - skills manage it.

## Quick Test Workflow

Try a complete mini-workflow:

```
1. "phase3-codex-review for test-project"
2. [Claude analyzes, creates agent prompts]
3. Copy one agent prompt to a new chat
4. [Agent works and reports back]
5. "phase5-integration for test-project"
6. "phase6-iteration for test-project"
```

This verifies all skills work.

## Using with Existing Multi-Agent Docs

These skills **complement** your existing documentation:
- Skills reference `INTEGRATION_PROMPT.md`
- Skills reference `POST_INTEGRATION_REVIEW.md`
- Skills reference `PHASE_REFERENCE_CARD.md`

**But you don't need to read those anymore** - skills do it for you!

## Tips for Success

### 1. Use in Projects with the Docs

Add skills to the same project that has:
- `MULTI_AGENT_WORKFLOW_GUIDE.md`
- `INTEGRATION_PROMPT.md`
- `PHASE_REFERENCE_CARD.md`
- Other workflow documentation

Skills will reference these automatically.

### 2. Always Use Exact Trigger Phrases

✅ Good: `"phase3-codex-review for ship-MTA-draft"`
❌ Bad: `"analyze my code"` (too vague)

### 3. Start Fresh When Context Gets Full

If a chat gets too long:
1. Open new chat in same project
2. Use `workflow-state` to catch up
3. Continue from current phase

### 4. Keep QUICK_REFERENCE.md Handy

Print it or keep it open while working. It has all trigger phrases.

## What Each Skill Does (Summary)

| Skill | Use For | Required? |
|-------|---------|-----------|
| workflow-state | Check status anytime | Helpful |
| phase1 | New projects only | Skip for existing |
| phase2 | New projects only | Skip for existing |
| **phase3** | **Start here for existing!** | **Always** |
| phase4 | Agent management | Always |
| phase5 | Merge PRs | Always |
| phase5.5 | Quality check | Optional |
| phase6 | Decide next | Always |

## Typical Workflow

**Most Common Pattern (Existing Code):**

```
workflow-state         [Optional: Check where you are]
↓
phase3-codex-review   [Analyze, create agent prompts]
↓
phase4-agent-launcher [Run agents in sprints]
↓
phase5-integration    [Merge all PRs]
↓
phase5-quality-audit  [Optional: Comprehensive review]
↓
phase6-iteration      [Deploy or iterate]
```

## Troubleshooting

### Skills Not Appearing

- Verify you uploaded to correct project
- Check Skills section in project settings
- Refresh your browser

### Skill Not Triggering

- Use exact trigger phrase from QUICK_REFERENCE.md
- Make sure you're in the project with skills installed
- Try `workflow-state for [project]` first

### State File Issues

Skills create `WORKFLOW_STATE.json` automatically. If missing:
- Run any phase skill
- It will create the file
- Don't create manually

### Lost Agent Prompts

They're saved in `AGENT_PROMPTS/` directory. Use phase4 skill to re-display them.

## Next Steps

1. **Install all 8 skills** in your project
2. **Keep QUICK_REFERENCE.md** open while working
3. **Run phase3-codex-review** on your next project
4. **Experience the difference!**

## What Changed from Manual Process

**Before:**
- Had to find and read long docs
- Lost track between sessions
- Unclear what to do next
- Git commands confusing
- Context overflow

**After:**
- Skills reference docs for you
- State tracked automatically
- Next steps always clear
- Git commands provided
- Fresh context per phase

## Support

Read the documentation:
1. `README.md` - Full guide with examples
2. `QUICK_REFERENCE.md` - Trigger phrases and patterns

Still stuck? Use `workflow-state` to see where you are.

---

**You're ready! Start with phase3-codex-review on your next project.**

**Version:** 1.0
**Created:** November 2025
**Skills:** 8 total
