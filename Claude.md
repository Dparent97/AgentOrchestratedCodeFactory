# CLAUDE.md
*Context for AI agents working on DP's repos*

## Git - CRITICAL

**All repos use SSH authentication, not HTTPS.**

If push fails with "could not read Username":
```bash
git remote set-url origin git@github.com:Dparent97/[repo-name].git
```

## Commit Convention

```
type: short description (<72 chars)

Types: feat, fix, docs, refactor, test, chore
```

**Never mention AI/Claude in commit messages.**

## Code Style

### Python
- Type hints always
- f-strings for formatting
- Ruff/Black for formatting
- Explicit error handling

### Swift
- SwiftUI for UI
- Follow Apple naming conventions

### General
- Readability > cleverness
- Explicit > implicit
- Handle errors, never fail silently

## Branch Naming

```
improve/[N]-description   # Multi-agent improvements
feature/description       # New features
fix/description          # Bug fixes
```

## Communication

- Be direct, skip preambles
- Show code, not descriptions
- Point out issues directly
- Commit often, small logical chunks

## When Done

Just say "Done." - no summaries unless asked.

```
✓ Completed task
⚠ Needs review
→ Next step
```
