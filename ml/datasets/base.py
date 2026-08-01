"""
Abstract base class for all dataset adapters.

Every dataset must inherit from DatasetAdapter and implement
the required interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, List

from .metadata import ImageMetadata


class DatasetAdapter(ABC):
    """
    Base class for every dataset adapter.
    """

    def __init__(self, root: Path):
        self.root = Path(root)

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable dataset name.
        """
        ...

    @abstractmethod
    def validate(self) -> None:
        """
        Verify dataset structure before processing.

        Raises:
            FileNotFoundError
            ValueError
        """
        ...

    @abstractmethod
    def build(self) -> List[ImageMetadata]:
        """
        Convert the dataset into ImageMetadata objects.
        """
        ...

    def __iter__(self) -> Iterator[ImageMetadata]:
        """
        Allows:

        for sample in adapter:
            ...
        """
        yield from self.build()

    def __len__(self) -> int:
        return len(self.build())