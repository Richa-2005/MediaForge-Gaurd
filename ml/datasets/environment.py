"""
Environment detection for MediaForge Vision.

Automatically selects the correct dataset root depending on
whether the code is running locally or inside Kaggle.
"""

from __future__ import annotations

import os
from pathlib import Path


class Environment:
    """
    Detects the current execution environment.

    Supported:

        - Local development

        - Kaggle Notebook
    """

    @staticmethod
    def is_kaggle() -> bool:
        """
        Return True when running inside Kaggle.
        """

        return (
            "KAGGLE_KERNEL_RUN_TYPE" in os.environ
            or Path("/kaggle").exists()
        )

    @staticmethod
    def dataset_root(dataset_cfg: dict) -> Path:
        """
        Return the correct dataset root.

        Parameters
        ----------
        dataset_cfg
            One dataset section from datasets.yaml.
        """

        key = (
            "kaggle_root"
            if Environment.is_kaggle()
            else "fixture_root"
        )

        root = dataset_cfg.get(key)

        if root is None:
            raise KeyError(
                f"'{key}' missing from dataset configuration."
            )

        return Path(root)

    @staticmethod
    def working_directory() -> Path:
        """
        Return the working directory.

        Local:
            project root

        Kaggle:
            /kaggle/working
        """

        if Environment.is_kaggle():
            return Path("/kaggle/working")

        return Path.cwd()

    @staticmethod
    def manifest_directory() -> Path:
        """
        Directory where manifests are stored.
        """

        directory = (
            Environment.working_directory()
            / "artifacts"
            / "manifests"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory