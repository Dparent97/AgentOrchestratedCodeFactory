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

The SafetyGuard agent implements **defense-in-depth security** with multiple validation layers to prevent bypass attempts. Every idea is reviewed through 5 security layers before execution:

### Layer 1: Input Normalization

**Purpose**: Prevent bypass via obfuscation techniques

The SafetyGuard normalizes all input text to prevent common bypass attempts:

- **Unicode normalization** (NFKD) - removes accents and diacritics
- **Lowercase conversion** - eliminates case-based bypasses
- **Separator normalization** - converts `_`, `-`, `.`, `/`, `\` to spaces
- **Whitespace collapsing** - removes multiple/zero-width spaces
- **Zero-width character removal** - prevents invisible character bypasses

**Examples of prevented bypasses**:
```
❌ "control_equipment" → normalized to "control equipment" → BLOCKED
❌ "control-equipment" → normalized to "control equipment" → BLOCKED
❌ "Control Equipment" → normalized to "control equipment" → BLOCKED
❌ "control  equipment" → normalized to "control equipment" → BLOCKED
❌ "controlequipment" → kept as "controlequipment" → Still caught by patterns
```

### Layer 2: Regex Pattern Matching

**Purpose**: Robustly detect dangerous operations

Uses regex-based patterns instead of simple substring matching:

**Automatic Rejection** (Critical Severity):
- Physical control: `control\s*equipment`, `actuate`, `bypass\s*interlock`
- Safety systems: `override\s*safety`, `disable\s*alarm`
- Security violations: `hack`, `exploit`, `crack\s*password`, `inject`, `malware`
- Destructive operations: `rm\s*-?r?f\s*/`, `format\s*drive`, `drop\s*database`
- Obfuscation attempts: `eval\(`, `exec\(`, `base64.*decode`

**Requires Human Review** (Medium/High Severity):
- File operations: `delete\s*file`
- Network operations: `send\s*email`, `api\s*request`
- Elevated privileges: `sudo`, `admin\s*privilege`
- System calls: `subprocess`, `system\s*call`

### Layer 3: Semantic Analysis

**Purpose**: Context-aware detection of dangerous intent

Analyzes combinations of action verbs and destructive indicators:

- **Destructive verbs**: destroy, wipe, erase, corrupt, damage, break, crash, kill
- **Risky combinations**: "system control", "obfuscate + execute", "encode + eval"
- **Missing safe operations**: Flags inputs with no clearly approved actions

**Example detections**:
```
"Override safety and destroy old equipment"
↓
✗ Pattern: "override safety" → BLOCKED
✗ Semantic: Destructive verbs (destroy) → BLOCKED
```

### Layer 4: Whitelist Validation

**Purpose**: Explicitly approve known-safe operations

**Approved safe operations**:
- Read/Display: read, display, show, list, view, get, fetch
- Calculate: calculate, compute, analyze, parse, validate
- Transform: format, convert, transform, encode, decode
- Monitor: log, track, monitor, measure, report
- Search: search, find, filter, sort, query
- Create: create, generate, build, make, initialize
- Test: test, verify, check, inspect, scan
- Update: update, modify, edit, change, adjust (when properly scoped)
- Help: help, guide, assist, support, document

Ideas containing primarily non-approved operations receive warnings and reduced confidence scores.

### Layer 5: Audit Trail

**Purpose**: Full transparency and accountability

Every safety check generates detailed metadata:

- **Timestamp**: When the check was performed
- **Normalized text**: The sanitized input used for checking
- **Patterns matched**: Which specific patterns triggered (for audit)
- **Semantic flags**: What semantic issues were detected
- **Whitelist violations**: Unapproved operations found
- **Confidence score**: 0.0-1.0 indicating certainty in the decision

All decisions are logged with severity levels:
- `INFO`: Approved operations with confirmations
- `WARNING`: Pattern matches and semantic flags
- `ERROR`: Blocked operations and security violations

**Auto-Approved**

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

## Security Improvements (v2.0)

### Bypass Prevention

The SafetyGuard has been hardened against sophisticated bypass attempts:

**Previously vulnerable to**:
- `control_equipment` (underscore bypass)
- `Control Equipment` (case variation)
- `control  equipment` (multiple spaces)
- `controlequipment` (concatenation)
- Unicode obfuscation with accents/diacritics

**Now protected by**:
- Multi-layer normalization (see Layer 1 above)
- Regex-based pattern matching with `\s*` for flexible spacing
- Semantic analysis for context-aware detection
- Comprehensive audit logging for all decisions

### Defense-in-Depth Architecture

Each layer provides independent protection:

1. **Normalization** prevents obfuscation
2. **Pattern matching** catches known dangerous operations
3. **Semantic analysis** detects novel/combined threats
4. **Whitelist validation** ensures operations are approved
5. **Audit trail** provides accountability and forensics

Even if one layer is bypassed, others provide backup protection.

### Testing Coverage

Comprehensive test suite (`tests/unit/test_safety_guard.py`) validates:

- ✅ All known bypass techniques are blocked
- ✅ Normalization handles edge cases (Unicode, zero-width chars, etc.)
- ✅ Pattern matching is resistant to obfuscation
- ✅ Semantic analysis detects destructive intent
- ✅ Safe operations are correctly approved
- ✅ Audit trail captures all decisions
- ✅ Multi-layer defense works together

**Test categories**:
- Normalization tests (8 scenarios)
- Bypass prevention tests (6 techniques)
- Dangerous pattern tests (15+ patterns)
- Semantic analysis tests (4 scenarios)
- Whitelist validation tests (3 scenarios)
- Audit trail tests (5 scenarios)
- Edge case tests (7 scenarios)

### Audit and Forensics

Every safety decision is logged with:

```
AUDIT: timestamp=2025-01-15T10:23:45.123456, approved=False,
       violations=2, confirmations=0
```

Metadata includes:
- Original input text
- Normalized text used for checking
- All patterns that matched
- Semantic flags detected
- Confidence score in the decision

This enables:
- Post-incident investigation
- Pattern analysis for new threats
- Compliance auditing
- Security metrics and reporting

## Future Safety Enhancements

1. **Sandboxed Execution**: Run generated code in isolated containers
2. **Code Analysis**: Static analysis to detect potential issues
3. **Human Review Queue**: Escalate ambiguous cases
4. **Safety Metrics**: Track rejection rates and patterns
5. **Community Reporting**: Allow users to flag unsafe templates
6. **Machine Learning**: Train models on attack patterns for better detection
7. **Rate Limiting**: Prevent automated bypass attempts
8. **Honeypot Patterns**: Detect sophisticated attackers

---

*Safety is not optional. It's the foundation of everything we build.*
