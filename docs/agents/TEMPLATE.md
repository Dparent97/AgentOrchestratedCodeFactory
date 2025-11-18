# [AgentName] - [Purpose]

## Overview

[Brief description of what this agent does and why it exists in the factory pipeline]

**Position in Pipeline**: [Where this agent fits in the overall workflow]

**Key Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

---

## API Reference

### Input Model

```python
class InputModel(BaseModel):
    field_name: Type = Field(..., description="Field description")
    optional_field: Optional[Type] = Field(None, description="Optional field description")
```

**Field Descriptions**:
- `field_name`: [Detailed explanation of what this field represents and how it's used]
- `optional_field`: [Explanation of optional field]

### Output Model

```python
class OutputModel(BaseModel):
    result_field: Type = Field(..., description="Result description")
    status: str = Field(default="success", description="Execution status")
```

**Field Descriptions**:
- `result_field`: [What this field contains and how to use it]
- `status`: [Status information]

### Execute Method

```python
def execute(self, input_data: InputModel) -> OutputModel:
    """
    [Brief description of what execute does]

    Args:
        input_data: [Description of input]

    Returns:
        OutputModel: [Description of output]

    Raises:
        ValueError: [When this might be raised]
        AgentExecutionError: [When this might be raised]
    """
    pass
```

---

## Usage Examples

### Basic Example

```python
from code_factory.agents.[agent_module] import [AgentName]
from code_factory.core.models import InputModel

# Create agent instance
agent = [AgentName]()

# Prepare input
input_data = InputModel(
    field_name="example_value",
    optional_field="optional_value"
)

# Execute agent
result = agent.execute(input_data)

# Use result
print(f"Status: {result.status}")
print(f"Result: {result.result_field}")
```

**Expected Output**:
```
Status: success
Result: [expected result]
```

### Real-World Example: Marine Log Analyzer

```python
# [Practical example relevant to blue-collar use case]
# Show a complete workflow using this agent

from code_factory.agents.[agent_module] import [AgentName]
from code_factory.core.models import InputModel

# Real-world scenario
input_data = InputModel(
    field_name="Parse marine engine alarm logs and highlight critical issues",
    optional_field="marine_engineer"
)

result = agent.execute(input_data)

# Result processing
for item in result.result_field:
    print(f"- {item}")
```

### Integration Example

```python
# Show how this agent integrates with other agents in the pipeline

from code_factory.agents.planner import PlannerAgent
from code_factory.agents.[agent_module] import [AgentName]
from code_factory.core.models import Idea

# Step 1: Previous agent in pipeline
previous_agent = PreviousAgent()
previous_result = previous_agent.execute(...)

# Step 2: This agent
agent = [AgentName]()
result = agent.execute(previous_result)

# Step 3: Next agent in pipeline
next_agent = NextAgent()
final_result = next_agent.execute(result)
```

---

## Implementation Notes

### Algorithm Overview

[Describe the core algorithm or logic this agent uses]

1. **Step 1**: [What happens first]
2. **Step 2**: [What happens next]
3. **Step 3**: [Final step]

### Design Decisions

**Why [specific design choice]?**
- [Reason 1]
- [Reason 2]

**Trade-offs**:
- **Pro**: [Advantage of current approach]
- **Con**: [Limitation of current approach]
- **Alternative**: [What we considered and why we didn't choose it]

### Future Enhancements

- [ ] [Planned improvement 1]
- [ ] [Planned improvement 2]
- [ ] [Planned improvement 3]

---

## Blue-Collar Considerations

### Design Choices for Field Use

- **[Consideration 1]**: [How this agent is designed to work well in real-world conditions]
- **[Consideration 2]**: [Another practical design choice]
- **[Consideration 3]**: [User experience consideration]

### Target Environment Awareness

This agent is designed to help build tools for:
- [Environment characteristic 1]
- [Environment characteristic 2]
- [Environment characteristic 3]

### Example Scenarios

**Scenario 1: [Real-world situation]**
- **Challenge**: [What problem the user faces]
- **How this agent helps**: [What this agent does to address it]
- **Result**: [Practical outcome]

**Scenario 2: [Another situation]**
- **Challenge**: [Problem]
- **How this agent helps**: [Solution]
- **Result**: [Outcome]

---

## Testing

### Test Location

Tests for this agent are located in: `tests/unit/agents/test_[agent_name].py`

### Running Tests

```bash
# Run all agent tests
pytest tests/unit/agents/test_[agent_name].py -v

# Run specific test
pytest tests/unit/agents/test_[agent_name].py::test_[specific_test] -v

# Run with coverage
pytest tests/unit/agents/test_[agent_name].py --cov=code_factory.agents.[agent_module]
```

### Test Coverage

Current test coverage: [X%]

**Test Categories**:
- ✅ Input validation tests
- ✅ Happy path tests
- ✅ Error handling tests
- ✅ Edge case tests
- ✅ Integration tests

### Example Test

```python
def test_[agent_name]_basic_usage():
    """Test basic agent execution"""
    agent = [AgentName]()

    input_data = InputModel(
        field_name="test_value"
    )

    result = agent.execute(input_data)

    assert result.status == "success"
    assert result.result_field is not None
```

---

## Error Handling

### Common Errors

**Error**: `ValueError: [error message]`
- **Cause**: [What causes this error]
- **Solution**: [How to fix it]

**Error**: `AgentExecutionError: [error message]`
- **Cause**: [What causes this error]
- **Solution**: [How to fix it]

### Error Recovery

[Describe how this agent handles partial failures and recovery]

```python
# Example error handling
try:
    result = agent.execute(input_data)
except ValueError as e:
    print(f"Invalid input: {e}")
    # Recovery action
except AgentExecutionError as e:
    print(f"Execution failed: {e}")
    # Recovery action
```

---

## Performance Considerations

**Typical Execution Time**: [Time range]

**Resource Usage**:
- **Memory**: [Typical memory usage]
- **CPU**: [CPU usage characteristics]
- **I/O**: [I/O requirements]

**Optimization Tips**:
- [Tip 1 for better performance]
- [Tip 2 for better performance]

---

## Related Documentation

- [Main Architecture Overview](../architecture.md)
- [Agent Roles](../agent_roles.md)
- [Safety Guidelines](../safety.md)
- [Other Related Agent](./other_agent.md)

---

## Changelog

### Version 1.0.0 (2025-01-XX)
- Initial implementation
- [Feature 1]
- [Feature 2]

### Version 1.1.0 (Planned)
- [Planned enhancement 1]
- [Planned enhancement 2]
