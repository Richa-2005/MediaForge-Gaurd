"""
Learning-rate scheduler builder for MediaForge Vision.
"""

from __future__ import annotations

from typing import Any

import torch
from torch.optim.lr_scheduler import (
    CosineAnnealingLR,
    LinearLR,
    SequentialLR,
)


def build_scheduler(
    optimizer: torch.optim.Optimizer,
    config: dict[str, Any],
) -> torch.optim.lr_scheduler.LRScheduler:
    """
    Build a learning-rate scheduler from configuration.

    Currently supported:

        - cosine (with optional warmup)
    """

    scheduler_cfg = config["scheduler"]

    scheduler_name = scheduler_cfg["name"].lower()

    if scheduler_name != "cosine":
        raise ValueError(
            f"Unsupported scheduler: {scheduler_name}"
        )

    total_epochs = config["training"]["epochs"]

    warmup_epochs = scheduler_cfg.get(
        "warmup_epochs",
        0,
    )

    if warmup_epochs > 0:

        warmup = LinearLR(
            optimizer,
            start_factor=0.1,
            end_factor=1.0,
            total_iters=warmup_epochs,
        )

        cosine = CosineAnnealingLR(
            optimizer,
            T_max=max(
                total_epochs - warmup_epochs,
                1,
            ),
            eta_min=1e-6,
        )

        scheduler = SequentialLR(
            optimizer,
            schedulers=[
                warmup,
                cosine,
            ],
            milestones=[
                warmup_epochs,
            ],
        )

        return scheduler

    return CosineAnnealingLR(
        optimizer,
        T_max=total_epochs,
        eta_min=1e-6,
    )