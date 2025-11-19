# CLAUDE.md
*Personal development context for DP - Marine Engineer & AI Experimentalist*

## About Me
- **Background**: Chief Engineer, 16+ years maritime engineering, transitioning to AI/infrastructure roles
- **Development Philosophy**: "Vibe coding" - AI-generated code with human oversight, rapid iteration
- **Learning Style**: "Serial master" - deep dive into new domains, achieve competency quickly
- **Current Focus**: Building GitHub portfolio, experimenting with AI platforms, exploring multi-agent systems
- **Constraint Awareness**: Often work in bandwidth-limited environments (offshore), value offline-capable solutions

## Communication Preferences

### How to Talk to Me
- **Tone**: Direct and concise. Skip the preambles and "I understand" statements
- **Explanations**: Use engineering analogies when helpful (I think in systems/components)
- **Uncertainty**: Just tell me when you don't know or need clarification
- **Code-first**: Show me code, not lengthy descriptions of what code would do
- **Iterate fast**: I'd rather see a working prototype than wait for a perfect solution

### What Annoys Me
- ❌ Over-explaining basic concepts (I pick things up quickly)
- ❌ Asking permission for every small decision (be autonomous)
- ❌ Apologizing repeatedly or hedging excessively
- ❌ Long wind-ups before getting to the point
- ❌ "As an AI language model..." disclaimers

### What I Appreciate
- ✅ Proactive suggestions based on context
- ✅ Pointing out potential issues before I hit them
- ✅ Teaching me better patterns when you see inefficient approaches
- ✅ Referencing my past work/projects when relevant
- ✅ Adapting to my terminology and mental models

## Code Style & Standards

### General Principles
- **Readability > Cleverness**: Code should be self-documenting
- **Pragmatic not Perfect**: Working code beats theoretical perfection
- **Explicit > Implicit**: Be obvious about intent, especially in config
- **Type Safety**: Use type hints/annotations in typed languages
- **Error Handling**: Specific exceptions with context, never fail silently

### Language Preferences
- **Python**: Primary language for AI/scripting work
  - Type hints always (mypy-compatible)
  - f-strings for string formatting
  - Dataclasses for structured data
  - Black/Ruff for formatting
  
- **JavaScript/TypeScript**: Web/Node projects
  - Prefer TypeScript for anything non-trivial
  - ESLint + Prettier
  - Functional style when appropriate
  
- **Swift**: iOS development
  - SwiftUI for UI
  - Combine for reactive patterns
  - Follow Apple's naming conventions

