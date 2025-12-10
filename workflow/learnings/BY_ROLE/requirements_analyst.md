# Requirements Analyst Learnings

**Role:** Phase 1 - Requirements Analysis
**Last Updated:** YYYY-MM-DD

---

## Role Overview

**Responsibilities:**
- Decompose user requests into clear, actionable requirements
- Define acceptance criteria
- Identify edge cases and constraints
- Create detailed specifications for the Architect

**Success Criteria:**
- Requirements are unambiguous
- All edge cases identified
- Acceptance criteria are testable
- Specifications are complete enough for design

---

## Best Practices

### 1. Requirement Decomposition

**Pattern: User Story Breakdown**
- Break large requests into user stories
- Use "As a [role], I want [feature], so that [benefit]" format
- Ensure each story is independently valuable

**Example:**
```
User Request: "Build a dashboard"

Broken Down:
- As a user, I want to see my key metrics at a glance, so I can monitor system health
- As a user, I want to customize which metrics appear, so I can focus on what matters to me
- As a user, I want to set alert thresholds, so I'm notified of issues
```

---

### 2. Acceptance Criteria Definition

**Pattern: Given-When-Then**
```
Given [initial context]
When [action occurs]
Then [expected outcome]
```

**Example:**
```
Given the user is logged in
When they click "Export Data"
Then a CSV file downloads containing all visible data
And the file is named "export_YYYY-MM-DD.csv"
And the download completes within 5 seconds for datasets under 10k rows
```

---

### 3. Edge Case Identification

**Checklist:**
- [ ] Empty state (no data)
- [ ] Error state (network failure, server error)
- [ ] Loading state
- [ ] Maximum capacity (what's the limit?)
- [ ] Invalid input (malformed data)
- [ ] Permission denied
- [ ] Concurrent access
- [ ] Browser/platform compatibility

---

## Common Pitfalls

### ❌ Pitfall 1: Vague Requirements
**Problem:** "Make it fast"
**Why It's Bad:** "Fast" is subjective and unmeasurable
**Fix:** "Page load time under 2 seconds for 95th percentile users"

---

### ❌ Pitfall 2: Mixing Requirements with Implementation
**Problem:** "Use a Redis cache for the user session"
**Why It's Bad:** Prescribes solution instead of stating need
**Fix:** "User session must persist across page refreshes for 30 days"

---

### ❌ Pitfall 3: Implicit Assumptions
**Problem:** "Users can edit their profile"
**Missing:** Can all users edit? Can they edit all fields? Any validation?
**Fix:** "Authenticated users can edit their own profile's name, email, and bio. Email must be validated. Users cannot edit their username or registration date."

---

### ❌ Pitfall 4: Non-Testable Criteria
**Problem:** "The UI should be intuitive"
**Why It's Bad:** Cannot be objectively verified
**Fix:** "Users can complete task X without consulting documentation (measured via user testing)"

---

## Learnings from Past Iterations

### Learning 1: [Title]
**Date:** YYYY-MM-DD
**Context:** [What was the situation]
**Issue:** [What went wrong]
**Resolution:** [How it was fixed]
**Takeaway:** [What to do differently]

---

### Learning 2: [Title]
**Date:** YYYY-MM-DD
**Context:**
**Issue:**
**Resolution:**
**Takeaway:**

---

## Templates and Tools

### Requirement Document Template
```markdown
# Requirement: [Title]

## Description
[Clear description of what is needed]

## User Story
As a [role]
I want [feature]
So that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Edge Cases
- Case 1: [description]
- Case 2: [description]

## Constraints
- Technical: [e.g., must work on mobile]
- Business: [e.g., must comply with GDPR]
- Performance: [e.g., must load in <2s]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Out of Scope
- [What is explicitly NOT included]
```

---

## Questions to Always Ask

1. **Who is the user?** (Persona, role, permissions)
2. **What problem are we solving?** (The "why")
3. **What does success look like?** (Measurable outcomes)
4. **What are the constraints?** (Time, tech, budget)
5. **What happens in error cases?** (Edge cases)
6. **What's explicitly out of scope?** (Prevent scope creep)

---

## Handoff Checklist

Before passing to Phase 2 (Architect):
- [ ] All user stories documented
- [ ] Acceptance criteria defined for each story
- [ ] Edge cases identified
- [ ] Constraints listed
- [ ] Dependencies mapped
- [ ] Out-of-scope items explicitly stated
- [ ] Reviewed with stakeholder (if applicable)

---

## Metrics to Track

- **Requirement Clarity Score:** (subjective, 1-5) How clear were requirements to downstream phases?
- **Rework Rate:** % of requirements that needed clarification during implementation
- **Edge Cases Found Later:** Number of edge cases discovered after Phase 1 (should be minimized)

---

## Related Resources

- [UNIVERSAL_PATTERNS.md](../UNIVERSAL_PATTERNS.md) - Cross-cutting best practices
- [templates/IMPROVEMENT_PROPOSAL.md](../../templates/IMPROVEMENT_PROPOSAL.md) - For proposing process improvements
- [Phase 2 Architect Learnings](architect.md) - Understanding downstream needs

---

*Keep this document updated with new learnings from each iteration.*
