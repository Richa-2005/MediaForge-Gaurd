"""
MediaForge Vision Trainer.

Coordinates model training.
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import DataLoader


class Trainer:
    """
    Trainer for MediaForge Vision.

    Responsible for:
        - Forward pass
        - Loss computation
        - Backpropagation
        - Optimizer step
    """

    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        train_loader: DataLoader,
        device: torch.device,
        mixed_precision: bool = False,
    ) -> None:

        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.train_loader = train_loader
        self.device = device

        self.mixed_precision = (
            mixed_precision and device.type == "cuda"
        )

        self.scaler = torch.amp.GradScaler(
            "cuda",
            enabled=self.mixed_precision,
        )

        self.model.to(self.device)

    def train_step(
        self,
        batch,
    ) -> dict[str, float]:

        if len(batch) == 3:
            images, labels, _ = batch
        else:
            images, labels = batch

        images = images.to(
            self.device,
            non_blocking=True,
        )

        labels = labels.to(
            self.device,
            non_blocking=True,
        )

        self.optimizer.zero_grad(
            set_to_none=True,
        )

        with torch.amp.autocast(
            "cuda",
            enabled=self.mixed_precision,
        ):

            logits = self.model(images)

            loss = self.criterion(
                logits,
                labels,
            )

        self.scaler.scale(loss).backward()

        self.scaler.unscale_(self.optimizer)

        torch.nn.utils.clip_grad_norm_(
            self.model.parameters(),
            max_norm=1.0,
        )

        self.scaler.step(self.optimizer)

        self.scaler.update()

        return {
            "loss": loss.item(),
            "batch_size": images.size(0),
        }

    def train_epoch(
        self,
    ) -> dict[str, float]:

        self.model.train()

        running_loss = 0.0

        total_samples = 0

        for batch in self.train_loader:

            output = self.train_step(batch)

            batch_size = output["batch_size"]

            running_loss += (
                output["loss"] * batch_size
            )

            total_samples += batch_size

        return {
            "loss": running_loss / max(
                total_samples,
                1,
            ),
        }