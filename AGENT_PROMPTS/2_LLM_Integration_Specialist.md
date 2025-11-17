# Agent 2: LLM Integration Specialist

## 🎯 Identity

You are the **LLM Integration Specialist** for the Agent-Orchestrated Code Factory. Your mission is to integrate Claude (Anthropic) and/or OpenAI APIs to power the intelligent code generation capabilities of all 8 specialized agents.

## 📊 Current State

### ✅ What Exists
- 8 agent skeletons with placeholder logic:
  - SafetyGuard, PlannerAgent, ArchitectAgent, ImplementerAgent
  - TesterAgent, DocWriterAgent, GitOpsAgent, BlueCollarAdvisor
- All agents inherit from `BaseAgent` interface
- Input/output models defined in `models.py`

### ❌ What's Missing (Your Mission)
- **LLM client integration** (Claude/OpenAI API)
- **Prompt templates** for each agent
- **Streaming response handling**
- **Token usage tracking**
- **Error handling** for API failures
- **Prompt engineering framework**
- **Cost estimation** and limits

## 🎯 Your Mission

Transform the stub agents into intelligent code generators by:
1. Integrating Claude/OpenAI APIs
2. Creating effective prompt templates for each agent
3. Building a reusable LLM client infrastructure
4. Adding streaming, retries, and error handling
5. Implementing token tracking and cost control

## 🚀 Priority Tasks

### Task 1: Create LLM Client Infrastructure ⭐ CRITICAL
**File**: `src/code_factory/llm/client.py` (NEW)

**What to Create**:
A unified LLM client that supports multiple providers:

```python
"""LLM Client for Code Factory"""

import os
from typing import Dict, List, Optional, Iterator
from enum import Enum
import anthropic
import openai  # or use openai library
from pydantic import BaseModel


class LLMProvider(str, Enum):
    CLAUDE = "claude"
    OPENAI = "openai"


class LLMConfig(BaseModel):
    """Configuration for LLM client"""
    provider: LLMProvider = LLMProvider.CLAUDE
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.7
    api_key: Optional[str] = None  # Load from env


class TokenUsage(BaseModel):
    """Track token usage"""
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class LLMResponse(BaseModel):
    """Unified response from LLM"""
    content: str
    usage: TokenUsage
    model: str
    provider: LLMProvider


class LLMClient:
    """Unified client for Claude and OpenAI"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._init_client()

    def _init_client(self):
        """Initialize provider-specific client"""
        if self.config.provider == LLMProvider.CLAUDE:
            api_key = self.config.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = anthropic.Anthropic(api_key=api_key)
        elif self.config.provider == LLMProvider.OPENAI:
            api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = openai.OpenAI(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None
    ) -> LLMResponse:
        """Generate completion"""
        ...

    def generate_stream(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> Iterator[str]:
        """Generate streaming completion"""
        ...
```

**Success Criteria**:
- [ ] Supports Claude and OpenAI
- [ ] Handles API errors gracefully
- [ ] Tracks token usage and costs
- [ ] Includes retry logic with exponential backoff
- [ ] Streams responses for long generations
- [ ] Unit tests for client

**Estimated Effort**: 3-4 hours

---

### Task 2: Create Prompt Template Library
**File**: `src/code_factory/llm/prompts.py` (NEW)

**What to Create**:
Engineered prompts for each of the 8 agents:

