# Git Workflow for Multi-Agent Development

**Project**: Agent-Orchestrated Code Factory
**Model**: Feature Branch Workflow with Agent-Specific Branches

---

## 🌳 Branch Structure

```
main (protected)
├── backend-core-infrastructure        # Agent 1
├── llm-integration                    # Agent 2
├── agent-implementations              # Agent 3
├── testing-infrastructure             # Agent 4
└── templates-and-docs                 # Agent 5
```

---

## 📋 Branch Rules

### Main Branch
- **Protected**: No direct commits
- **Requires**: PR with passing tests
- **Reviews**: Coordinator approval required
- **CI/CD**: Must pass all checks

### Agent Branches
- **One per agent**: Each agent works in isolation
- **Naming**: Descriptive, lowercase, hyphens
- **Lifetime**: Merge after phase completion
- **Rebasing**: Rebase on main weekly to stay current

---

## 🚀 Workflow Steps

### 1. Agent Starts Work

```bash
# Clone the repository (if not already done)
git clone <repo-url>
cd AgentOrchestratedCodeFactory

# Checkout main and pull latest
git checkout main
git pull origin main

# Create your agent branch
git checkout -b [your-branch-name]

# Example for Agent 1:
git checkout -b backend-core-infrastructure
```

### 2. Daily Development

```bash
# Start of day: Pull latest from main
git fetch origin main
git rebase origin/main

# Make changes
# ... work on files ...

# Stage changes
git add src/code_factory/core/orchestrator.py

# Commit with clear message
git commit -m "feat: implement orchestrator pipeline stages"

# Push to your branch
git push origin backend-core-infrastructure
```

### 3. Handling Conflicts

If rebase has conflicts:

```bash
# During rebase, if conflicts occur:
# 1. Fix conflicts in files
# 2. Stage resolved files
git add <resolved-files>

# 3. Continue rebase
git rebase --continue

# If rebase gets too messy, abort and merge instead:
git rebase --abort
git merge origin/main
```

### 4. Keeping Branch Updated

Weekly (or when needed):

```bash
# Fetch latest main
git fetch origin main

# Rebase your branch on main
git checkout backend-core-infrastructure
git rebase origin/main

# Force push (since history changed)
git push --force-with-lease origin backend-core-infrastructure
```

### 5. Ready to Merge

When your phase is complete:

```bash
# 1. Ensure all tests pass locally
pytest tests/ -v

# 2. Ensure code style is correct
black src/ tests/
ruff check src/ tests/

# 3. Update your branch with latest main
git fetch origin main
git rebase origin/main

# 4. Push final version
git push origin backend-core-infrastructure

# 5. Notify coordinator for review
# (Post in AGENT_PROMPTS/issues/merge_request_agent1.md)
```

### 6. Coordinator Merges

Coordinator will:

```bash
# Review the branch
git checkout backend-core-infrastructure
git pull origin backend-core-infrastructure

# Run tests
pytest tests/ -v

# Merge to main
git checkout main
git merge --no-ff backend-core-infrastructure -m "Merge Agent 1: Backend Infrastructure"

# Push to main
git push origin main

# Tag the release (optional)
git tag -a v0.2.0 -m "Phase 1: Backend infrastructure complete"
git push origin v0.2.0
```

---

## 📝 Commit Message Convention

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks

### Examples

**Good commits**:
```bash
git commit -m "feat(orchestrator): implement 8-stage pipeline execution"
git commit -m "fix(agent_runtime): handle timeout errors gracefully"
git commit -m "test(orchestrator): add integration tests for pipeline"
git commit -m "docs(api): add docstrings to AgentRuntime methods"
```

**Bad commits**:
```bash
git commit -m "update stuff"
git commit -m "fix"
git commit -m "WIP"
```

---

## 🔀 Merge Strategy

### Merge Order (Critical!)

Merge agents in dependency order:

1. **Agent 1** → Backend Infrastructure
2. **Agent 2** → LLM Integration
3. **Agent 3** → Agent Implementations
4. **Agent 4** → Testing Infrastructure
5. **Agent 5** → Templates & Documentation

**Why?** Each agent depends on previous agents' work.

### Merge Checklist

Before merging any branch:

- [ ] All unit tests pass locally
- [ ] Integration tests pass (if applicable)
- [ ] Code style checks pass (black, ruff, mypy)
- [ ] No TODO or FIXME comments (unless documented)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Daily logs submitted
- [ ] Coordinator approval obtained
- [ ] No merge conflicts with main

### Merge Command

```bash
# Coordinator performs merge
git checkout main
git pull origin main
git merge --no-ff backend-core-infrastructure

# If conflicts, resolve and commit
git add <resolved-files>
git commit

# Push to main
git push origin main
```

**Use `--no-ff`** to preserve branch history and make rollbacks easier.

---

## 🚫 Conflict Prevention

### File Ownership

Each agent has exclusive ownership of certain files to minimize conflicts:

