"""
COCO Dataset Adapter.

Converts the COCO dataset into the canonical ImageMetadata format used
throughout the MediaForge Vision pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

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


@register("coco")
class COCOAdapter(DatasetAdapter):
    """
    Adapter for the Microsoft COCO dataset.

    Expected structure:

    root/
        train2017/
        val2017/
        test2017/
    """

    SPLITS = {
        "train2017": Split.TRAIN,
        "val2017": Split.VAL,
        "test2017": Split.TEST,
    }

    @property
    def name(self) -> str:
        return "coco"

    def validate(self) -> None:
        """
        Lightweight validation.

        Heavy image verification should NOT run while building
        production manifests.
        """

        if not self.root.exists():
            raise FileNotFoundError(
                f"Dataset root not found: {self.root}"
            )

        discovered_split = False

        for folder in self.SPLITS:

            split_dir = self.root / folder

            if split_dir.exists():
                discovered_split = True

        if not discovered_split:
            raise ValueError(
                "No valid COCO split folders were found."
            )

    def discover(self) -> Iterator[tuple[Path, Split]]:
        """
        Discover all dataset images.
        """

        for folder, split in self.SPLITS.items():

            split_dir = self.root / folder

            if not split_dir.exists():
                continue

            for image_path in iter_images(split_dir):
                yield image_path, split

    def map_sample(
        self,
        image_path: Path,
        split: Split,
    ) -> ImageMetadata:
        """
        Convert one COCO image into ImageMetadata.

        Opens every image only once.
        """

        with Image.open(image_path) as image:

            width, height = image.size
            channels = len(image.getbands())

        return ImageMetadata(
            image_id=f"COCO_{image_path.stem}",
            dataset=self.name,
            image_path=image_path,
            authenticity=Authenticity.AUTHENTIC,
            origin=Origin.CAMERA,
            technique=Technique.NONE,
            generator=Generator.NONE,
            split=split,
            width=width,
            height=height,
            channels=channels,
        )

    def build(self) -> Iterator[ImageMetadata]:
        """
        Stream ImageMetadata samples.

        Validation is intentionally omitted here because production
        manifest generation should not spend hours verifying every
        image before processing.
        """

        for image_path, split in self.discover():
            yield self.map_sample(
                image_path,
                split,
            )