# Agent 2: Agent Implementation Engineer

## Mission
Complete the stub implementations for TesterAgent, DocWriterAgent, and BlueCollarAdvisor.

## Repository
- URL: https://github.com/dp/AgentOrchestratedCodeFactory
- Branch: `improve/2-complete-agent-implementations`

## Your Task
Three agents have TODO stubs instead of real implementations:
- `TesterAgent`: Should generate pytest test files based on ProjectSpec
- `DocWriterAgent`: Should generate README.md and usage documentation
- `BlueCollarAdvisor`: Should analyze specs for field-worker usability

## Approach
1. Study working agents (PlannerAgent, ArchitectAgent, SafetyGuard) for patterns
2. **TesterAgent** (`src/code_factory/agents/tester.py`):
   - Accept ProjectSpec as input
   - Generate test files for each source file in spec
   - Create pytest-compatible test structure
   - Return TestResult with file count
3. **DocWriterAgent** (`src/code_factory/agents/doc_writer.py`):
   - Accept ProjectSpec + optional AdvisoryReport
   - Generate README.md with sections: description, install, usage, API
   - Return dict of doc files (path → content)
4. **BlueCollarAdvisor** (`src/code_factory/agents/blue_collar_advisor.py`):
   - Accept ProjectSpec as input
   - Analyze for: offline capability, simple UI, error tolerance, large buttons/text
   - Return AdvisoryReport with recommendations, warnings, accessibility_score

## Files to Modify
- `src/code_factory/agents/tester.py`
- `src/code_factory/agents/doc_writer.py`
- `src/code_factory/agents/blue_collar_advisor.py`

## Reference Patterns
Look at these for implementation patterns:
- `src/code_factory/agents/planner.py` - task generation logic
- `src/code_factory/agents/architect.py` - spec analysis patterns
- `src/code_factory/core/models.py` - data models (TestResult, AdvisoryReport)

## Time Estimate
2-3 hours

## Definition of Done
- [ ] TesterAgent generates valid pytest test files
- [ ] DocWriterAgent generates comprehensive README.md
- [ ] BlueCollarAdvisor returns meaningful usability analysis
- [ ] All three agents pass through AgentRuntime.execute_agent()
- [ ] Unit tests added for each agent
- [ ] Existing tests still pass
- [ ] PR created with descriptive title

## START NOW
