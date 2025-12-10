# Master Learnings Index

**Last Updated:** YYYY-MM-DD
**Purpose:** Central index of all agent learnings across the multi-agent workflow system.

---

## How to Use This Index

1. **Before Starting Work:** Review relevant sections to avoid repeating past mistakes
2. **During Work:** Reference role-specific and category-specific learnings
3. **After Completing Work:** Update appropriate learning files with new insights
4. **When Blocked:** Check if similar issues were solved before

---

## Quick Links

- [Universal Patterns](UNIVERSAL_PATTERNS.md) - Cross-project rules that apply everywhere
- [Iteration Template](ITERATION_TEMPLATE.md) - Template for capturing learnings at end of each cycle

---

## Learnings by Role

### Phase 1: Requirements Analyst
**File:** [BY_ROLE/requirements_analyst.md](BY_ROLE/requirements_analyst.md)

**Key Topics:**
- User story decomposition
- Acceptance criteria definition
- Edge case identification
- Requirement ambiguity resolution

**Last Updated:** [Date]

---

### Phase 2: Architect
**File:** [BY_ROLE/architect.md](BY_ROLE/architect.md)

**Key Topics:**
- System design patterns
- Technology selection criteria
- Scalability considerations
- Integration points

**Last Updated:** [Date]

---

### Phase 3: Code Reviewer
**File:** [BY_ROLE/code_reviewer.md](BY_ROLE/code_reviewer.md)

**Key Topics:**
- Review checklist
- Common code smells
- Performance anti-patterns
- Security vulnerabilities to watch for

**Last Updated:** [Date]

---

### Phase 4: Implementation Agents
**File:** [BY_ROLE/implementation_agent.md](BY_ROLE/implementation_agent.md)

**Key Topics:**
- Coding standards
- Testing practices
- Error handling patterns
- Documentation requirements

**Last Updated:** [Date]

---

### Phase 5: Integration Manager
**File:** [BY_ROLE/integration_manager.md](BY_ROLE/integration_manager.md)

**Key Topics:**
- Merge conflict resolution
- Dependency management
- Integration testing
- Rollback procedures

**Last Updated:** [Date]

---

### Phase 6: QA Engineer
**File:** [BY_ROLE/qa_engineer.md](BY_ROLE/qa_engineer.md)

**Key Topics:**
- Test case design
- Regression testing
- Performance testing
- Bug reporting standards

**Last Updated:** [Date]

---

## Learnings by Category

### Testing
**File:** [BY_CATEGORY/testing.md](BY_CATEGORY/testing.md)
- Unit testing best practices
- Integration testing strategies
- Mocking and stubbing techniques
- Test coverage targets

---

### Security
**File:** [BY_CATEGORY/security.md](BY_CATEGORY/security.md)
- Common vulnerabilities (OWASP Top 10)
- Input validation
- Authentication/Authorization
- Dependency security

---

### Performance
**File:** [BY_CATEGORY/performance.md](BY_CATEGORY/performance.md)
- Optimization techniques
- Profiling tools
- Caching strategies
- Database query optimization

---

### Documentation
**File:** [BY_CATEGORY/documentation.md](BY_CATEGORY/documentation.md)
- Code documentation standards
- API documentation
- README best practices
- Diagram creation

---

### Error Handling
**File:** [BY_CATEGORY/error_handling.md](BY_CATEGORY/error_handling.md)
- Exception handling patterns
- Logging best practices
- Error recovery strategies
- User-facing error messages

---

### Code Quality
**File:** [BY_CATEGORY/code_quality.md](BY_CATEGORY/code_quality.md)
- Linting rules
- Code style guidelines
- Refactoring techniques
- Technical debt management

---

## Learnings by Language

### Python
**File:** [BY_LANGUAGE/python.md](BY_LANGUAGE/python.md)
- Python-specific idioms
- Common pitfalls
- Library recommendations
- Performance tips

---

### JavaScript/TypeScript
**File:** [BY_LANGUAGE/javascript.md](BY_LANGUAGE/javascript.md)
- JS/TS best practices
- Async/await patterns
- Framework-specific learnings
- Build tool configurations

---

### [Other Languages]
**File:** [BY_LANGUAGE/other.md](BY_LANGUAGE/other.md)
- Add as needed based on project

---

## Cross-Cutting Concerns

### Communication Between Agents
- Use standardized templates (see `/templates`)
- Always include context in handoffs
- Document assumptions explicitly
- Use PR template learnings section

### Workflow Process
- Follow phase sequence strictly
- Don't skip validation steps
- Document all decisions
- Keep state updated

### Common Anti-Patterns
1. **Skipping Phase 3 Review** - Always get code reviewed before implementation
2. **Parallel Work Without Stubs** - Use stub templates to prevent blocking
3. **Incomplete PR Descriptions** - Always fill out PR template completely
4. **Ignoring Past Learnings** - Check this index before starting work

---

## Recent Critical Learnings

**[Date]:** [Brief description of critical learning]
- **Issue:** [What went wrong]
- **Resolution:** [How it was fixed]
- **Prevention:** [How to avoid in future]
- **Reference:** [Link to detailed documentation]

---

## Maintenance Guidelines

### When to Update
- End of each iteration (use ITERATION_TEMPLATE.md)
- After resolving a significant bug
- When discovering a new pattern
- After completing a challenging feature

### How to Update
1. Identify the appropriate file (by role, category, or language)
2. Add learning with clear context
3. Update "Last Updated" date
4. Add entry to "Recent Critical Learnings" if significant
5. Update UNIVERSAL_PATTERNS.md if pattern applies broadly

### Quality Standards
- Be specific, not vague
- Include examples when possible
- Link to relevant code/PRs
- Keep entries concise but complete

---

## Metrics

**Total Learning Entries:** [Number]
**Last Iteration Review:** [Date]
**Most Referenced Category:** [Category]
**Most Common Issue Type:** [Type]

---

*This is a living document. All agents should contribute learnings to improve the collective knowledge base.*
