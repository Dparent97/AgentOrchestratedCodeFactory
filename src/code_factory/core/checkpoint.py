"""
Checkpoint system for saving and restoring pipeline state

Enables resuming from the last successful stage if a failure occurs.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from code_factory.core.config import get_config
from code_factory.core.models import AgentRun, Idea, ProjectResult

logger = logging.getLogger(__name__)


class Checkpoint:
    """
    Represents a saved checkpoint at a specific pipeline stage

    Contains all information needed to resume from this point.
    """

    def __init__(
        self,
        stage_name: str,
        idea: Idea,
        completed_runs: List[AgentRun],
        project_path: Optional[Path] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.stage_name = stage_name
        self.idea = idea
        self.completed_runs = completed_runs
        self.project_path = project_path
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        self.checkpoint_id = f"{stage_name}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize checkpoint to dictionary"""
        return {
            "checkpoint_id": self.checkpoint_id,
            "stage_name": self.stage_name,
            "timestamp": self.timestamp.isoformat(),
            "idea": self.idea.model_dump(),
            "completed_runs": [run.model_dump() for run in self.completed_runs],
            "project_path": str(self.project_path) if self.project_path else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Checkpoint":
        """Deserialize checkpoint from dictionary"""
        checkpoint = cls(
            stage_name=data["stage_name"],
            idea=Idea(**data["idea"]),
            completed_runs=[AgentRun(**run) for run in data["completed_runs"]],
            project_path=Path(data["project_path"]) if data["project_path"] else None,
            metadata=data.get("metadata", {}),
        )
        checkpoint.checkpoint_id = data["checkpoint_id"]
        checkpoint.timestamp = datetime.fromisoformat(data["timestamp"])
        return checkpoint


class CheckpointManager:
    """
    Manages checkpoint creation, storage, and restoration

    Checkpoints are saved to disk and can be used to resume pipeline
    execution from the last successful stage.
    """

    def __init__(self, project_name: Optional[str] = None):
        """
        Initialize checkpoint manager

        Args:
            project_name: Optional project name for organizing checkpoints
        """
        self.config = get_config()
        self.project_name = project_name or "default"

        # Create checkpoint directory structure
        self.checkpoint_root = self.config.checkpoint_dir / self.project_name
        self.checkpoint_root.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        stage_name: str,
        idea: Idea,
        completed_runs: List[AgentRun],
        project_path: Optional[Path] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Checkpoint:
        """
        Save a checkpoint at a specific stage

        Args:
            stage_name: Name of the completed stage
            idea: Original project idea
            completed_runs: List of completed agent runs
            project_path: Path to project directory
            metadata: Additional metadata to store

        Returns:
            Checkpoint: Created checkpoint
        """
        checkpoint = Checkpoint(
            stage_name=stage_name,
            idea=idea,
            completed_runs=completed_runs,
            project_path=project_path,
            metadata=metadata,
        )

        # Save to file
        checkpoint_file = self.checkpoint_root / f"{checkpoint.checkpoint_id}.json"

        try:
            with open(checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(checkpoint.to_dict(), f, indent=2, default=str)

            logger.info(f"Checkpoint saved: {stage_name} -> {checkpoint_file}")

            # Save as "latest" checkpoint
            latest_file = self.checkpoint_root / "latest.json"
            with open(latest_file, "w", encoding="utf-8") as f:
                json.dump(checkpoint.to_dict(), f, indent=2, default=str)

            return checkpoint

        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            raise

    def load_checkpoint(
        self, checkpoint_id: Optional[str] = None
    ) -> Optional[Checkpoint]:
        """
        Load a checkpoint

        Args:
            checkpoint_id: Specific checkpoint ID to load (loads latest if None)

        Returns:
            Checkpoint: Loaded checkpoint, or None if not found
        """
        try:
            if checkpoint_id:
                checkpoint_file = self.checkpoint_root / f"{checkpoint_id}.json"
            else:
                # Load latest checkpoint
                checkpoint_file = self.checkpoint_root / "latest.json"

            if not checkpoint_file.exists():
                logger.warning(f"Checkpoint not found: {checkpoint_file}")
                return None

            with open(checkpoint_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            checkpoint = Checkpoint.from_dict(data)
            logger.info(f"Checkpoint loaded: {checkpoint.stage_name}")

            return checkpoint

        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """
        List all available checkpoints

        Returns:
            List of checkpoint metadata dictionaries
        """
        checkpoints = []

        try:
            for checkpoint_file in self.checkpoint_root.glob("*.json"):
                if checkpoint_file.name == "latest.json":
                    continue

                with open(checkpoint_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                checkpoints.append({
                    "checkpoint_id": data["checkpoint_id"],
                    "stage_name": data["stage_name"],
                    "timestamp": data["timestamp"],
                })

            # Sort by timestamp (newest first)
            checkpoints.sort(key=lambda x: x["timestamp"], reverse=True)

            return checkpoints

        except Exception as e:
            logger.error(f"Failed to list checkpoints: {e}")
            return []

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete a specific checkpoint

        Args:
            checkpoint_id: Checkpoint ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        try:
            checkpoint_file = self.checkpoint_root / f"{checkpoint_id}.json"

            if not checkpoint_file.exists():
                logger.warning(f"Checkpoint not found: {checkpoint_id}")
                return False

            checkpoint_file.unlink()
            logger.info(f"Checkpoint deleted: {checkpoint_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to delete checkpoint: {e}")
            return False

    def cleanup_old_checkpoints(self, keep_count: int = 10) -> int:
        """
        Clean up old checkpoints, keeping only the most recent N

        Args:
            keep_count: Number of checkpoints to keep

        Returns:
            int: Number of checkpoints deleted
        """
        try:
            checkpoints = self.list_checkpoints()

            if len(checkpoints) <= keep_count:
                return 0

            # Delete oldest checkpoints
            deleted = 0
            for checkpoint in checkpoints[keep_count:]:
                if self.delete_checkpoint(checkpoint["checkpoint_id"]):
                    deleted += 1

            logger.info(f"Cleaned up {deleted} old checkpoints")
            return deleted

        except Exception as e:
            logger.error(f"Failed to cleanup checkpoints: {e}")
            return 0

    def clear_all_checkpoints(self) -> int:
        """
        Delete all checkpoints for this project

        Returns:
            int: Number of checkpoints deleted
        """
        try:
            deleted = 0

            for checkpoint_file in self.checkpoint_root.glob("*.json"):
                checkpoint_file.unlink()
                deleted += 1

            logger.info(f"Cleared all checkpoints: {deleted}")
            return deleted

        except Exception as e:
            logger.error(f"Failed to clear checkpoints: {e}")
            return 0
