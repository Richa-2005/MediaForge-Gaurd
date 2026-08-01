from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

from .metadata import ImageMetadata


class DatasetAdapter(ABC):

    def __init__(self, root: Path):
        self.root = Path(root)

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def build(self) -> Iterator[ImageMetadata]:
        ...

    def __iter__(self) -> Iterator[ImageMetadata]:
        yield from self.build()

    def __len__(self) -> int:
        raise TypeError(
            "Streaming dataset adapters do not expose __len__()."
        )