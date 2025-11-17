# Project Summary: Agent-Orchestrated Code Factory

## Mission

Transform the way practical software is built by creating an intelligent meta-agent system that can generate complete, tested, documented software projects from plain-language descriptions—with a specific focus on tools that help blue-collar and technical workers in the field.

## Core Problem

Technical workers (marine engineers, plant operators, mechanics, HVAC technicians) often need custom software tools but:
- Don't have time to learn programming
- Can't afford custom development
- Work in challenging environments (noisy, poor connectivity, hands dirty)
- Need solutions that "just work" without fancy features

Meanwhile, building even simple utility software takes days or weeks of development time.

## Solution

The Agent-Orchestrated Code Factory automates the entire software creation pipeline:

1. **Human provides idea**: "I need a tool to parse PLC alarm logs and highlight critical errors"
2. **PlannerAgent** breaks it into tasks
3. **ArchitectAgent** designs the structure (CLI? Web app? What libraries?)
4. **ImplementerAgent** writes the code
5. **TesterAgent** creates and runs tests
6. **DocWriterAgent** generates README and usage docs
7. **GitOpsAgent** initializes version control and pushes to GitHub
8. **BlueCollarAdvisor** ensures the solution fits real-world workflows
9. **SafetyGuard** prevents dangerous or out-of-scope operations

Output: A complete, working repository ready for use or further customization.

## Technical Approach

- **Language**: Python 3.11+ (accessible, widely used, great for automation)
- **Agent Architecture**: Custom, minimal framework (not over-engineered)
- **CLI-First**: Built with Typer for ease of use
- **Safety-Constrained**: Only operates in designated directories
- **Git-Native**: Every project is version controlled from the start

## Success Criteria

Phase 1 (Current):
- ✅ Project scaffold and structure
- ✅ Basic CLI (init, status)
- ✅ Core agent placeholders
- ⏳ Full orchestration logic

Phase 2 (Next):
- Multi-agent task execution
- First end-to-end project generation
- Blue-collar template library

Phase 3 (Future):
- LLM integration for intelligent code generation
- Interactive refinement loop
- Community template sharing

## Key Principles

1. **Practical over fancy**: Tools must work in real conditions
2. **Safety-first**: Hard boundaries on what can be generated
3. **Transparent**: No black boxes—every step is loggable and debuggable
4. **Iterative**: Start minimal, grow based on real use
5. **Respectful**: This automates tedious work, doesn't replace human judgment

## Target Users (Personas)

### Mike - Marine Chief Engineer
- Works on cargo ships, limited shore time
- Needs: Log analysis tools, maintenance checklists, parts cross-reference
- Environment: Noisy engine room, unreliable internet, gloves on

### Sarah - HVAC Service Technician  
- Travels between job sites all day
- Needs: Quick load calculators, troubleshooting guides, code lookup
- Environment: Attics, rooftops, phone is primary device

### James - Plant Operator
- Monitors industrial processes 12-hour shifts
- Needs: Alarm pattern analysis, shift handoff notes, procedure lookup
- Environment: Control room, can't install unapproved software

## Repository Structure

```
/Users/dp/Projects/AgentOrchestratedCodeFactory/  ← This project
    ├── src/code_factory/                          ← The factory itself
    ├── docs/                                      ← Architecture & guides
    └── tests/                                     ← Quality assurance

/Users/dp/Projects/                                ← Parent directory
    ├── MarineLogAnalyzer/                         ← Generated project 1
    ├── HVACLoadCalculator/                        ← Generated project 2
    └── ...                                        ← More generated projects
```

## Current Status

**Phase**: Initial scaffold complete  
**Version**: 0.1.0  
**Next Steps**: Implement orchestrator logic and agent execution framework

---

*This is a living document. Update as the project evolves.*
