"""
PlannerAgent - Transforms ideas into task dependency graphs

Breaks down a high-level project idea into concrete, actionable tasks
with dependencies and execution order.
"""

import logging
from typing import List

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, Task, TaskType
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TaskList(BaseModel):
    """Output model for PlannerAgent"""
    tasks: List[Task]


class PlannerAgent(BaseAgent):
    """
    Plans the work breakdown for a project
    
    Takes an Idea and produces a list of Tasks with dependencies,
    creating a logical execution order for the build pipeline.
    """
    
    @property
    def name(self) -> str:
        return "planner"
    
    @property
    def description(self) -> str:
        return "Breaks down ideas into actionable task dependency graphs"
    
    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Generate task list from an idea
        
        Args:
            input_data: Idea object
            
        Returns:
            TaskList: List of tasks to execute
        """
        idea = self.validate_input(input_data, Idea)
        
        logger.info(f"Planning tasks for: {idea.description}")
        
        # TODO: Implement intelligent task planning
        # For now, return a basic task structure
        tasks = [
            Task(
                id="t1",
                type=TaskType.CONFIG,
                description="Initialize project structure",
                dependencies=[],
                files_to_create=["README.md", "pyproject.toml"]
            ),
            Task(
                id="t2",
                type=TaskType.CODE,
                description="Implement core functionality",
                dependencies=["t1"],
                files_to_create=["src/main.py"]
            ),
            Task(
                id="t3",
                type=TaskType.TEST,
                description="Create unit tests",
                dependencies=["t2"],
                files_to_create=["tests/test_main.py"]
            ),
            Task(
                id="t4",
                type=TaskType.DOC,
                description="Write documentation",
                dependencies=["t2"],
                files_to_create=["docs/usage.md"]
            )
        ]
        
        logger.info(f"Generated {len(tasks)} tasks")
        return TaskList(tasks=tasks)
