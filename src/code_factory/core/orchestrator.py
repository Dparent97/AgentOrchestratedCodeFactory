"""
Orchestrator - Coordinates the entire code factory pipeline

The Orchestrator is the main controller that:
1. Accepts an Idea
2. Coordinates specialized agents to build the project
3. Manages the build pipeline stages
4. Returns a ProjectResult
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.checkpoint import CheckpointManager, Checkpoint
from code_factory.core.config import FactoryConfig, get_config
from code_factory.core.models import Idea, ProjectResult, ProjectSpec, Task, AgentRun
from code_factory.core.transaction import Transaction

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Main coordinator for the code factory
    
    Orchestrates the multi-agent pipeline to transform an Idea
    into a complete project.
    """
    
    def __init__(self, runtime: AgentRuntime, config: Optional[FactoryConfig] = None):
        """
        Initialize the orchestrator

        Args:
            runtime: AgentRuntime with registered agents
            config: Factory configuration (uses default if not provided)
        """
        self.runtime = runtime
        self.config = config or get_config()
        self.projects_dir = self.config.projects_dir
        self._current_run: Optional[ProjectResult] = None
        self._checkpoint_manager: Optional[CheckpointManager] = None
        self._completed_runs: List[AgentRun] = []
    
    def run_factory(self, idea: Idea) -> ProjectResult:
        """
        Execute the complete factory pipeline
        
        This is the main entry point for building a project from an idea.
        
        Args:
            idea: The project idea to build
            
        Returns:
            ProjectResult: Complete results including path and status
            
        Pipeline stages:
        1. Safety validation (SafetyGuard)
        2. Task planning (PlannerAgent)
        3. Architecture design (ArchitectAgent)
        4. Blue-collar advisory (BlueCollarAdvisor)
        5. Code generation (ImplementerAgent)
        6. Test creation (TesterAgent)
        7. Documentation (DocWriterAgent)
        8. Git initialization (GitOpsAgent)
        """
        start_time = datetime.now()
        logger.info("Starting factory run")
        logger.info(f"Idea: {idea.description}")
        
        result = ProjectResult(
            success=False,
            project_name="",
            agent_runs=[],
            errors=[]
        )
        
        try:
            # Stage 1: Safety validation
            logger.info("Stage 1: Safety validation")
            # TODO: Implement safety check
            # safety_run = self.runtime.execute_agent("safety_guard", idea)
            # result.agent_runs.append(safety_run)
            
            # Stage 2: Planning
            logger.info("Stage 2: Planning tasks")
            # TODO: Implement task planning
            # planner_run = self.runtime.execute_agent("planner", idea)
            # result.agent_runs.append(planner_run)
            
            # Stage 3: Architecture design
            logger.info("Stage 3: Architecture design")
            # TODO: Implement architecture design
            # architect_run = self.runtime.execute_agent("architect", ...)
            # result.agent_runs.append(architect_run)
            
            # Stage 4: Implementation
            logger.info("Stage 4: Code implementation")
            # TODO: Implement code generation
            
            # Stage 5: Testing
            logger.info("Stage 5: Test generation")
            # TODO: Implement test generation
            
            # Stage 6: Documentation
            logger.info("Stage 6: Documentation")
            # TODO: Implement documentation generation
            
            # Stage 7: Git initialization
            logger.info("Stage 7: Git initialization")
            # TODO: Implement Git operations
            
            # For now, mark as success (will be replaced with real logic)
            result.success = True
            result.project_name = "placeholder"
            
        except Exception as e:
            logger.error(f"Factory run failed: {e}")
            result.success = False
            result.errors.append(str(e))
        
        end_time = datetime.now()
        result.duration_seconds = (end_time - start_time).total_seconds()
        
        logger.info(f"Factory run completed: success={result.success}")
        return result
    
    def checkpoint(
        self,
        stage: str,
        idea: Idea,
        project_path: Optional[Path] = None,
        metadata: Optional[dict] = None
    ) -> Checkpoint:
        """
        Create a checkpoint at a major stage

        Saves pipeline state to enable resuming from this point.

        Args:
            stage: Stage name (e.g., "planning", "implementation")
            idea: Original project idea
            project_path: Path to project directory
            metadata: Additional metadata

        Returns:
            Checkpoint: Created checkpoint
        """
        logger.info(f"Creating checkpoint: {stage}")

        if not self._checkpoint_manager:
            project_name = metadata.get("project_name", "unknown") if metadata else "unknown"
            self._checkpoint_manager = CheckpointManager(project_name)

        checkpoint = self._checkpoint_manager.save_checkpoint(
            stage_name=stage,
            idea=idea,
            completed_runs=self._completed_runs.copy(),
            project_path=project_path,
            metadata=metadata or {},
        )

        logger.info(f"Checkpoint created: {checkpoint.checkpoint_id}")
        return checkpoint
    
    def handle_failure(
        self,
        agent_name: str,
        error: Exception,
        stage: str,
        idea: Idea,
        offer_recovery: bool = True
    ) -> dict:
        """
        Handle agent execution failure with recovery options

        Args:
            agent_name: Name of the failed agent
            error: The exception that occurred
            stage: Current pipeline stage
            idea: Original project idea
            offer_recovery: Whether to offer recovery options

        Returns:
            dict: Recovery options and information
        """
        logger.error(f"Agent {agent_name} failed at stage '{stage}': {error}")

        # Load last successful checkpoint
        last_checkpoint = None
        if self._checkpoint_manager:
            last_checkpoint = self._checkpoint_manager.load_checkpoint()

        recovery_info = {
            "failed_agent": agent_name,
            "failed_stage": stage,
            "error": str(error),
            "last_checkpoint": None,
            "can_resume": False,
            "recovery_options": [],
        }

        if last_checkpoint:
            recovery_info["last_checkpoint"] = {
                "stage": last_checkpoint.stage_name,
                "timestamp": last_checkpoint.timestamp.isoformat(),
                "checkpoint_id": last_checkpoint.checkpoint_id,
            }
            recovery_info["can_resume"] = True
            recovery_info["recovery_options"].append({
                "option": "resume",
                "description": f"Resume from checkpoint: {last_checkpoint.stage_name}",
            })

        if offer_recovery:
            recovery_info["recovery_options"].extend([
                {
                    "option": "retry",
                    "description": f"Retry stage '{stage}' from the beginning",
                },
                {
                    "option": "skip",
                    "description": f"Skip stage '{stage}' and continue (may cause issues)",
                },
                {
                    "option": "abort",
                    "description": "Abort the pipeline and clean up",
                },
            ])

        logger.info(
            f"Recovery options available: {len(recovery_info['recovery_options'])}"
        )

        return recovery_info

    def resume_from_checkpoint(self, checkpoint_id: Optional[str] = None) -> Optional[Checkpoint]:
        """
        Resume pipeline from a checkpoint

        Args:
            checkpoint_id: Specific checkpoint to resume from (uses latest if None)

        Returns:
            Checkpoint: Loaded checkpoint, or None if not found
        """
        if not self._checkpoint_manager:
            logger.error("No checkpoint manager available")
            return None

        checkpoint = self._checkpoint_manager.load_checkpoint(checkpoint_id)

        if checkpoint:
            logger.info(f"Resuming from checkpoint: {checkpoint.stage_name}")
            self._completed_runs = checkpoint.completed_runs.copy()

        return checkpoint
    
    def get_current_status(self) -> dict:
        """
        Get current orchestrator status
        
        Returns:
            Dict with status information
        """
        return {
            "projects_dir": str(self.projects_dir),
            "registered_agents": list(self.runtime.list_agents().keys()),
            "execution_history": len(self.runtime.get_execution_history())
        }