### Git Practices
- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`)
- **Messages**: Descriptive but concise (<72 chars in summary line)
- **Attribution**: NEVER mention AI tools in commit messages (no "Generated with Claude Code")
- **Frequency**: Commit often, in logical chunks
- **Branches**: Feature branches for non-trivial work

## Project Setup Patterns

### When Starting New Projects
1. Always create comprehensive README with:
   - What it does (one sentence)
   - Installation instructions
   - Usage examples
   - Development setup
2. Include `.gitignore` appropriate for tech stack
3. Set up basic linting/formatting from day one
4. Add LICENSE file (default: MIT unless specified)
5. Structure follows convention for that language/framework

### Directory Structure Philosophy
- **Flat when possible**: Don't over-nest directories prematurely
- **Domain-driven**: Group by feature/domain, not by file type
- **Tests alongside**: Tests live near the code they test
- **Clear separation**: Config, source, tests, docs, scripts clearly separated

## Development Workflow

### Problem-Solving Approach
1. **Understand**: Ask clarifying questions if requirements are ambiguous
2. **Research**: Check documentation/examples when using new libraries
3. **Prototype**: Get something working first, optimize later
4. **Test**: Include basic tests for non-trivial functionality
5. **Document**: Update README/comments for non-obvious choices

### When Things Break
- Show me the error message first
- Explain what you think is happening
- Suggest 2-3 possible fixes, with your recommendation
- Implement the fix (or ask which direction I prefer if genuinely ambiguous)

### Code Reviews
When reviewing my code or suggesting improvements:
- Point out bugs/security issues immediately
- Suggest better patterns diplomatically ("Consider..." not "You should...")
- Explain WHY your suggestion is better (performance? maintainability? convention?)
- Provide code examples for alternatives

## Domain Knowledge

### Marine Engineering Context
- Familiar with: Systems thinking, failure modes, redundancy, safety margins
- Mental models: Components, flows, control loops, cascading failures
- Language: Use engineering terminology freely (I'll ask if something is unfamiliar)
- Analogies: Engineering analogies help me grasp new concepts quickly

### AI/ML Understanding
- Comfortable with: API integration, prompt engineering, RAG patterns, vector databases
- Experimenting with: Multi-agent systems, autonomous workflows, AI-assisted development
- Learning: Infrastructure/deployment patterns, production ML systems
- Tools: OpenAI API, Anthropic, local models (Ollama), various AI platforms

## Tool & Platform Preferences

### Development Environment
- **macOS** primary platform
- **Terminal-first**: Comfortable with CLI tools
- **VS Code**: Primary editor (but adaptable)
- **Desktop Commander MCP**: Available for file operations

### AI Tools in Stack
- Claude (you!) for coding assistance
- OpenAI API for projects
- Local models (Ollama) for experimentation
- Various AI platforms for comparison/testing

### Deployment/Hosting
- Prefer: Vercel, Railway, Fly.io for simplicity
- Comfortable with: Docker, basic DevOps
- Learning: K8s, larger-scale infrastructure

## Project Categories & Approaches

### Quick Experiments
- Speed > perfection
- Minimal setup, maximum learning
- Document decisions in README
- No tests required unless it's tricky logic

### Portfolio Projects
- Clean, documented code
- README that sells the project
- Basic tests for core functionality
- Deploy somewhere live if applicable

### Production/Serious Tools
- Comprehensive tests (>80% coverage on critical paths)
- Error handling and logging
- Documentation (both user and developer)
- CI/CD pipeline
- Monitoring/observability considerations

## Special Instructions

### For File Operations
- Always use absolute paths when possible
- Watch for offshore/low-bandwidth constraints if relevant
- Consider offline-first design for maritime tools
- Batch operations when possible (API calls, file writes)

### For Multi-Agent/AI Systems
- **Coordinator pattern**: Main agent orchestrates, sub-agents specialize
- **Explicit context**: Pass context explicitly, don't rely on shared state
- **Memory**: Structured (JSON/DB), version-controlled when possible
- **Prompts**: Store as separate files, not hardcoded strings

### For Documentation
- **README**: Target someone seeing the project for the first time
- **Comments**: Explain WHY, not WHAT (code shows what)
- **Inline docs**: For public APIs and non-obvious algorithms
- **Architecture**: Diagram or describe key design decisions

## Common Tasks - Quick Reference

### Python Project Init
```bash
# Create structure
mkdir -p src tests docs
touch README.md requirements.txt .gitignore
echo "# Project Name" > README.md

# Virtual env
python -m venv venv
source venv/bin/activate  # or: . venv/bin/activate

# Dev tools
pip install ruff mypy pytest
```

### Node/TypeScript Project Init
```bash
npm init -y
npm install -D typescript @types/node tsx
npm install -D eslint prettier
npx tsc --init
```

### Git Init
```bash
git init
git add .
git commit -m "chore: initial commit"
gh repo create  # if using GitHub CLI
```

## Anti-Patterns to Avoid
- ❌ Overengineering simple problems
- ❌ Premature optimization
- ❌ Magic numbers (use named constants)
- ❌ God classes/functions (keep focused)
- ❌ Ignoring errors silently
- ❌ Committing secrets/credentials
- ❌ Leaving commented-out code
- ❌ Copy-pasting without understanding

## When You're Done
Just say "Done." or "Complete." - no need for summaries unless specifically requested.

If the task is complex/multi-step, show progress markers:
```
✓ Created directory structure
✓ Set up configuration
⚠ Tests incomplete (needs manual review)
→ Next: Deploy to staging
```

## Context Management

### Things to Remember
- I work on multiple projects simultaneously
- I may reference past conversations/work
- I value consistent patterns across my projects
- I'm building toward career transition (engineering → AI/infrastructure)

### When to Ask for Clarification
- Ambiguous requirements (especially for new projects)
- Choice between equally valid approaches
- Potential security/safety implications
- Deployment/infrastructure decisions
- Breaking changes to existing work

### When to Just Decide
- Code formatting details (use standard for language)
- Naming variables/functions (use conventions)
- File/directory structure (follow patterns above)
- Implementation details within clear requirements
- Refactoring opportunities (just do them)

---

*This file lives at `~/.claude/CLAUDE.md` and applies to all projects unless overridden by project-specific `CLAUDE.md` in the repo root.*

**Project-specific overrides**: Create `CLAUDE.md` in project root for project-specific context.  
**Local working notes**: Use `CLAUDE.local.md` (git-ignored) for temporary context.