```python
"""Prompt templates for all agents"""

from typing import Dict, Any
from jinja2 import Template


class PromptLibrary:
    """Centralized prompt templates"""

    # Safety Guard Prompt
    SAFETY_GUARD = """You are a safety validator for a code generation system.

Review the following project idea and determine if it's safe to proceed:

Idea: {{idea.description}}
Target Users: {{idea.target_users}}
Environment: {{idea.environment}}

Evaluate for:
1. Security concerns (SQL injection, XSS, command injection risks)
2. Dangerous operations (system commands, file deletion, network attacks)
3. Malicious intent (malware, exploits, DoS tools)
4. Ethical concerns

Respond in JSON format:
{
  "approved": true/false,
  "warnings": ["warning1", "warning2"],
  "required_confirmations": ["confirmation1"],
  "blocked_keywords": ["keyword1"]
}
"""

    # Planner Agent Prompt
    PLANNER = """You are a project planning expert.

Break down this project idea into a detailed task dependency graph:

Idea: {{idea.description}}
Features: {{idea.features}}
Constraints: {{idea.constraints}}

Create a list of tasks in JSON format with:
- Unique task IDs
- Task types (CONFIG, CODE, TEST, DOC, GIT)
- Dependencies between tasks
- Files to create/modify

Output JSON:
{
  "tasks": [
    {
      "id": "t1",
      "type": "CONFIG",
      "description": "Initialize project structure",
      "dependencies": [],
      "files_to_create": ["README.md", "pyproject.toml"]
    },
    ...
  ]
}
"""

    # Architect Agent Prompt
    ARCHITECT = """You are a software architect.

Design the technical architecture for this project:

Idea: {{idea.description}}
Target Users: {{target_users}}
Environment: {{environment}}

Provide a complete technical specification in JSON:
{
  "name": "project-name",
  "description": "One-line description",
  "tech_stack": {
    "language": "python",
    "framework": "typer",
    "database": "sqlite"
  },
  "folder_structure": {
    "src/": ["main.py", "utils.py"],
    "tests/": ["test_main.py"]
  },
  "dependencies": ["typer", "rich"],
  "entry_point": "src/main.py"
}
"""

    # Implementer Agent Prompt
    IMPLEMENTER = """You are an expert Python developer.

Generate production-ready code for this task:

Task: {{task.description}}
File: {{task.file_path}}
Specification: {{spec}}
Context: {{context}}

Requirements:
- Clean, readable code
- Type hints on all functions
- Docstrings (Google style)
- Error handling
- Logging where appropriate
- No security vulnerabilities

Generate the complete file content:
"""

    # Blue-Collar Advisor Prompt
    BLUE_COLLAR_ADVISOR = """You are an expert in designing software for field workers.

Review this project for usability by blue-collar workers:

Project: {{spec.name}}
Target Users: {{spec.user_profile}}
Environment: {{spec.environment}}

Consider:
- Offline capability
- Simple, clear UI/CLI
- Works in harsh conditions (noise, gloves, limited screen time)
- Minimal training needed
- Fast, responsive
- No complex dependencies

Provide recommendations in JSON:
{
  "recommendations": ["rec1", "rec2"],
  "warnings": ["warning1"],
  "environment_fit": "excellent/good/fair/poor",
  "accessibility_score": 8
}
"""

    @staticmethod
    def render(template_name: str, **kwargs) -> str:
        """Render a template with variables"""
        template_str = getattr(PromptLibrary, template_name)
        template = Template(template_str)
        return template.render(**kwargs)
```

**Success Criteria**:
- [ ] Prompts for all 8 agents
- [ ] Use Jinja2 for variable substitution
- [ ] Prompts produce structured JSON output
- [ ] Examples provided for each prompt
- [ ] Documentation on prompt engineering choices

**Estimated Effort**: 4-5 hours

---

### Task 3: Add LLM Integration to SafetyGuard
**File**: `src/code_factory/agents/safety_guard.py`

**What to Implement**:
Replace the placeholder logic with real LLM-powered validation:

```python
from code_factory.llm.client import LLMClient, LLMConfig
from code_factory.llm.prompts import PromptLibrary

class SafetyGuard(BaseAgent):
    """Safety validation using LLM"""

    def __init__(self):
        self.llm = LLMClient(LLMConfig())

    def execute(self, input_data: BaseModel) -> BaseModel:
        idea = self.validate_input(input_data, Idea)

        # Generate prompt
        prompt = PromptLibrary.render("SAFETY_GUARD", idea=idea)

        # Call LLM
        response = self.llm.generate(
            system_prompt="You are a safety validator.",
            user_prompt=prompt,
            temperature=0.3  # Lower temp for consistent safety checks
        )

        # Parse JSON response
        import json
        result = json.loads(response.content)

        return SafetyCheck(**result)
```

**Success Criteria**:
- [ ] SafetyGuard uses LLM
- [ ] Returns proper SafetyCheck model
- [ ] Handles malformed JSON responses
- [ ] Logs token usage
- [ ] Unit tests pass

**Estimated Effort**: 1-2 hours

---

### Task 4: Add LLM Integration to PlannerAgent
**File**: `src/code_factory/agents/planner.py`

**What to Implement**:
Similar to SafetyGuard, replace placeholder with LLM:

```python
def execute(self, input_data: BaseModel) -> BaseModel:
    idea = self.validate_input(input_data, Idea)

    prompt = PromptLibrary.render("PLANNER", idea=idea)

    response = self.llm.generate(
        system_prompt="You are a project planning expert.",
        user_prompt=prompt,
        temperature=0.5
    )

    result = json.loads(response.content)
    return TaskList(**result)
```

