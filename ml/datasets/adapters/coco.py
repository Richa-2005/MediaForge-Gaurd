"""
COCO Dataset Adapter.

Converts the COCO dataset into the canonical ImageMetadata format used
throughout the MediaForge Vision pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

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
from ..utils.images import (
    get_image_size,
    get_num_channels,
    verify_image,
)


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
        Validate the COCO dataset structure.
        """

        if not self.root.exists():
            raise FileNotFoundError(
                f"Dataset root not found: {self.root}"
            )

        discovered_split = False

        for folder in self.SPLITS:

            split_dir = self.root / folder

            if not split_dir.exists():
                continue

            discovered_split = True

            images = list(iter_images(split_dir))

            if not images:
                raise ValueError(
                    f"No images found inside {split_dir}"
                )

            corrupt = [
                image
                for image in images
                if not verify_image(image)
            ]

            if corrupt:
                raise ValueError(
                    f"{len(corrupt)} corrupt images detected "
                    f"in {split_dir}"
                )

        if not discovered_split:
            raise ValueError(
                "No valid COCO split folders were found."
            )

    def discover(self) -> Iterator[tuple[Path, Split]]:
        """
        Discover all dataset images.

        Yields
        ------
        tuple[Path, Split]
            Image path and corresponding dataset split.
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
        """

        width, height = get_image_size(image_path)

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
            channels=get_num_channels(image_path),
            
        )

    def build(self) -> Iterator[ImageMetadata]:
        """
        Stream ImageMetadata samples from the dataset.
        """

        self.validate()

        for image_path, split in self.discover():
            yield self.map_sample(image_path, split)