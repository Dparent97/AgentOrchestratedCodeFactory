"""
ArchitectAgent - Designs project architecture and technology choices

Analyzes the idea and tasks to determine the optimal tech stack,
folder structure, and architectural patterns.
"""

import logging
import re
from typing import Dict, List

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import ArchitectResult, Idea, ProjectSpec, Task
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ArchitectInput(BaseModel):
    """Input combining idea and task information"""
    idea: Idea
    tasks: List[Task] = []


class ArchitectAgent(BaseAgent):
    """
    Designs the technical architecture for a project

    Chooses technology stack, defines folder structure,
    and makes all architectural decisions with a focus on
    blue-collar practicality.

    Algorithm:
    1. Analyze idea domain (data processing, calculator, etc.)
    2. Select tech stack based on features
    3. Design folder structure (simple vs complex)
    4. Identify dependencies
    5. Calculate blue-collar score (CLI=high, web=low)
    """

    @property
    def name(self) -> str:
        return "architect"

    @property
    def description(self) -> str:
        return "Designs project architecture and selects appropriate technologies"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Design architecture from idea and tasks

        Args:
            input_data: Idea or ArchitectInput containing idea and tasks

        Returns:
            ArchitectResult: Complete architectural specification with rationale
        """
        # Handle both Idea and ArchitectInput
        if isinstance(input_data, Idea):
            idea = input_data
            tasks = []
        else:
            arch_input = self.validate_input(input_data, ArchitectInput)
            idea = arch_input.idea
            tasks = arch_input.tasks

        logger.info(f"Designing architecture for: {idea.description}")

        # Step 1: Analyze idea domain
        domain = self._analyze_domain(idea)
        logger.info(f"Identified domain: {domain}")

        # Step 2: Select tech stack
        tech_stack = self._select_tech_stack(idea, domain)

        # Step 3: Design folder structure
        folder_structure = self._design_folder_structure(idea, tasks, domain)

        # Step 4: Identify dependencies
        dependencies = self._identify_dependencies(idea, tech_stack)

        # Step 5: Generate project name
        project_name = self._generate_project_name(idea.description)

        # Build ProjectSpec
        spec = ProjectSpec(
            name=project_name,
            description=idea.description[:100],
            tech_stack=tech_stack,
            folder_structure=folder_structure,
            dependencies=dependencies,
            entry_point="src/main.py",
            user_profile=idea.target_users[0] if idea.target_users else "general",
            environment=idea.environment
        )

        # Step 6: Build rationale
        rationale = self._build_rationale(idea, domain, tech_stack)

        # Step 7: Calculate blue-collar score
        blue_collar_score = self._calculate_blue_collar_score(idea, spec)

        # Generate warnings
        warnings = self._generate_warnings(idea, spec, blue_collar_score)

        logger.info(
            f"Generated spec for project: {project_name} "
            f"(blue-collar score: {blue_collar_score:.1f}/10)"
        )

        return ArchitectResult(
            spec=spec,
            rationale=rationale,
            blue_collar_score=blue_collar_score,
            warnings=warnings
        )

    def _analyze_domain(self, idea: Idea) -> str:
        """
        Analyze the idea to determine project domain

        Args:
            idea: Project idea

        Returns:
            str: Domain type (e.g., "data_processing", "calculator", "tool")
        """
        description = idea.description.lower()
        features = [f.lower() for f in idea.features]
        combined_text = f"{description} {' '.join(features)}"

        # Pattern matching for common domains
        if any(kw in combined_text for kw in ["csv", "excel", "data", "parse", "analyze"]):
            return "data_processing"
        elif any(kw in combined_text for kw in ["log", "monitor", "track", "record"]):
            return "logging_tracking"
        elif any(kw in combined_text for kw in ["calculate", "math", "formula", "compute"]):
            return "calculator"
        elif any(kw in combined_text for kw in ["convert", "transform", "translate"]):
            return "converter"
        elif any(kw in combined_text for kw in ["web", "api", "http", "server"]):
            return "web_service"
        else:
            return "general_utility"

    def _select_tech_stack(self, idea: Idea, domain: str) -> Dict[str, str]:
        """
        Select technology stack based on idea and domain

        Args:
            idea: Project idea
            domain: Identified domain

        Returns:
            Dict: Technology choices
        """
        tech_stack = {
            "language": "python",
            "cli_framework": "typer",
            "ui_library": "rich",
            "testing": "pytest"
        }

        # Add domain-specific technologies
        if domain == "data_processing":
            tech_stack["data_library"] = "pandas"
        elif domain == "logging_tracking":
            tech_stack["data_library"] = "sqlite3"
        elif domain == "web_service":
            tech_stack["web_framework"] = "fastapi"

        return tech_stack

    def _design_folder_structure(
        self, idea: Idea, tasks: List[Task], domain: str
    ) -> Dict[str, List[str]]:
        """
        Design folder structure based on complexity

        Args:
            idea: Project idea
            tasks: Planned tasks
            domain: Project domain

        Returns:
            Dict: Folder structure mapping
        """
        # Start with basic structure
        structure = {
            "": ["README.md", "pyproject.toml", ".gitignore"],
            "src/": ["main.py", "cli.py"],
            "tests/": ["test_main.py"],
        }

        # Add domain-specific modules
        if domain == "data_processing":
            structure["src/"].extend(["parser.py", "processor.py"])
            structure["tests/"].extend(["test_parser.py", "test_processor.py"])
        elif domain == "logging_tracking":
            structure["src/"].extend(["database.py", "logger.py"])
            structure["tests/"].extend(["test_database.py"])
        elif domain == "web_service":
            structure["src/"].extend(["api.py", "models.py"])
            structure["tests/"].extend(["test_api.py"])
        else:
            structure["src/"].append("core.py")
            structure["tests/"].append("test_core.py")

        # Add examples for complex projects
        if len(idea.features) >= 3:
            structure["examples/"] = ["demo.py"]
            structure["docs/"] = ["usage.md"]

        return structure

    def _identify_dependencies(
        self, idea: Idea, tech_stack: Dict[str, str]
    ) -> List[str]:
        """
        Identify package dependencies based on tech stack

        Args:
            idea: Project idea
            tech_stack: Selected technologies

        Returns:
            List: Package names
        """
        deps = []

        # Core dependencies
        if tech_stack.get("cli_framework") == "typer":
            deps.append("typer")
        if tech_stack.get("ui_library") == "rich":
            deps.append("rich")

        # Domain-specific dependencies
        if tech_stack.get("data_library") == "pandas":
            deps.append("pandas")
        if tech_stack.get("web_framework") == "fastapi":
            deps.extend(["fastapi", "uvicorn"])

        return deps

    def _build_rationale(
        self, idea: Idea, domain: str, tech_stack: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Build rationale for architectural decisions

        Args:
            idea: Project idea
            domain: Identified domain
            tech_stack: Selected technologies

        Returns:
            Dict: Decision rationale mapping
        """
        rationale = {
            "language": "Python chosen for simplicity and wide availability",
            "domain": f"Identified as {domain} based on requirements",
            "cli_approach": "CLI interface for field usability (offline, simple)",
        }

        if "data_library" in tech_stack:
            rationale["data_processing"] = (
                f"{tech_stack['data_library']} for efficient data handling"
            )

        if idea.environment:
            rationale["environment"] = (
                f"Designed for {idea.environment} - optimized for robustness"
            )

        return rationale

    def _calculate_blue_collar_score(self, idea: Idea, spec: ProjectSpec) -> float:
        """
        Calculate blue-collar practicality score (0-10)

        Scoring criteria:
        - Start at 10.0 (perfect field tool)
        - Deduct for complexity factors:
          * Database: -2 (harder to deploy)
          * Web UI: -2 (requires browser)
          * Internet required: -3 (not offline-friendly)
          * Complex dependencies: -1
          * Non-CLI interface: -2

        Args:
            idea: Project idea
            spec: Project specification

        Returns:
            float: Score from 0-10 (higher is better for field workers)
        """
        score = 10.0

        # Deduct for database usage
        if any("sqlite" in dep or "database" in dep for dep in spec.dependencies):
            score -= 2.0

        # Deduct for web framework (requires browser)
        if any("fastapi" in dep or "flask" in dep or "django" in dep
               for dep in spec.dependencies):
            score -= 2.0

        # Deduct if internet is required
        combined = f"{idea.description} {' '.join(idea.features)}".lower()
        if any(kw in combined for kw in ["api", "cloud", "sync", "online"]):
            score -= 3.0

        # Deduct for complex dependencies (more than 3 packages)
        if len(spec.dependencies) > 3:
            score -= 1.0

        # Bonus for offline capability
        if any(kw in combined for kw in ["offline", "local", "standalone"]):
            score = min(10.0, score + 1.0)

        return max(0.0, min(10.0, score))

    def _generate_warnings(
        self, idea: Idea, spec: ProjectSpec, score: float
    ) -> List[str]:
        """
        Generate architectural warnings and recommendations

        Args:
            idea: Project idea
            spec: Project specification
            score: Blue-collar score

        Returns:
            List: Warning messages
        """
        warnings = []

        if score < 5.0:
            warnings.append(
                "Low blue-collar score - consider simplifying for field use"
            )

        if len(spec.dependencies) > 5:
            warnings.append(
                f"High dependency count ({len(spec.dependencies)}) may complicate deployment"
            )

        if idea.environment and "noisy" in idea.environment.lower():
            warnings.append(
                "Consider adding visual feedback for noisy environments"
            )

        if not idea.features:
            warnings.append(
                "No specific features defined - architecture may need refinement"
            )

        return warnings

    def _generate_project_name(self, description: str) -> str:
        """
        Generate a valid project name from description

        Args:
            description: Project description

        Returns:
            str: Valid project name (lowercase, hyphenated)
        """
        # Extract meaningful words
        words = description.lower().split()

        # Filter out common words and clean
        stop_words = {"a", "an", "the", "for", "to", "with", "and", "or", "build"}
        meaningful_words = []

        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s-]', '', word)
            if clean_word and clean_word not in stop_words and len(clean_word) > 2:
                meaningful_words.append(clean_word)

        # Take first 3 meaningful words
        if meaningful_words:
            name_parts = meaningful_words[:3]
        else:
            # Fallback to first few words
            name_parts = words[:3]

        # Join with hyphens and ensure valid format
        name = "-".join(name_parts)

        # Ensure it's valid (alphanumeric, hyphens, underscores only)
        name = re.sub(r'[^a-z0-9\-_]', '', name)

        # Fallback if name is empty
        return name if name else "project"
