"""
Loss functions for MediaForge Vision.

Current Version:
    - Weighted Cross Entropy
    - Label Smoothing
    - Easy future extension to Focal Loss
"""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn


class AuthenticityLoss(nn.Module):
    """
    Binary authenticity classification loss.

    Supports:

    - Class weighting
    - Label smoothing
    """

    def __init__(
        self,
        class_weights: Optional[list[float]] = None,
        label_smoothing: float = 0.0,
    ) -> None:

        super().__init__()

        weight_tensor = None

        if class_weights is not None:
            weight_tensor = torch.tensor(
                class_weights,
                dtype=torch.float32,
            )

        self.criterion = nn.CrossEntropyLoss(
            weight=weight_tensor,
            label_smoothing=label_smoothing,
        )

    def forward(
        self,
        logits: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:

        return self.criterion(
            logits,
            labels,
        )


def build_loss(config: dict) -> nn.Module:
    """
    Build the training loss from configuration.
    """

    loss_cfg = config.get("loss", {})

    class_weights = None

    if loss_cfg.get("use_class_weights", False):
        class_weights = loss_cfg.get(
            "class_weights",
            None,
        )

    return AuthenticityLoss(
        class_weights=class_weights,
        label_smoothing=loss_cfg.get(
            "label_smoothing",
            0.0,
        ),
    )