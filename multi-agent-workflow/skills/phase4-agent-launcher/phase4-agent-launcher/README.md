# Phase 4: Agent Launcher & Progress Management

A skill for launching parallel AI agents and managing sprint-based progress tracking in the multi-agent workflow.

## Overview

This skill implements Phase 4 of the multi-agent workflow, which:
1. **Launches agents** - Generates copy-paste prompts for 3-5 specialized agents
2. **Tracks progress** - Evaluates agent progress reports during sprint check-ins
3. **Re-evaluates work** - Dynamically adjusts agent tasks based on progress

## Quick Start

### Installation

The skill is ready to use. Simply invoke it from Claude Code or run the CLI directly:

```bash
# Show current status
python scripts/launcher.py /path/to/project status

# Launch agents for 60-minute sprint
python scripts/launcher.py /path/to/project launch 60

# Evaluate progress reports
python scripts/launcher.py /path/to/project evaluate reports.txt 60
```

### Prerequisites

- Phase 3 (codex-review) completed - creates agent prompt files
- `WORKFLOW_STATE.json` with agent definitions
- `AGENT_PROMPTS/` directory with agent role files

## Usage

### 1. Launch Agents

After Phase 3 generates agent prompts:

```python
from scripts.launcher import AgentLauncher

launcher = AgentLauncher("/path/to/project")
launcher.launch_agents(sprint_duration=60)
```

This will:
- Read agent definitions from `WORKFLOW_STATE.json`
- Generate copy-paste prompts for each agent
- Display prompts for launching in separate Claude chat windows
- Update agent status to `in_progress`

**Output Example:**
```
🚀 Launching 3 Agents in Parallel

======================================================================
💬 Agent 1: Backend Developer
======================================================================

You are Agent 1: Backend Developer

Repository: https://github.com/user/repo

📋 Instructions:
1. Clone the repository: git clone https://github.com/user/repo
2. Read your detailed instructions: AGENT_PROMPTS/1_backend_developer.md
3. Follow the role definition and complete assigned tasks
4. Create a PR when ready
5. Provide progress reports when asked

START NOW - Work independently and follow your role's guidelines.

----------------------------------------------------------------------
```

### 2. Evaluate Progress Reports

After a sprint (30-60 minutes), collect progress reports from each agent:

```python
reports = """
Agent 1: Backend Developer
✅ Done:
- Implemented user authentication
- Added database migrations
🔄 Working on:
- API rate limiting (60% complete)
⏭️ Next:
- Error handling middleware

Agent 2: Frontend Developer
✅ Done:
- Login page component
- Routing setup
⚠️ Blocked by:
- Need authentication API endpoints
⏭️ Next:
- Dashboard UI
"""

launcher.evaluate_progress(reports, next_sprint_duration=60)
```

This will:
- Parse each agent's progress report
- Analyze status (ahead/on-track/behind/blocked)
- Generate updated prompts for next sprint
- Adjust tasks dynamically

**Output Example:**
```
📊 Analyzing Agent Progress Reports
======================================================================

✅ Agent 1: Backend Developer
   Status: ON_TRACK
   Action: Continue current plan
   Note: Good progress, stay on track

🚫 Agent 2: Frontend Developer
   Status: BLOCKED
   Action: Provide workaround or redirect to different task
   Note: Blocked by: Need authentication API endpoints

🔄 Updated Prompts for Next 60-Minute Sprint
======================================================================

💬 Agent 2: Frontend Developer (Updated)
======================================================================

Continue your work as Frontend Developer

✅ Completed:
   - Login page component
   - Routing setup

🔄 NEW DIRECTION:
   Your blocker: Need authentication API endpoints
   → Switch to different task while waiting
   → Work on: Dashboard UI

⏱️  Time: 60 minutes

💡 Provide progress report when this sprint ends
```

### 3. Check Status

At any time, check workflow status:

```python
launcher.show_status()
```

Or via CLI:
```bash
python scripts/launcher.py . status
```

## Progress Report Format

Agents should provide reports in this format:

```markdown
Agent [N] - [Role Name]

✅ Done:
- Task 1 completed
- Task 2 completed

🔄 Working on:
- Current task (X% complete)

⚠️ Blocked by:
- [Issue description, or "None"]

⏭️ Next:
- Planned next task
```

## Re-Evaluation Logic

The launcher automatically adjusts agent tasks based on progress:

| Status | Criteria | Action |
|--------|----------|--------|
| **Ahead** | 3+ tasks done | Add stretch goal or bonus task |
| **On Track** | 1-2 tasks done | Continue current plan |
| **Behind** | 0 tasks done | Simplify scope or extend time |
| **Blocked** | Has blockers | Redirect to different task |

## Sprint Durations

Recommended sprint lengths:
- **30 minutes** - Quick tasks, bug fixes
- **60 minutes** - Standard (most common)
- **90 minutes** - Complex features

## Files

```
phase4-agent-launcher/
├── SKILL.md                    # Skill definition
├── README.md                   # This file
└── scripts/
    ├── workflow_state.py       # State management utility
    └── launcher.py             # Main launcher implementation
```

## Integration with Workflow

```
Phase 3 (codex-review)
    ↓
    Creates AGENT_PROMPTS/*.md files
    ↓
Phase 4 (agent-launcher)  ← YOU ARE HERE
    ↓
    • Launch agents in parallel
    • Track sprint progress
    • Re-evaluate and adjust
    ↓
Phase 5 (integration)
    Merge all agent PRs
```

## Example Workflow

1. **Complete Phase 3**: Generate agent prompts
2. **Launch agents**: Run `launcher.launch_agents(60)`
3. **Copy prompts**: Paste each to separate Claude chat
4. **Wait for sprint**: Let agents work for 60 minutes
5. **Collect reports**: Ask each agent for progress
6. **Evaluate**: Run `launcher.evaluate_progress(reports, 60)`
7. **Copy updated prompts**: Paste to each agent's chat
8. **Repeat**: Continue sprint cycles until complete
9. **Move to Phase 5**: Merge all PRs

## CLI Reference

```bash
# Show status
python scripts/launcher.py <project_path> status

# Launch agents
python scripts/launcher.py <project_path> launch [sprint_duration]

# Evaluate progress
python scripts/launcher.py <project_path> evaluate <reports_file> [next_sprint]
```

## State File Format

The launcher reads/writes `WORKFLOW_STATE.json`:

```json
{
  "project": "my-project",
  "phase": 4,
  "status": "agents_launched",
  "repo_url": "https://github.com/user/repo",
  "agents": [
    {
      "id": 1,
      "role": "Backend Developer",
      "status": "in_progress",
      "started_at": "2025-11-18T10:00:00",
      "completed_at": null,
      "pr_number": null
    }
  ]
}
```

## Troubleshooting

**No agents found**
- Ensure Phase 3 completed successfully
- Check `WORKFLOW_STATE.json` has `agents` array

**Agent prompt files missing**
- Verify `AGENT_PROMPTS/` directory exists
- Check agent prompt files match pattern: `{id}_{role}.md`

**Report parsing fails**
- Ensure agents use the standard report format
- Check for emoji markers: ✅ 🔄 ⚠️ ⏭️

## Key Principles

1. **Sprints not marathons** - 30-60 min check-ins keep momentum
2. **Dynamic adjustment** - Redirect based on actual progress
3. **Unblock quickly** - Don't let agents wait on each other
4. **Celebrate wins** - Acknowledge completed work
5. **Stay flexible** - Adapt plan to reality

## License

Part of the AgentOrchestratedCodeFactory project.
