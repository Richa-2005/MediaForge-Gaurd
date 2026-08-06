"""
Optimizer builder for MediaForge Vision.
"""

from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn


def build_optimizer(
    model: nn.Module,
    config: dict[str, Any],
) -> torch.optim.Optimizer:
    """
    Build optimizer from the training configuration.
    """

    optimizer_cfg = config["optimizer"]

    optimizer_name = optimizer_cfg["name"].lower()

    if optimizer_name != "adamw":
        raise ValueError(
            f"Unsupported optimizer: {optimizer_name}"
        )

    learning_rate = optimizer_cfg.get(
        "learning_rate",
        3e-4,
    )

    backbone_lr = optimizer_cfg.get(
        "backbone_lr",
        learning_rate,
    )

    classifier_lr = optimizer_cfg.get(
        "classifier_lr",
        learning_rate,
    )

    parameter_groups = [

        {
            "params": model.backbone.parameters(),
            "lr": backbone_lr,
        },

        {
            "params": model.classifier.parameters(),
            "lr": classifier_lr,
        },

    ]

    return torch.optim.AdamW(

        params=parameter_groups,

        lr=learning_rate,

        weight_decay=optimizer_cfg.get(
            "weight_decay",
            1e-4,
        ),

        betas=tuple(
            optimizer_cfg.get(
                "betas",
                (0.9, 0.999),
            )
        ),

        eps=optimizer_cfg.get(
            "eps",
            1e-8,
        ),
    )