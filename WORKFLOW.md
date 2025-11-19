# Multi-Agent Workflow Guide

This project uses the multi-agent workflow system.

## Quick Commands

### Status & Planning
```bash
# Check current status
python skills/workflow-state/workflow-state/scripts/workflow_state.py .

# Get next action
python skills/workflow-state/workflow-state/scripts/workflow_state.py . next-step

# Validate current phase
python skills/workflow-state/workflow-state/scripts/workflow_state.py . validate
```

### Quality & Metrics
```bash
# Collect metrics
python scripts/collect_metrics.py

# Run quality audit
./scripts/auto_quality_audit.sh

# Generate dashboard
python scripts/generate_dashboard.py
cat DASHBOARD.md
```

### PR Management
```bash
# Determine merge order
python scripts/determine_merge_order.py
cat merge_order.txt
```

### Agent Management
```bash
# Block an agent
python skills/workflow-state/workflow-state/scripts/workflow_state.py . block --agent-id 1 --reason "Waiting for API"

# Unblock an agent
python skills/workflow-state/workflow-state/scripts/workflow_state.py . unblock --agent-id 1

# List blocked agents
python skills/workflow-state/workflow-state/scripts/workflow_state.py . blocked
```

## Templates

Templates are available in the `templates/` directory:
- `IMPROVEMENT_PROPOSAL.md` - For Phase 3 code review suggestions
- `PR_TEMPLATE.md` - For Phase 5 pull requests
- `STUB_TEMPLATE_PYTHON.py` - For creating Python interface stubs
- `STUB_TEMPLATE_JAVASCRIPT.js` - For creating JS/TS interface stubs

## Agent Learnings

Refer to `AGENT_LEARNINGS/MASTER_LEARNINGS.md` for accumulated knowledge and best practices.

## Workflow Phases

1. **Phase 1**: Requirements Analysis
2. **Phase 2**: Architecture Design
3. **Phase 3**: Code Review
4. **Phase 4**: Implementation
5. **Phase 5**: Integration
6. **Phase 6**: QA Testing

For detailed documentation, see the main toolkit repository.
