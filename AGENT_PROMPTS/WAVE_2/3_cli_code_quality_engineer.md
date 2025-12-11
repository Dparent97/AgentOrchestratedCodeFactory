# Agent 3: CLI & Code Quality Engineer

## Mission
Add the `generate` CLI command and fix duplicate model definitions.

## Repository
- URL: https://github.com/dp/AgentOrchestratedCodeFactory
- Branch: `improve/3-cli-generate-command`

## Your Task
The CLI only has `init`, `status`, and `version` commands. The core `generate` command to actually run the factory is missing. Additionally, `models.py` has duplicate class definitions that need fixing.

## Approach

### Part 1: Fix Duplicate Models
1. Open `src/code_factory/core/models.py`
2. Find duplicate definitions of `PlanResult` (lines ~261 and ~315)
3. Find duplicate definitions of `ArchitectResult` (lines ~291 and ~345)
4. Remove the duplicate definitions (keep the first occurrence)
5. Run tests to verify no breakage

### Part 2: Add Generate Command
1. Open `src/code_factory/cli/main.py`
2. Add `@app.command()` for `generate`:
   ```python
   @app.command()
   def generate(
       description: str = typer.Argument(..., help="Project description"),
       output_dir: Optional[Path] = typer.Option(None, help="Output directory"),
       features: Optional[List[str]] = typer.Option(None, help="Features"),
   ):
   ```
3. Create Idea from CLI args
4. Initialize runtime with get_runtime()
5. Create Orchestrator and call run_factory()
6. Display results with Rich formatting

## Files to Modify
- `src/code_factory/core/models.py` (remove duplicates)
- `src/code_factory/cli/main.py` (add generate command)

## CLI UX Requirements
- Show spinner during generation with `console.status()`
- Display each pipeline stage as it completes
- Show final summary: project path, files created, time taken
- Handle errors gracefully with helpful messages

## Time Estimate
1-2 hours

## Definition of Done
- [ ] Duplicate model definitions removed from models.py
- [ ] `code-factory generate "description"` command works
- [ ] CLI shows progress during generation
- [ ] CLI displays clear success/failure output
- [ ] `code-factory generate --help` shows usage
- [ ] Existing tests still pass
- [ ] PR created with descriptive title

## START NOW
