"""
Dataset environment resolution for MediaForge Vision.

Supports:

- Local fixtures
- Standard Kaggle datasets
- KaggleHub datasets
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


class Environment:
    """
    Resolves dataset locations for the current environment.
    """

    @staticmethod
    def is_kaggle() -> bool:
        """
        Detect Kaggle runtime.
        """
        return (
            "KAGGLE_KERNEL_RUN_TYPE" in os.environ
            or Path("/kaggle").exists()
        )

    @staticmethod
    def dataset_root(dataset_cfg: dict[str, Any]) -> Path:
        """
        Resolve the dataset root automatically.
        """

        # -----------------------------
        # Local development
        # -----------------------------

        if not Environment.is_kaggle():

            root = Path(dataset_cfg["fixture_root"])

            if root.exists():
                return root

            raise FileNotFoundError(
                f"Fixture dataset not found:\n{root}"
            )

        # -----------------------------
        # Kaggle
        # -----------------------------

        configured = Path(dataset_cfg["kaggle_root"])

        if configured.exists():
            return configured

        dataset_name = configured.name.lower()

        kagglehub_root = Path("/kaggle/input/datasets")

        if kagglehub_root.exists():

            candidates: list[Path] = []

            for path in kagglehub_root.rglob("*"):

                if not path.is_dir():
                    continue

                name = path.name.lower()

                if dataset_name in name:
                    candidates.append(path)

            #
            # Prefer dataset roots
            #

            for candidate in candidates:

                names = {
                    p.name.lower()
                    for p in candidate.iterdir()
                    if p.is_dir()
                }

                #
                # CASIA
                #

                if {
                    "au",
                    "tp",
                }.issubset(names):

                    return candidate

                #
                # COCO
                #

                if {
                    "train2017",
                    "val2017",
                    "annotations",
                }.issubset(names):

                    return candidate

                #
                # GenImage
                #

                if any(
                    child.name.startswith("imagenet")
                    for child in candidate.iterdir()
                    if child.is_dir()
                ):
                    return candidate

        raise FileNotFoundError(
            f"Unable to locate dataset:\n{dataset_cfg['kaggle_root']}"
        )