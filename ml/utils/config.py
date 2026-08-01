"""
Configuration utilities for MediaForge Vision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(
    config_path: str | Path,
) -> dict[str, Any]:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    config_path
        Path to the YAML configuration.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            f"Configuration file is empty: {config_path}"
        )

    return config
