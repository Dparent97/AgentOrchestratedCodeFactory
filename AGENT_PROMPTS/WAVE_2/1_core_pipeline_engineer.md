# Agent 1: Core Pipeline Engineer

## Mission
Wire the orchestrator pipeline to connect all agents into a functioning code generation system.

## Repository
- URL: https://github.com/dp/AgentOrchestratedCodeFactory
- Branch: `improve/1-wire-orchestrator-pipeline`

## Your Task
The `Orchestrator.run_factory()` method has 7 TODO stubs where agent execution should happen. Currently, the pipeline logs stages but doesn't actually call any agents. Wire up the complete pipeline: safety validation → planning → architecture → implementation → testing → documentation → git initialization.

## Approach
1. Read `src/code_factory/core/orchestrator.py` and understand the pipeline stages
2. Review how `AgentRuntime.execute_agent()` works in `agent_runtime.py`
3. Wire Stage 1: Execute SafetyGuard, abort if not approved
4. Wire Stage 2: Execute PlannerAgent with the idea
5. Wire Stage 3: Execute ArchitectAgent with idea + tasks
6. Wire Stage 4: Execute ImplementerAgent with ProjectSpec
7. Wire Stage 5-7: Execute TesterAgent, DocWriterAgent, GitOpsAgent
8. Create project directory, write generated files to disk
9. Ensure proper error handling and checkpoint creation

## Files to Modify
- `src/code_factory/core/orchestrator.py` (main work)
- `src/code_factory/core/code_writer.py` (may need updates for file writing)

## Key Integration Points
- SafetyGuard returns `SafetyCheck` - check `approved` field
- PlannerAgent returns `PlanResult` with `tasks` list
- ArchitectAgent returns `ArchitectResult` with `spec` field
- ImplementerAgent returns `CodeOutput` with `files` dict
- Use `self.runtime.execute_agent(agent_name, input_data)` pattern

## Time Estimate
2-3 hours

## Definition of Done
- [ ] All 7 pipeline stages execute real agents
- [ ] SafetyGuard rejection stops pipeline with clear error
- [ ] Generated files are written to project directory
- [ ] Pipeline creates checkpoint at key stages
- [ ] Error in any stage triggers `handle_failure()`
- [ ] Existing tests still pass
- [ ] PR created with descriptive title

## START NOW