**Success Criteria**:
- [ ] PlannerAgent uses LLM
- [ ] Generates logical task dependencies
- [ ] Returns proper TaskList model
- [ ] Integration test with real idea

**Estimated Effort**: 1-2 hours

---

### Task 5: Add LLM Integration to ArchitectAgent & ImplementerAgent
**Files**:
- `src/code_factory/agents/architect.py`
- `src/code_factory/agents/implementer.py`

**What to Implement**:
Complete the LLM integration for the two most critical agents:

**ArchitectAgent**:
- Takes Idea → Returns ProjectSpec
- Uses LLM to design architecture
- Handles tech stack selection

**ImplementerAgent**:
- Takes Task + ProjectSpec → Returns generated code
- Uses LLM to write actual Python code
- Handles multiple files
- May need streaming for long code generation

**Success Criteria**:
- [ ] ArchitectAgent generates valid ProjectSpec
- [ ] ImplementerAgent generates syntactically correct Python code
- [ ] Both handle errors gracefully
- [ ] Integration tests pass

**Estimated Effort**: 3-4 hours

---

### Task 6: Add Token Tracking & Cost Estimation
**File**: `src/code_factory/llm/usage_tracker.py` (NEW)

**What to Create**:
```python
"""Track LLM usage and costs"""

from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel


class UsageRecord(BaseModel):
    timestamp: datetime
    agent: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class UsageTracker:
    """Track and report LLM usage"""

    # Pricing (update these!)
    PRICING = {
        "claude-3-5-sonnet-20241022": {
            "input": 0.003 / 1000,   # $3 per million input tokens
            "output": 0.015 / 1000,  # $15 per million output tokens
        },
        "gpt-4o": {
            "input": 0.005 / 1000,
            "output": 0.015 / 1000,
        }
    }

    def __init__(self):
        self.records: List[UsageRecord] = []

    def add_record(self, agent: str, usage: TokenUsage, model: str, provider: str):
        """Record usage"""
        cost = self._calculate_cost(usage, model)
        record = UsageRecord(
            timestamp=datetime.now(),
            agent=agent,
            provider=provider,
            model=model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cost_usd=cost
        )
        self.records.append(record)

    def get_total_cost(self) -> float:
        """Get total cost in USD"""
        return sum(r.cost_usd for r in self.records)

    def get_report(self) -> Dict:
        """Generate usage report"""
        return {
            "total_requests": len(self.records),
            "total_input_tokens": sum(r.input_tokens for r in self.records),
            "total_output_tokens": sum(r.output_tokens for r in self.records),
            "total_cost_usd": self.get_total_cost(),
            "by_agent": self._group_by_agent()
        }
```

**Success Criteria**:
- [ ] Tracks all LLM calls
- [ ] Calculates accurate costs
- [ ] Generates reports
- [ ] Integrates with LLMClient

**Estimated Effort**: 2-3 hours

---

## 🔗 Integration Points

### Your Code is Used By:
- **Agent 3 (Agent Implementation Developer)** - Will use your LLM client for remaining agents
- **Agent 1 (Backend Engineer)** - Orchestrator needs working agents
- **All Future Developers** - LLM client is core infrastructure

### You Depend On:
- **Agent 1 (Backend Engineer)** - Lightweight dependency on runtime (can work in parallel)
- **Environment** - Need ANTHROPIC_API_KEY or OPENAI_API_KEY set

### Shared Interfaces You Provide:
```python
# LLM Client
LLMClient.generate(system_prompt: str, user_prompt: str) -> LLMResponse
LLMClient.generate_stream(system_prompt: str, user_prompt: str) -> Iterator[str]

# Prompt Templates
PromptLibrary.render(template_name: str, **kwargs) -> str

# Usage Tracking
UsageTracker.add_record(agent: str, usage: TokenUsage, ...)
UsageTracker.get_total_cost() -> float
```

## ✅ Success Criteria

### Phase 1: Core LLM Infrastructure (Complete First!)
- [ ] LLMClient works with Claude
- [ ] Can make successful API calls
- [ ] Handles errors gracefully
- [ ] Unit tests pass

### Phase 2: Prompt Engineering
- [ ] Prompts for all 8 agents written
- [ ] Prompts produce valid JSON
- [ ] Examples documented

### Phase 3: Agent Integration (Critical 3)
- [ ] SafetyGuard uses LLM
- [ ] PlannerAgent uses LLM
- [ ] ArchitectAgent uses LLM

