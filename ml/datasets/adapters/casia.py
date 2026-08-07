"""
CASIA v2 Dataset Adapter.

Converts the CASIA v2 dataset into the canonical ImageMetadata format
used throughout the MediaForge Vision pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional

from PIL import Image

from ..base import DatasetAdapter
from ..metadata import ImageMetadata
from ..registry import register
from ..taxonomy import (
    Authenticity,
    Generator,
    Origin,
    Split,
    Technique,
)
from ..utils.files import iter_images


@register("casia")
class CASIAAdapter(DatasetAdapter):
    """
    Adapter for the CASIA v2 dataset.

    Expected structure:

    root/
        Au/
        Tp/
        Groundtruth/
    """

    LABELS = {
        "Au": Authenticity.AUTHENTIC,
        "Tp": Authenticity.NOT_AUTHENTIC,
    }

    @property
    def name(self) -> str:
        return "casia"

    def validate(self) -> None:
        """
        Lightweight validation.

        Only verify directory structure.
        Heavy image verification is intentionally omitted
        for production manifest generation.
        """

        if not self.root.exists():
            raise FileNotFoundError(
                f"Dataset root not found: {self.root}"
            )

        for folder in self.LABELS:

            directory = self.root / folder

            if not directory.exists():
                raise FileNotFoundError(
                    f"Missing required folder: {directory}"
                )

        groundtruth = self.root / "Groundtruth"

        if groundtruth.exists() and not groundtruth.is_dir():
            raise ValueError(
                "Groundtruth exists but is not a directory."
            )

    def discover(self) -> Iterator[tuple[Path, Authenticity]]:
        """
        Discover dataset images.
        """

        for folder, authenticity in self.LABELS.items():

            directory = self.root / folder

            if not directory.exists():
                continue

            for image_path in iter_images(directory):
                yield image_path, authenticity

    def find_mask(
        self,
        image_path: Path,
    ) -> Optional[Path]:

        if image_path.parent.name != "Tp":
            return None

        mask = (
            self.root
            / "Groundtruth"
            / f"{image_path.stem}.png"
        )

        return mask if mask.exists() else None

    def map_sample(
        self,
        image_path: Path,
        authenticity: Authenticity,
    ) -> ImageMetadata:
        """
        Convert one CASIA image into ImageMetadata.

        Opens every image only once.
        """

        with Image.open(image_path) as image:

            width, height = image.size
            channels = len(image.getbands())

        return ImageMetadata(
            image_id=f"CASIA_{image_path.stem}",
            dataset=self.name,
            image_path=image_path,
            mask_path=self.find_mask(image_path),
            authenticity=authenticity,
            origin=Origin.CAMERA,
            technique=(
                Technique.NONE
                if authenticity == Authenticity.AUTHENTIC
                else Technique.UNKNOWN
            ),
            generator=Generator.NONE,
            split=Split.TRAIN,
            width=width,
            height=height,
            channels=channels,
        )

    def build(self) -> Iterator[ImageMetadata]:
        """
        Stream ImageMetadata objects.

        Validation is intentionally not executed here.
        """

        for image_path, authenticity in self.discover():

            yield self.map_sample(
                image_path,
                authenticity,
            )