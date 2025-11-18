# Multi-Agent Workflow - Quick Reference Card

## 🎯 One-Line Triggers

```
workflow-state for [project]           → Where am I?
phase1-planning for [project]          → New project setup
phase2-framework                       → Build skeleton code
phase3-codex-review for [project]      → Analyze & create agent prompts ⭐ START HERE
phase4-agent-launcher for [project]    → Launch/manage agents
phase5-integration for [project]       → Merge all PRs
phase5-quality-audit for [project]     → Post-merge review
phase6-iteration for [project]         → Deploy or iterate?
```

## 🚀 Typical Flow (Existing Project)

```
1. "phase3-codex-review for ship-MTA-draft"
   → Get 3-4 agent prompts

2. Copy each prompt to separate Claude chat
   → Agents work in parallel

3. After 30-60 min: Ask agents for progress reports

4. Paste reports to: "phase4-agent-launcher"
   → Get updated prompts, repeat

5. When agents done: "phase5-integration"
   → Merge all PRs

6. (Optional) "phase5-quality-audit"
   → Comprehensive review

7. "phase6-iteration"
   → Deploy or start Iteration 2
```

## 📋 State Tracking

**WORKFLOW_STATE.json** in project root tracks everything:
- Current phase
- Agent status
- Iteration number
- History

**Never edit directly** - skills manage it automatically.

## 🔄 Progress Reports Template

Give to agents:
```markdown
Agent [N] - [30/60] min check-in

✅ Done:
- Task 1

🔄 Working on:
- Current task

⚠️ Blocked by:
- Issue or "None"

⏭️ Next:
- Planned task
```

## 🎨 Agent Sprint Pattern

```
1. Launch agents (Phase 4)
2. Agents work 30-60 min
3. Collect progress reports
4. Paste to Phase 4 skill
5. Get updated prompts
6. Repeat until done
```

## 📊 Lost Track?

```
"workflow-state for my-project"
```

Shows:
- Current phase/iteration
- Completed phases
- Active agents
- Next action

## ⚡ Quick Commands

```bash
# Check status
workflow-state for [project]

# Start fresh iteration
phase3-codex-review for [project]

# Quick merge (skip comprehensive review)
phase5-integration for [project]

# Skip audit (go straight to decision)
[After Phase 5] → phase6-iteration
```

## 🎯 Phase Purposes

| Phase | Purpose | Skip When |
|-------|---------|-----------|
| 1 | Plan new project | Have existing code |
| 2 | Build skeleton | Have existing code |
| 3 | Find improvements | Never (start here!) |
| 4 | Run agents | - |
| 5 | Merge PRs | - |
| 5.5 | Quality audit | Low-risk changes |
| 6 | Decide next | - |

## 🔧 Common Patterns

### Pattern 1: New Project
```
phase1-planning → phase2-framework → phase3-codex-review → ...
```

### Pattern 2: Existing Project (Most Common)
```
phase3-codex-review → phase4-agent-launcher → phase5-integration → phase6-iteration
```

### Pattern 3: Quick Iteration
```
phase3-codex-review → phase4-agent-launcher → phase5-integration → phase6-iteration → [repeat]
```

### Pattern 4: Production Deploy
```
... → phase5-integration → phase5-quality-audit → phase6-iteration → DEPLOY
```

## 💡 Pro Tips

1. **Always start with Phase 3** for existing projects
2. **workflow-state** is your friend when lost
3. **Agent sprints** work better than marathons (30-60 min)
4. **Phase 4 re-evaluation** keeps agents unblocked
5. **Skip Phase 5.5** for simple changes
6. **Fresh chat per phase** if context gets full

## 🚨 Common Issues

**"Skill not triggering"**
→ Use exact trigger phrase: `phase3-codex-review for [project]`

**"Lost where I was"**
→ `workflow-state for [project]`

**"Can't find agent prompts"**
→ They're in `AGENT_PROMPTS/` directory in your project

**"Context overflow in main chat"**
→ Each phase works in independent context

## 📦 What Gets Created

```
your-project/
├── WORKFLOW_STATE.json         ← Auto-created by skills
├── AGENT_PROMPTS/               ← Created by Phase 3
│   ├── 1_Role.md
│   ├── 2_Role.md
│   └── 3_Role.md
└── [your code]
```

## 🎪 Phase 4 Agent Management

```
Launch → Work 60min → Report → Evaluate → Adjust → Repeat → Done
         ↑                                  ↑
         └──────────────────────────────────┘
         Skills provide updated prompts each cycle
```

## 📈 Success Metrics

Track via workflow-state:
- Iterations completed
- Improvements per iteration
- Time per phase
- Agent completion rate

---

**Remember:** Start with `phase3-codex-review` for existing projects!

**Stuck?** → `workflow-state for [project]`
