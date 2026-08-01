"""
Validation loop for MediaForge Vision.
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from .metrics import Metrics


class Validator:
    """
    Runs model evaluation on a validation dataset.
    """

    def __init__(
        self,
        model: nn.Module,
        criterion: nn.Module,
        dataloader: DataLoader,
        metrics: Metrics,
        device: torch.device,
    ) -> None:

        self.model = model
        self.criterion = criterion
        self.dataloader = dataloader
        self.metrics = metrics
        self.device = device

    @torch.no_grad()
    def validate(self) -> dict[str, float | torch.Tensor]:
        """
        Run one validation epoch.

        Returns
        -------
        Dictionary containing validation loss and metrics.
        """

        self.model.eval()

        self.metrics.reset()

        running_loss = 0.0

        total_batches = 0

        for images, labels in self.dataloader:

            images = images.to(
                self.device,
                non_blocking=True,
            )

            labels = labels.to(
                self.device,
                non_blocking=True,
            )

            logits = self.model(images)

            loss = self.criterion(
                logits,
                labels,
            )

            running_loss += loss.item()

            total_batches += 1

            self.metrics.update(
                logits,
                labels,
            )

        results = self.metrics.compute()

        results["loss"] = running_loss / max(
            total_batches,
            1,
        )

        return results