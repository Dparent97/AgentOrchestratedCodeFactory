# Safety Guidelines

## Core Safety Principles

The Agent-Orchestrated Code Factory is designed to generate **decision support tools**, not autonomous control systems. Safety is enforced through multiple layers:

1. **Scope Boundaries**: Strict file system access controls
2. **SafetyGuard Agent**: Pre-execution validation of all ideas
3. **Human Confirmation**: Required for risky operations
4. **Audit Logging**: Complete record of all operations

---

## What This Factory DOES NOT Do

### ❌ Equipment Control

The factory will **NEVER** generate code that:
- Controls physical equipment (motors, pumps, valves, actuators)
- Modifies PLC programs or industrial control systems
- Interfaces with SCADA or DCS systems for write operations
- Overrides safety interlocks or emergency stops
- Sends commands to machinery or robots

**Why**: Physical safety is paramount. Generated tools are for information and analysis only.

### ❌ Safety System Modification

The factory will **NEVER** generate code that:
- Bypasses safety interlocks
- Disables alarms or warnings
- Modifies fail-safe logic
- Circumvents access controls
- Suppresses safety-critical notifications

**Why**: Safety systems exist for a reason. We support workers, not endanger them.

### ❌ Exploit or Malicious Code

The factory will **NEVER** generate:
- Malware, viruses, or ransomware
- Vulnerability scanners or exploit tools
- Password crackers or keyloggers
- Network intrusion tools
- Code obfuscation for malicious purposes

**Why**: Ethical obligation. This is a tool for building, not breaking.

### ❌ Unauthorized System Access

The factory will **NEVER**:
- Modify system files outside `/Users/dp/Projects`
- Change system configurations
- Install global packages without permission
- Access files in other users' directories
- Modify system security settings

**Why**: System stability and security. The factory operates in a sandbox.

---

## What This Factory DOES

### ✅ Analysis and Monitoring Tools

Generate tools that:
- Parse and analyze log files
- Visualize data trends
- Monitor system status (read-only)
- Generate reports and summaries
- Detect patterns and anomalies

**Examples**:
- "Parse PLC alarm logs and highlight critical events"
- "Plot temperature trends from sensor CSV files"
- "Summarize daily production reports"

### ✅ Documentation and Checklists

Generate tools that:
- Create maintenance checklists
- Format procedure documents
- Generate shift handoff reports
- Organize technical notes
- Cross-reference manuals and specs

**Examples**:
- "Checklist generator for diesel engine startup procedure"
- "Tool to format maintenance logs into standard reports"

### ✅ Calculation and Reference Tools

Generate tools that:
- Perform engineering calculations
- Convert units
- Look up specifications
- Calculate torque, pressure, flow, etc.
- Reference tables and charts

**Examples**:
- "HVAC load calculator for different room sizes"
- "Pipe sizing calculator based on flow rate"
- "Bolt torque lookup by grade and size"

### ✅ Data Processing and Transformation

Generate tools that:
- Convert file formats
- Clean and normalize data
- Aggregate and summarize
- Export to CSV, JSON, or text
- Batch process multiple files

**Examples**:
- "Convert equipment logs from XML to CSV"
- "Batch rename and organize photos from job sites"
- "Merge multiple sensor logs into one report"

---

## File System Safety

### Allowed Operations

The factory **CAN**:
- Create, read, modify, delete files in `/Users/dp/Projects/AgentOrchestratedCodeFactory`
- Create new project directories under `/Users/dp/Projects`
- Read files anywhere when explicitly given paths by the user

### Forbidden Operations

The factory **CANNOT**:
- Modify files outside `/Users/dp/Projects` (except with explicit permission)
- Delete system files or directories
- Access other users' home directories
- Modify application binaries
- Change system configurations

### Enforcement

1. **Path Validation**: All file operations validate paths before execution
2. **Logging**: Every file operation is logged with timestamp and user
3. **Git Operations**: Logged separately in `git_activity.log`

```python
# Example validation
def validate_path(path: str) -> bool:
    allowed_roots = ["/Users/dp/Projects"]
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(root) for root in allowed_roots)
```

---

## Git and GitHub Safety

### Safe Operations (Automatic)

- `git init` - Initialize new repositories
- `git add` - Stage files
- `git commit` - Commit changes
- `git branch` - Create branches
- `git push` (non-force) - Push to remote

### Requires Confirmation

Before executing these operations, the factory will ask for explicit user confirmation:

- `git push --force` - Force push
- `git branch -D` - Delete local branch
- `git push origin --delete` - Delete remote branch
- Changing default branch
- Rewriting commit history

### Logging

