"""
PlannerAgent - Transforms ideas into task dependency graphs

Breaks down a high-level project idea into concrete, actionable tasks
with dependencies and execution order.
"""

import logging
from typing import Dict, List, Set

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, PlanResult, Task, TaskType
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Plans the work breakdown for a project

    Takes an Idea and produces a list of Tasks with dependencies,
    creating a logical execution order for the build pipeline.

    Algorithm:
    1. Analyze idea.description and idea.features
    2. Create config tasks (setup, dependencies)
    3. Create code tasks (one per feature)
    4. Add test tasks (one per code task)
    5. Add doc tasks (README, examples)
    6. Build dependency graph
    7. Estimate complexity
    """

    @property
    def name(self) -> str:
        return "planner"

    @property
    def description(self) -> str:
        return "Breaks down ideas into actionable task dependency graphs"

    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Generate task plan from an idea

        Args:
            input_data: Idea object

        Returns:
            PlanResult: Complete plan with tasks, dependencies, and complexity
        """
        idea = self.validate_input(input_data, Idea)

        logger.info(f"Planning tasks for: {idea.description}")

        tasks: List[Task] = []
        task_counter = 0
        warnings: List[str] = []

        # Step 1: Analyze idea
        if not idea.features:
            warnings.append("No features specified - generating minimal task set")

        if not idea.description or len(idea.description.strip()) < 10:
            warnings.append("Description is very brief - plan may be incomplete")

        # Step 2: Create config tasks
        task_counter += 1
        config_task = Task(
            id=f"task_{task_counter}",
            type=TaskType.CONFIG,
            description="Initialize project structure and configuration",
            dependencies=[],
            files_to_create=["pyproject.toml", "setup.py", ".gitignore"],
            agent="implementer"
        )
        tasks.append(config_task)

        # Step 3: Create code tasks (one per feature, or one default)
        code_task_ids = []
        if idea.features:
            for feature in idea.features:
                task_counter += 1
                task_id = f"task_{task_counter}"
                code_task = Task(
                    id=task_id,
                    type=TaskType.CODE,
                    description=f"Implement feature: {feature}",
                    dependencies=[config_task.id],
                    files_to_create=[self._infer_filename(feature)],
                    agent="implementer"
                )
                tasks.append(code_task)
                code_task_ids.append(task_id)
        else:
            # Create a single generic code task
            task_counter += 1
            task_id = f"task_{task_counter}"
            code_task = Task(
                id=task_id,
                type=TaskType.CODE,
                description="Implement core functionality",
                dependencies=[config_task.id],
                files_to_create=["src/main.py", "src/core.py"],
                agent="implementer"
            )
            tasks.append(code_task)
            code_task_ids.append(task_id)

        # Step 4: Create test tasks (one per code task)
        test_task_ids = []
        for code_task_id in code_task_ids:
            task_counter += 1
            task_id = f"task_{task_counter}"
            test_task = Task(
                id=task_id,
                type=TaskType.TEST,
                description=f"Write unit tests for {code_task_id}",
                dependencies=[code_task_id],
                files_to_create=[f"tests/test_{code_task_id}.py"],
                agent="tester"
            )
            tasks.append(test_task)
            test_task_ids.append(task_id)

        # Step 5: Create documentation tasks
        task_counter += 1
        readme_task = Task(
            id=f"task_{task_counter}",
            type=TaskType.DOC,
            description="Create README documentation",
            dependencies=code_task_ids,  # Depends on all code tasks
            files_to_create=["README.md"],
            agent="documenter"
        )
        tasks.append(readme_task)

        # Add usage examples doc if features are substantial
        if len(idea.features) >= 3:
            task_counter += 1
            examples_task = Task(
                id=f"task_{task_counter}",
                type=TaskType.DOC,
                description="Create usage examples and tutorials",
                dependencies=[readme_task.id],
                files_to_create=["docs/examples.md", "examples/demo.py"],
                agent="documenter"
            )
            tasks.append(examples_task)

        # Step 6: Build dependency graph
        dependency_graph = self._build_dependency_graph(tasks)

        # Validate for cycles
        if self._has_circular_dependencies(dependency_graph):
            warnings.append("Circular dependencies detected - plan may need adjustment")

        # Step 7: Estimate complexity
        complexity = self._estimate_complexity(idea, tasks)

        logger.info(
            f"Generated {len(tasks)} tasks with {complexity} complexity"
        )

        return PlanResult(
            tasks=tasks,
            dependency_graph=dependency_graph,
            estimated_complexity=complexity,
            warnings=warnings
        )

    def _infer_filename(self, feature: str) -> str:
        """
        Infer a module filename from a feature description

        Args:
            feature: Feature description

        Returns:
            str: Suggested filename (e.g., "src/parser.py")
        """
        # Extract key words and create a filename
        words = feature.lower().split()
        # Filter out common words
        stop_words = {"a", "an", "the", "and", "or", "for", "to", "from", "with"}
        key_words = [w for w in words if w not in stop_words and w.isalpha()]

        if key_words:
            filename = "_".join(key_words[:2]) + ".py"
        else:
            filename = "module.py"

        return f"src/{filename}"

    def _build_dependency_graph(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """
        Build dependency graph from task list

        Args:
            tasks: List of tasks

        Returns:
            Dict mapping task_id -> list of dependency task_ids
        """
        return {task.id: task.dependencies for task in tasks}

    def _has_circular_dependencies(self, graph: Dict[str, List[str]]) -> bool:
        """
        Check for circular dependencies using DFS

        Args:
            graph: Dependency graph

        Returns:
            bool: True if circular dependencies exist
        """
        visited = set()
        rec_stack = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True

        return False

    def _estimate_complexity(self, idea: Idea, tasks: List[Task]) -> str:
        """
        Estimate project complexity based on idea and task count

        Criteria:
        - Simple: 5 or fewer tasks, 1-2 features
        - Moderate: 6-10 tasks, 3-5 features
        - Complex: 11+ tasks, 6+ features

        Args:
            idea: Original idea
            tasks: Generated tasks

        Returns:
            str: "simple", "moderate", or "complex"
        """
        task_count = len(tasks)
        feature_count = len(idea.features) if idea.features else 1

        # Calculate complexity score
        score = 0

        # Task count factor
        if task_count <= 5:
            score += 0
        elif task_count <= 10:
            score += 1
        else:
            score += 2

        # Feature count factor
        if feature_count <= 2:
            score += 0
        elif feature_count <= 5:
            score += 1
        else:
            score += 2

        # Constraint factor (constraints indicate complexity)
        if len(idea.constraints) >= 3:
            score += 1

        # Map score to complexity level
        if score <= 1:
            return "simple"
        elif score <= 3:
            return "moderate"
        else:
            return "complex"