| Agent | Files |
|-------|-------|
| Agent 1 | `src/code_factory/core/` |
| Agent 2 | `src/code_factory/llm/` |
| Agent 3 | `src/code_factory/agents/` |
| Agent 4 | `tests/`, `.github/workflows/` |
| Agent 5 | `templates/`, `examples/`, `docs/` |

### Shared Files

Some files may be touched by multiple agents:

- `pyproject.toml` - Dependencies
- `README.md` - Project overview
- `src/code_factory/__init__.py` - Package exports

**Protocol for shared files**:
1. Coordinate via `AGENT_PROMPTS/questions.md`
2. Make minimal changes
3. Merge more frequently
4. Resolve conflicts immediately

---

## 🔄 Handling Dependency Changes

### If Agent 2 Changes API Used by Agent 3

**Agent 2 (LLM Specialist)**:
```bash
# Make changes to LLMClient
# Update COORDINATION.md with new API

# Post notification
echo "LLMClient API updated. New signature: ..." > AGENT_PROMPTS/issues/api_change_llm_client.md
git add AGENT_PROMPTS/issues/api_change_llm_client.md
git commit -m "docs: notify agents of LLMClient API change"
git push origin llm-integration
```

**Agent 3 (Agent Developer)**:
```bash
# Pull latest from Agent 2's branch
git fetch origin llm-integration
git merge origin/llm-integration

# Update agent code to use new API
# Test changes

# Commit
git commit -m "refactor: update agents for new LLMClient API"
```

---

## 🐛 Troubleshooting

### Problem: Merge Conflict

```bash
# During merge:
git merge origin/main
# CONFLICT (content): Merge conflict in src/code_factory/core/models.py

# Fix conflict in file
# Look for <<<<<<< HEAD markers
vim src/code_factory/core/models.py

# Stage resolved file
git add src/code_factory/core/models.py

# Complete merge
git commit
```

### Problem: Accidentally Committed to Main

```bash
# If you committed directly to main (don't do this!):
git checkout main
git log  # Find the commit hash

# Revert the commit
git revert <commit-hash>
git push origin main

# Or reset (if no one else pulled):
git reset --hard HEAD~1
git push --force origin main  # DANGEROUS!
```

### Problem: Need to Undo Last Commit

```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Undo last commit that was pushed (create reverse commit)
git revert HEAD
git push origin [branch-name]
```

### Problem: Branch Diverged from Main

```bash
# Your branch is way behind main
git fetch origin main
git rebase origin/main

# Resolve conflicts if any
# Then force push
git push --force-with-lease origin [branch-name]
```

---

## 📊 Git Best Practices

### DO ✅
- Commit frequently (multiple times per day)
- Write clear commit messages
- Rebase on main weekly
- Test before pushing
- Keep commits focused (one feature/fix per commit)
- Use meaningful branch names
- Push daily backups

### DON'T ❌
- Commit directly to main
- Force push to main
- Commit secrets or API keys
- Make huge commits (>500 lines changed)
- Leave "WIP" or "test" commits
- Ignore conflicts and hope they go away

---

## 🔐 Security

### Never Commit
- API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY)
- Passwords or credentials
- `.env` files
- Private keys or certificates

### If You Accidentally Commit a Secret
```bash
# Remove from history (nuclear option)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push all branches
git push --force --all

# IMPORTANT: Rotate the compromised secret immediately!
```

**Better**: Use `.gitignore` to prevent committing secrets:
```
# .gitignore
.env
*.key
*.pem
credentials.json
```

---

## 📈 Monitoring Progress

### View Agent Progress

```bash
# See all branches
git branch -a

# See commits on agent branch
git log backend-core-infrastructure --oneline

# See diff from main
git diff main..backend-core-infrastructure

# See changed files
git diff --name-only main..backend-core-infrastructure
```

### View Merge History

```bash
# See all merges to main
git log --merges --oneline

# See what's been merged
git branch --merged main
```

---

## 🏷️ Tagging Releases

After each phase:

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Phase 1 Complete: Backend & LLM Infrastructure"

# Push tag
git push origin v0.2.0

# List tags
git tag -l
```

**Versioning Scheme**:
- v0.1.0 - Initial scaffold
- v0.2.0 - Phase 1 complete
- v0.3.0 - Phase 2 complete
- v0.4.0 - Phase 3 complete
- v0.5.0 - Phase 4 complete
- v1.0.0 - Production ready

---

## 📞 Getting Help

**Conflicts or Issues?**
1. Post in `AGENT_PROMPTS/issues/`
2. Ask coordinator
3. Reference this guide

**Git Commands Reference**:
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)

---

## Quick Reference Card

```bash
# Start
git checkout -b my-agent-branch

# Daily work
git add .
git commit -m "feat: add feature"
git push origin my-agent-branch

# Update from main
git fetch origin main
git rebase origin/main

# Ready to merge
pytest tests/ -v  # Must pass
git push origin my-agent-branch
# Notify coordinator

# Coordinator merges
git checkout main
git merge --no-ff my-agent-branch
git push origin main
```

---

**Remember**: Communication is key. When in doubt, ask in `AGENT_PROMPTS/questions.md`!