All Git operations are logged to `git_activity.log`:
```
2025-01-15 10:23:45 - git init - /Users/dp/Projects/NewProject
2025-01-15 10:24:12 - git commit - Initial commit (3 files)
2025-01-15 10:25:01 - git push origin main - Success
```

---

## SafetyGuard Agent Logic

The SafetyGuard agent reviews every idea before execution:

### Automatic Rejection

Ideas containing these keywords are automatically rejected:
- control, actuate, activate, trigger (in equipment context)
- override, bypass, disable (in safety context)
- hack, crack, exploit, inject
- delete system, format drive, rm -rf /

### Requires Human Review

Ideas containing these patterns require confirmation:
- network, API, external calls
- delete, remove, purge (in file context)
- email, SMS, notifications
- sudo, admin, privileged

### Auto-Approved

Ideas clearly focused on these are auto-approved:
- parse, analyze, read, monitor
- calculate, convert, lookup
- format, document, generate report
- visualize, plot, chart

### Example Safety Checks

**REJECTED**:
```
Idea: "Control valve positions based on temperature readings"
Reason: Equipment control - safety violation
```

**REQUIRES CONFIRMATION**:
```
Idea: "Send alert emails when critical alarms are detected"
Reason: External network communication - user should approve
Confirmation: "This tool will send emails. Proceed? (y/n)"
```

**APPROVED**:
```
Idea: "Parse alarm logs and identify patterns in critical events"
Reason: Read-only analysis - safe operation
```

---

## Secrets and Credentials

### Never Store in Repository

The factory will **NEVER** commit these to Git:
- API keys and tokens
- Passwords or credentials
- SSH private keys
- Database connection strings
- Email addresses (in bulk)

### Proper Secret Handling

Generated tools should:
1. Use environment variables for secrets
2. Read from `.env` files (not committed)
3. Include `.env.example` templates
4. Document how to set up credentials
5. Add `.env` to `.gitignore`

Example:
```python
# config.py - GOOD
import os
API_KEY = os.getenv("API_KEY")

# config.py - BAD
API_KEY = "sk-1234567890abcdef"  # Never do this!
```

---

## Data Privacy

### User Data Protection

Generated tools should:
- Not log sensitive user data
- Minimize data retention
- Include data anonymization options
- Respect privacy in error messages
- Avoid transmitting PII without consent

### Example Guidelines

**GOOD**:
```
Error: Failed to process file 'engine_log_001.txt'
```

**BAD**:
```
Error: Failed to process SSN 123-45-6789 for John Smith at john@email.com
```

---

## Testing Safety

The factory tests its safety mechanisms:

### Unit Tests

```python
def test_safety_guard_rejects_equipment_control():
    idea = Idea(description="Control pump speed based on pressure")
    guard = SafetyGuard()
    result = guard.execute(idea)
    assert result.approved == False
    assert "control" in result.warnings[0].lower()

def test_path_validation_blocks_system_access():
    assert not validate_path("/System/Library/")
    assert not validate_path("/usr/bin/")
    assert validate_path("/Users/dp/Projects/MyTool")
```

### Integration Tests

- Verify factory cannot write outside allowed directories
- Confirm dangerous operations are logged and rejected
- Test that confirmations are required for risky operations

---

## Emergency Stop

If you discover the factory is doing something dangerous:

1. **Kill the process**: `Ctrl+C` or `kill <PID>`
2. **Review logs**: Check `git_activity.log` and application logs
3. **Report the issue**: Document what happened
4. **Fix and test**: Update safety logic and add test case

---

## Responsibilities

### Factory Responsibilities

- Enforce safety boundaries
- Validate all inputs
- Log all operations
- Require confirmations for risky actions
- Never generate dangerous code

### User Responsibilities

- Review generated code before using in production
- Don't bypass safety mechanisms
- Report safety issues
- Use generated tools responsibly
- Understand that tools are decision support, not autonomous systems

---

## Red Lines (Never Cross)

1. **Life Safety**: No code that could harm people
2. **Property Damage**: No code that could damage equipment
3. **Legal Violations**: No code for illegal activities
4. **Security Breaches**: No code to compromise systems
5. **Data Theft**: No code to steal or exfiltrate data

If an idea approaches these boundaries, the factory **MUST** reject it, regardless of how it's phrased or justified.

---

## Future Safety Enhancements

1. **Sandboxed Execution**: Run generated code in isolated containers
2. **Code Analysis**: Static analysis to detect potential issues
3. **Human Review Queue**: Escalate ambiguous cases
4. **Safety Metrics**: Track rejection rates and patterns
5. **Community Reporting**: Allow users to flag unsafe templates

---

*Safety is not optional. It's the foundation of everything we build.*
