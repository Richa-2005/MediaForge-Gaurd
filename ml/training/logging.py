"""
Experiment logging utilities for MediaForge Vision.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import yaml


class ExperimentLogger:
    """
    Handles experiment directories, logging and metric storage.
    """

    def __init__(
        self,
        experiment_name: str,
        output_root: str | Path = "artifacts/experiments",
    ) -> None:

        self.experiment_dir = (
            Path(output_root)
            / experiment_name
        )

        self.experiment_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logger = logging.getLogger(
            experiment_name
        )

        self.logger.setLevel(
            logging.INFO
        )

        # Avoid duplicate handlers if recreated
        self.logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            self.experiment_dir / "train.log",
            encoding="utf-8",
        )

        file_handler.setFormatter(
            formatter
        )

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(
            formatter
        )

        self.logger.addHandler(
            file_handler
        )

        self.logger.addHandler(
            console_handler
        )

        self.metrics_path = (
            self.experiment_dir
            / "metrics.json"
        )

        self.metrics: list[dict] = []

    # ==========================================================
    # Configuration
    # ==========================================================

    def save_config(
        self,
        config: dict,
    ) -> None:

        with (
            self.experiment_dir
            / "config.yaml"
        ).open(
            "w",
            encoding="utf-8",
        ) as file:

            yaml.safe_dump(
                config,
                file,
                sort_keys=False,
            )

    # ==========================================================
    # Logging
    # ==========================================================

    def info(
        self,
        message: str,
    ) -> None:

        self.logger.info(
            message
        )

    def warning(
        self,
        message: str,
    ) -> None:

        self.logger.warning(
            message
        )

    def error(
        self,
        message: str,
    ) -> None:

        self.logger.error(
            message
        )

    # ==========================================================
    # Metrics
    # ==========================================================

    def log_metrics(
        self,
        epoch: int,
        metrics: dict,
    ) -> None:

        record = {
            "epoch": epoch,
            **metrics,
        }

        self.metrics.append(
            record
        )

        with self.metrics_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.metrics,
                file,
                indent=4,
            )

    # ==========================================================
    # Paths
    # ==========================================================

    @property
    def directory(self) -> Path:

        return self.experiment_dir