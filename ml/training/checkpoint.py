"""
Checkpoint management for MediaForge Vision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
import torch.nn as nn


class CheckpointManager:
    """
    Handles saving and loading training checkpoints.
    """

    def __init__(
        self,
        checkpoint_dir: Path,
    ) -> None:

        self.checkpoint_dir = Path(checkpoint_dir)

        self.checkpoint_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ============================================================
    # Save
    # ============================================================

    def save(
        self,
        *,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        scheduler: Any,
        epoch: int,
        best_metric: float,
        config: dict,
        filename: str = "checkpoint.pt",
    ) -> Path:
        """
        Save a training checkpoint.
        """

        checkpoint = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": (
                scheduler.state_dict()
                if scheduler is not None
                else None
            ),
            "best_metric": best_metric,
            "config": config,
        }

        path = self.checkpoint_dir / filename

        torch.save(
            checkpoint,
            path,
        )

        return path

    # ============================================================
    # Load
    # ============================================================

    def load(
        self,
        *,
        model: nn.Module,
        optimizer: torch.optim.Optimizer | None = None,
        scheduler: Any = None,
        filename: str = "checkpoint.pt",
        map_location: str | torch.device = "cpu",
    ) -> dict:
        """
        Load a training checkpoint.
        """

        path = self.checkpoint_dir / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Checkpoint not found: {path}"
            )

        checkpoint = torch.load(
            path,
            map_location=map_location,
        )

        model.load_state_dict(
            checkpoint["model_state_dict"]
        )

        if (
            optimizer is not None
            and checkpoint["optimizer_state_dict"] is not None
        ):
            optimizer.load_state_dict(
                checkpoint["optimizer_state_dict"]
            )

        if (
            scheduler is not None
            and checkpoint["scheduler_state_dict"] is not None
        ):
            scheduler.load_state_dict(
                checkpoint["scheduler_state_dict"]
            )

        return checkpoint

    # ============================================================
    # Save Best
    # ============================================================

    def save_best(
        self,
        *,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        scheduler: Any,
        epoch: int,
        best_metric: float,
        config: dict,
    ) -> Path:
        """
        Save the current best model.
        """

        return self.save(
            model=model,
            optimizer=optimizer,
            scheduler=scheduler,
            epoch=epoch,
            best_metric=best_metric,
            config=config,
            filename="best_model.pt",
        )

    # ============================================================
    # Latest Checkpoint
    # ============================================================

    def latest(self) -> Path | None:
        """
        Return the most recently modified checkpoint.
        """

        checkpoints = list(
            self.checkpoint_dir.glob("*.pt")
        )

        if not checkpoints:
            return None

        return max(
            checkpoints,
            key=lambda path: path.stat().st_mtime,
        )