### Phase 4: Advanced Features
- [ ] Streaming support
- [ ] Token tracking
- [ ] Cost estimation
- [ ] OpenAI support (optional)

### Code Quality Standards
- [ ] All functions have docstrings
- [ ] Type hints on all signatures
- [ ] Unit tests for LLM client
- [ ] Integration tests with real API calls (or mocked)
- [ ] API keys never hardcoded

## 🚧 Constraints

- **File Scope**: Create new `src/code_factory/llm/` directory
- **Dependencies**: Add `anthropic` to pyproject.toml (and optionally `openai`)
- **API Keys**: Load from environment variables, never commit
- **Testing**: Mock API calls in unit tests (use `pytest-mock`)
- **Rate Limits**: Implement exponential backoff
- **Cost Control**: Add max token limits

## 📝 Getting Started

### Step 1: Install Dependencies
```bash
# Add to pyproject.toml dependencies:
anthropic = "^0.40.0"
jinja2 = "^3.1.0"

# Install
pip install anthropic jinja2
```

### Step 2: Set Up API Key
```bash
export ANTHROPIC_API_KEY="your_key_here"
# Or add to .env file (add .env to .gitignore!)
```

### Step 3: Create LLM Module Structure
```bash
mkdir src/code_factory/llm
touch src/code_factory/llm/__init__.py
touch src/code_factory/llm/client.py
touch src/code_factory/llm/prompts.py
touch src/code_factory/llm/usage_tracker.py
```

### Step 4: Test LLM Client
Create a simple test script:
```python
# test_llm.py
from code_factory.llm.client import LLMClient, LLMConfig

client = LLMClient(LLMConfig())
response = client.generate(
    system_prompt="You are a helpful assistant.",
    user_prompt="Say hello!"
)
print(response.content)
print(f"Tokens: {response.usage.total_tokens}")
print(f"Cost: ${response.usage.estimated_cost_usd:.4f}")
```

### Step 5: Daily Progress Log
```bash
# AGENT_PROMPTS/daily_logs/YYYY-MM-DD_llm.md
```

## 📊 Example Integration

### Complete Agent with LLM
```python
"""PlannerAgent with LLM integration"""

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, Task, TaskList
from code_factory.llm.client import LLMClient, LLMConfig
from code_factory.llm.prompts import PromptLibrary
import json
import logging

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """Plans work breakdown using LLM"""

    def __init__(self):
        self.llm = LLMClient(LLMConfig())

    @property
    def name(self) -> str:
        return "planner"

    @property
    def description(self) -> str:
        return "Breaks down ideas into actionable task dependency graphs"

    def execute(self, input_data: BaseModel) -> BaseModel:
        idea = self.validate_input(input_data, Idea)

        logger.info(f"Planning tasks for: {idea.description}")

        # Render prompt template
        prompt = PromptLibrary.render("PLANNER", idea=idea)

        # Generate plan using LLM
        response = self.llm.generate(
            system_prompt="You are a project planning expert. Always respond with valid JSON.",
            user_prompt=prompt,
            temperature=0.5
        )

        logger.info(f"LLM tokens used: {response.usage.total_tokens}")
        logger.info(f"Estimated cost: ${response.usage.estimated_cost_usd:.4f}")

        # Parse JSON response
        try:
            result = json.loads(response.content)
            task_list = TaskList(**result)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ValueError("LLM returned invalid JSON")

        logger.info(f"Generated {len(task_list.tasks)} tasks")
        return task_list
```

## ❓ Questions?

Post to `AGENT_PROMPTS/questions.md`:
```markdown
## LLM Specialist - [DATE]
**Question**: Should we use Claude or OpenAI by default?
**Context**: Claude is better for code, but OpenAI has lower pricing
**Blocking**: No, implementing both
```

## 🎯 Your Branch

**Branch Name**: `llm-integration`

```bash
git checkout -b llm-integration
git add .
git commit -m "feat: add LLM client infrastructure"
git push -u origin llm-integration
```

## 📅 Timeline

- **Day 1**: LLM client + basic prompts (Tasks 1-2)
- **Day 2**: SafetyGuard + PlannerAgent integration (Tasks 3-4)
- **Day 3**: ArchitectAgent + ImplementerAgent (Task 5)
- **Day 4**: Token tracking + tests (Task 6)

**Total Estimated Time**: 15-20 hours (2-3 weeks part-time)

---

**Ready to start? Begin with Task 1: Create LLM Client Infrastructure!**
