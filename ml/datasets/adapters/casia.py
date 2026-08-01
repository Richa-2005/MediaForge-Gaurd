"""
CASIA v2 Dataset Adapter.

Converts the CASIA v2 dataset into the canonical ImageMetadata format
used throughout the MediaForge Vision pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional

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
        Validate the CASIA dataset structure.
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

            images = list(iter_images(directory))

            if not images:
                raise ValueError(
                    f"No images found inside {directory}"
                )

            corrupt = [
                image
                for image in images
                if not verify_image(image)
            ]

            if corrupt:
                raise ValueError(
                    f"{len(corrupt)} corrupt images found in {directory}"
                )

        # Groundtruth masks are optional but, if present, should be a directory.
        groundtruth = self.root / "Groundtruth"

        if groundtruth.exists() and not groundtruth.is_dir():
            raise ValueError(
                "Groundtruth exists but is not a directory."
            )

    def discover(self) -> Iterator[tuple[Path, Authenticity]]:
        """
        Discover all dataset images.
        """

        for folder, authenticity in self.LABELS.items():

            directory = self.root / folder

            for image_path in iter_images(directory):
                yield image_path, authenticity

    def find_mask(self, image_path: Path) -> Optional[Path]:
        """
        Return the corresponding ground-truth mask if available.

        Matching rule:
            Tp_xxxxx.jpg
            ->
            Groundtruth/Tp_xxxxx.png
        """

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
        """

        width, height = get_image_size(image_path)

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
            channels=get_num_channels(image_path),
        )

    def build(self) -> Iterator[ImageMetadata]:
        """
        Stream ImageMetadata objects from the dataset.
        """

        self.validate()

        for image_path, authenticity in self.discover():
            yield self.map_sample(
                image_path,
                authenticity,
            )