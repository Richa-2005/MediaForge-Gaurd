"""
Evaluation metrics for MediaForge Vision.
"""

from __future__ import annotations

import torch

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


class Metrics:
    """
    Tracks predictions and computes classification metrics.
    """

    def __init__(self) -> None:

        self.reset()

    # ==========================================================
    # Reset
    # ==========================================================

    def reset(self) -> None:

        self.targets: list[int] = []

        self.predictions: list[int] = []

        self.probabilities: list[float] = []

    # ==========================================================
    # Update
    # ==========================================================

    @torch.no_grad()
    def update(
        self,
        logits: torch.Tensor,
        labels: torch.Tensor,
    ) -> None:
        """
        Update metric state from one batch.
        """

        probs = torch.softmax(
            logits,
            dim=1,
        )

        preds = torch.argmax(
            probs,
            dim=1,
        )

        self.targets.extend(
            labels.cpu().tolist()
        )

        self.predictions.extend(
            preds.cpu().tolist()
        )

        self.probabilities.extend(
            probs[:, 1].cpu().tolist()
        )

    # ==========================================================
    # Compute
    # ==========================================================

    def compute(
        self,
    ) -> dict[str, float | torch.Tensor]:
        """
        Compute all metrics.
        """

        accuracy = accuracy_score(
            self.targets,
            self.predictions,
        )

        precision = precision_score(
            self.targets,
            self.predictions,
            zero_division=0,
        )

        recall = recall_score(
            self.targets,
            self.predictions,
            zero_division=0,
        )

        f1 = f1_score(
            self.targets,
            self.predictions,
            zero_division=0,
        )

        cm = confusion_matrix(
            self.targets,
            self.predictions,
        )

        return {

            "accuracy": float(accuracy),

            "precision": float(precision),

            "recall": float(recall),

            "f1": float(f1),

            "confusion_matrix": torch.tensor(
                cm,
                dtype=torch.int64,
            ),
        }