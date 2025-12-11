# Agent 4: QA & Documentation Engineer

## Mission
Update tests and documentation for the new pipeline functionality.

## Repository
- URL: https://github.com/dp/AgentOrchestratedCodeFactory
- Branch: `improve/4-tests-and-docs`

## Your Task
With the orchestrator wired, agents implemented, and CLI updated, tests and docs need updates to reflect the new functionality. Focus on integration tests that verify the complete pipeline works end-to-end.

## Approach

### Part 1: Update Integration Tests
1. Review `tests/integration/test_pipeline.py`
2. Add tests that verify:
   - Complete pipeline executes all stages
   - SafetyGuard rejection stops pipeline
   - Each agent receives correct input from previous stage
   - Files are actually written to disk
3. Update `tests/e2e/test_factory_run.py` for real runs

### Part 2: Update Unit Tests
1. Add tests for TesterAgent in `tests/unit/test_agents.py`
2. Add tests for DocWriterAgent
3. Add tests for BlueCollarAdvisor
4. Update orchestrator tests for wired pipeline

### Part 3: Update Documentation
1. Update `docs/cli_usage.md` with generate command
2. Update `docs/architecture.md` if pipeline changed
3. Update main `README.md` Quick Start section
4. Add example usage to docs

## Files to Modify
- `tests/integration/test_pipeline.py`
- `tests/e2e/test_factory_run.py`
- `tests/unit/test_agents.py`
- `docs/cli_usage.md`
- `docs/architecture.md`
- `README.md`

## Test Coverage Goals
- Maintain >80% coverage (configured in pyproject.toml)
- All new agent methods have unit tests
- At least one happy-path integration test
- At least one error-handling test

## Time Estimate
2-3 hours

## Definition of Done
- [ ] Integration tests verify complete pipeline
- [ ] Unit tests added for new agent implementations
- [ ] CLI generate command documented
- [ ] README Quick Start updated with generate example
- [ ] All tests pass with >80% coverage
- [ ] PR created with descriptive title

## START NOW
