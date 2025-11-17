"""
ArchitectAgent - Designs project architecture and technology choices

Analyzes the idea and tasks to determine the optimal tech stack,
folder structure, and architectural patterns.
"""

import logging
from typing import Dict, List

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, ProjectSpec
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ArchitectInput(BaseModel):
    """Input combining idea and optional task information"""
    idea: Idea
    task_count: int = 0


class ArchitectAgent(BaseAgent):
    """
    Designs the technical architecture for a project
    
    Chooses technology stack, defines folder structure,
    and makes all architectural decisions.
    """
    
    @property
    def name(self) -> str:
        return "architect"
    
    @property
    def description(self) -> str:
        return "Designs project architecture and selects appropriate technologies"
    
    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Design architecture from idea
        
        Args:
            input_data: Idea or ArchitectInput
            
        Returns:
            ProjectSpec: Complete architectural specification
        """
        if isinstance(input_data, Idea):
            idea = input_data
        else:
            arch_input = self.validate_input(input_data, ArchitectInput)
            idea = arch_input.idea
        
        logger.info(f"Designing architecture for: {idea.description}")
        
        # TODO: Implement intelligent architecture design
        # For now, return a sensible default Python CLI structure
        project_name = self._generate_project_name(idea.description)
        
        spec = ProjectSpec(
            name=project_name,
            description=idea.description[:100],
            tech_stack={
                "language": "python",
                "cli_framework": "typer",
                "testing": "pytest"
            },
            folder_structure={
                "src/": ["main.py", "core.py"],
                "tests/": ["test_main.py"],
                "docs/": ["README.md"]
            },
            dependencies=["typer", "rich"],
            entry_point="src/main.py",
            user_profile=idea.target_users[0] if idea.target_users else "general",
            environment=idea.environment
        )
        
        logger.info(f"Generated spec for project: {project_name}")
        return spec
    
    def _generate_project_name(self, description: str) -> str:
        """Generate a project name from description"""
        # Simple implementation: take first few words, lowercase, hyphenate
        words = description.lower().split()[:3]
        return "-".join(word.strip(".,!?") for word in words if word.isalnum())
