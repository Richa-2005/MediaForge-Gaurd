"""
Dataset registry.

Central factory responsible for creating dataset adapters.
"""

from pathlib import Path
from typing import Dict, Type

from .base import DatasetAdapter

# Filled automatically by adapters
_REGISTRY: Dict[str, Type[DatasetAdapter]] = {}


def register(name: str):
    """
    Decorator used by dataset adapters.
    """

    def decorator(cls: Type[DatasetAdapter]):
        if name in _REGISTRY:
            raise ValueError(f"Dataset '{name}' already registered.")

        _REGISTRY[name] = cls
        return cls

    return decorator


def create(name: str, root: Path) -> DatasetAdapter:
    """
    Create an adapter from its registered name.
    """

    if name not in _REGISTRY:
        raise KeyError(f"Unknown dataset: {name}")

    return _REGISTRY[name](root)


def available():
    """
    Return registered datasets.
    """

    return sorted(_REGISTRY.keys())