"""
MediaForge Vision Model.

Configurable ConvNeXt backbone for image authenticity detection.
"""

from __future__ import annotations

from typing import Literal

import torch
import torch.nn as nn
from torchvision.models import (
    ConvNeXt_Tiny_Weights,
    ConvNeXt_Small_Weights,
    convnext_small,
    convnext_tiny,
)


SUPPORTED_BACKBONES = {
    "convnext_tiny": (
        convnext_tiny,
        ConvNeXt_Tiny_Weights.DEFAULT,
        768,
    ),
    "convnext_small": (
        convnext_small,
        ConvNeXt_Small_Weights.DEFAULT,
        768,
    ),
}


class MediaForgeVision(nn.Module):
    """
    ConvNeXt-based authenticity classifier.
    """

    def __init__(
        self,
        backbone: Literal[
            "convnext_tiny",
            "convnext_small",
        ] = "convnext_tiny",
        pretrained: bool = True,
        dropout: float = 0.30,
        hidden_dim: int = 512,
        num_classes: int = 2,
    ) -> None:

        super().__init__()

        if backbone not in SUPPORTED_BACKBONES:
            raise ValueError(
                f"Unsupported backbone: {backbone}"
            )

        model_builder, weights, feature_dim = SUPPORTED_BACKBONES[
            backbone
        ]

        self.backbone = model_builder(
            weights=weights if pretrained else None
        )

        self.backbone.classifier = nn.Identity()

        self.classifier = nn.Sequential(

            nn.Linear(
                feature_dim,
                hidden_dim,
            ),

            nn.ReLU(inplace=True),

            nn.Dropout(
                p=dropout,
            ),

            nn.Linear(
                hidden_dim,
                num_classes,
            ),
        )

    def forward(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """
        Returns raw logits.

        """
        features = self.backbone(images)

# ConvNeXt returns (B, C, 1, 1) when classifier is removed.
        if features.ndim == 4:
            features = torch.flatten(features, 1)

        logits = self.classifier(features)

        return logits

        