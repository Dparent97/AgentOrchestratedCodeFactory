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
from code_factory.core.code_writer import CodeWriter
from code_factory.core.config import FactoryConfig, get_config
from code_factory.core.models import (
    Idea,
    ProjectResult,
    ProjectSpec,
    Task,
    AgentRun,
    SafetyCheck,
    PlanResult,
    ArchitectResult,
)
from code_factory.core.transaction import Transaction

# Agent-specific input models
from code_factory.agents.architect import ArchitectInput
from code_factory.agents.tester import TestInput
from code_factory.agents.git_ops import GitOperation
from code_factory.agents.implementer import CodeOutput

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
        4. Code generation (ImplementerAgent)
        5. Test creation (TesterAgent)
        6. Documentation (DocWriterAgent)
        7. Git initialization (GitOpsAgent)
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
        
        # Track state for pipeline stages
        plan_result: Optional[PlanResult] = None
        architect_result: Optional[ArchitectResult] = None
        code_output: Optional[CodeOutput] = None
        project_path: Optional[Path] = None
        
        try:
            # Stage 1: Safety validation
            logger.info("Stage 1: Safety validation")
            safety_run = self.runtime.execute_agent("safety_guard", idea)
            result.agent_runs.append(safety_run)
            self._completed_runs.append(safety_run)
            
            if safety_run.status != "success":
                error_msg = f"Safety check failed: {safety_run.error}"
                logger.error(error_msg)
                recovery = self.handle_failure("safety_guard", Exception(error_msg), "safety", idea)
                result.errors.append(error_msg)
                result.errors.append(f"Recovery options: {recovery}")
                return self._finalize_result(result, start_time)
            
            # Check if idea was approved
            safety_check = SafetyCheck(**safety_run.output_data)
            if not safety_check.approved:
                error_msg = f"Idea rejected by SafetyGuard: {', '.join(safety_check.warnings)}"
                if safety_check.blocked_keywords:
                    error_msg += f" Blocked keywords: {', '.join(safety_check.blocked_keywords)}"
                logger.error(error_msg)
                result.errors.append(error_msg)
                return self._finalize_result(result, start_time)
            
            logger.info("Safety check passed")
            if safety_check.warnings:
                logger.warning(f"Safety warnings: {safety_check.warnings}")
            
            # Create checkpoint after safety validation
            self.checkpoint("safety_validated", idea, metadata={"warnings": safety_check.warnings})
            
            # Stage 2: Planning
            logger.info("Stage 2: Planning tasks")
            planner_run = self.runtime.execute_agent("planner", idea)
            result.agent_runs.append(planner_run)
            self._completed_runs.append(planner_run)
            
            if planner_run.status != "success":
                error_msg = f"Planning failed: {planner_run.error}"
                logger.error(error_msg)
                recovery = self.handle_failure("planner", Exception(error_msg), "planning", idea)
                result.errors.append(error_msg)
                return self._finalize_result(result, start_time)
            
            plan_result = PlanResult(**planner_run.output_data)
            logger.info(f"Generated {len(plan_result.tasks)} tasks, complexity: {plan_result.estimated_complexity}")
            
            # Create checkpoint after planning
            self.checkpoint("planning_complete", idea, metadata={
                "task_count": len(plan_result.tasks),
                "complexity": plan_result.estimated_complexity
            })
            
            # Stage 3: Architecture design
            logger.info("Stage 3: Architecture design")
            architect_input = ArchitectInput(idea=idea, tasks=plan_result.tasks)
            architect_run = self.runtime.execute_agent("architect", architect_input)
            result.agent_runs.append(architect_run)
            self._completed_runs.append(architect_run)
            
            if architect_run.status != "success":
                error_msg = f"Architecture design failed: {architect_run.error}"
                logger.error(error_msg)
                recovery = self.handle_failure("architect", Exception(error_msg), "architecture", idea)
                result.errors.append(error_msg)
                return self._finalize_result(result, start_time)
            
            architect_result = ArchitectResult(**architect_run.output_data)
            spec = architect_result.spec
            result.project_name = spec.name
            
            logger.info(f"Project: {spec.name}, Blue-collar score: {architect_result.blue_collar_score:.1f}/10")
            
            # Create checkpoint after architecture
            self.checkpoint("architecture_complete", idea, metadata={
                "project_name": spec.name,
                "blue_collar_score": architect_result.blue_collar_score
            })
            
            # Stage 4: Implementation
            logger.info("Stage 4: Code implementation")
            implementer_run = self.runtime.execute_agent("implementer", spec)
            result.agent_runs.append(implementer_run)
            self._completed_runs.append(implementer_run)
            
            if implementer_run.status != "success":
                error_msg = f"Code implementation failed: {implementer_run.error}"
                logger.error(error_msg)
                recovery = self.handle_failure("implementer", Exception(error_msg), "implementation", idea)
                result.errors.append(error_msg)
                return self._finalize_result(result, start_time)
            
            code_output = CodeOutput(**implementer_run.output_data)
            logger.info(f"Generated {code_output.files_created} code files")
            
            # Create project directory and write files
            project_path = self.projects_dir / spec.name
            project_path.mkdir(parents=True, exist_ok=True)
            result.project_path = str(project_path)
            
            code_writer = CodeWriter(project_path)
            code_writer.write_project_files(code_output.files)
            logger.info(f"Wrote {len(code_output.files)} files to {project_path}")
            
            # Create checkpoint after implementation
            self.checkpoint("implementation_complete", idea, project_path=project_path, metadata={
                "files_created": code_output.files_created
            })
            
            # Stage 5: Testing
            logger.info("Stage 5: Test generation")
            test_input = TestInput(spec=spec, code_files=code_output.files)
            tester_run = self.runtime.execute_agent("tester", test_input)
            result.agent_runs.append(tester_run)
            self._completed_runs.append(tester_run)
            
            if tester_run.status != "success":
                # Testing failures are warnings, not fatal errors
                logger.warning(f"Test generation had issues: {tester_run.error}")
            else:
                from code_factory.core.models import TestResult
                test_result = TestResult(**tester_run.output_data.get("test_result", tester_run.output_data))
                logger.info(f"Tests: {test_result.passed}/{test_result.total_tests} passed")
            
            # Stage 6: Documentation
            logger.info("Stage 6: Documentation")
            doc_run = self.runtime.execute_agent("doc_writer", spec)
            result.agent_runs.append(doc_run)
            self._completed_runs.append(doc_run)
            
            if doc_run.status != "success":
                # Doc failures are warnings, not fatal errors
                logger.warning(f"Documentation generation had issues: {doc_run.error}")
            else:
                from code_factory.agents.doc_writer import DocOutput
                doc_output = DocOutput(**doc_run.output_data)
                # Write additional doc files (may overwrite/supplement existing)
                if doc_output.files:
                    code_writer.write_project_files(doc_output.files)
                    logger.info(f"Generated {len(doc_output.files)} documentation files")
            
            # Stage 7: Git initialization
            logger.info("Stage 7: Git initialization")
            git_init_op = GitOperation(
                repo_path=str(project_path),
                operation="init"
            )
            git_init_run = self.runtime.execute_agent("git_ops", git_init_op)
            result.agent_runs.append(git_init_run)
            self._completed_runs.append(git_init_run)
            
            if git_init_run.status == "success":
                # Create initial commit
                git_commit_op = GitOperation(
                    repo_path=str(project_path),
                    operation="commit",
                    message=f"Initial commit: {spec.name}\n\n{spec.description}"
                )
                git_commit_run = self.runtime.execute_agent("git_ops", git_commit_op)
                result.agent_runs.append(git_commit_run)
                self._completed_runs.append(git_commit_run)
                
                if git_commit_run.status == "success":
                    logger.info("Git repository initialized with initial commit")
                else:
                    logger.warning(f"Initial commit failed: {git_commit_run.error}")
            else:
                logger.warning(f"Git initialization had issues: {git_init_run.error}")
            
            # Create final checkpoint
            self.checkpoint("pipeline_complete", idea, project_path=project_path, metadata={
                "project_name": spec.name,
                "files_created": code_output.files_created,
                "success": True
            })
            
            # Mark as success
            result.success = True
            logger.info(f"Factory run completed successfully: {spec.name}")
            
        except Exception as e:
            logger.error(f"Factory run failed: {e}", exc_info=True)
            result.success = False
            result.errors.append(str(e))
            
            # Try to create failure checkpoint
            try:
                self.checkpoint("pipeline_failed", idea, project_path=project_path, metadata={
                    "error": str(e)
                })
            except Exception:
                pass  # Don't let checkpoint failure mask original error
        
        return self._finalize_result(result, start_time)
    
    def _finalize_result(self, result: ProjectResult, start_time: datetime) -> ProjectResult:
        """
        Finalize a ProjectResult by setting duration and logging completion.
        
        Args:
            result: The ProjectResult to finalize
            start_time: When the factory run started
            
        Returns:
            ProjectResult: The finalized result with duration set
        """
        end_time = datetime.now()
        result.duration_seconds = (end_time - start_time).total_seconds()
        
        logger.info(f"Factory run completed: success={result.success}, duration={result.duration_seconds:.2f}s")
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
