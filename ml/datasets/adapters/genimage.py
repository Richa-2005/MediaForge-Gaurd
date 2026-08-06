"""
Tiny GenImage Dataset Adapter.

Converts the Tiny GenImage dataset into the canonical ImageMetadata
representation used throughout MediaForge Vision.
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


@register("genimage")
class GenImageAdapter(DatasetAdapter):
    """
    Adapter for Tiny GenImage.
    """

    GENERATORS = {
        "imagenet_ai_0419_biggan": Generator.BIGGAN,
        "imagenet_ai_0419_vqdm": Generator.VQDM,
        "imagenet_ai_0424_sdv5": Generator.STABLE_DIFFUSION_V5,
        "imagenet_ai_0424_wukong": Generator.WUKONG,
        "imagenet_ai_0508_adm": Generator.ADM,
        "imagenet_glide": Generator.GLIDE,
        "imagenet_midjourney": Generator.MIDJOURNEY,
    }

    SPLITS = {
        "train": Split.TRAIN,
        "val": Split.VAL,
    }

    @property
    def name(self) -> str:
        return "genimage"

    def validate(self) -> None:
        """
        Lightweight validation.

        Only verifies directory structure.
        """

        if not self.root.exists():
            raise FileNotFoundError(
                f"Dataset root not found: {self.root}"
            )

        for folder in self.GENERATORS:

            dataset_dir = self.root / folder

            if not dataset_dir.exists():
                raise FileNotFoundError(
                    f"Missing generator folder: {dataset_dir}"
                )

            for split in self.SPLITS:

                split_dir = dataset_dir / split

                if not split_dir.exists():
                    raise FileNotFoundError(
                        f"Missing split directory: {split_dir}"
                    )

    def discover(
        self,
    ) -> Iterator[
        tuple[
            Path,
            Generator,
            Split,
        ]
    ]:
        """
        Discover all dataset images.
        """

        for folder, generator in self.GENERATORS.items():

            dataset_dir = self.root / folder

            if not dataset_dir.exists():
                continue

            for split_name, split in self.SPLITS.items():

                split_dir = dataset_dir / split_name

                if not split_dir.exists():
                    continue

                for image_path in iter_images(split_dir):

                    yield (
                        image_path,
                        generator,
                        split,
                    )

    def map_sample(
        self,
        image_path: Path,
        generator: Generator,
        split: Split,
    ) -> ImageMetadata:
        """
        Convert one image into ImageMetadata.

        Opens each image only once.
        """

        with Image.open(image_path) as image:

            width, height = image.size
            channels = len(image.getbands())

        return ImageMetadata(
            image_id=f"GENIMAGE_{generator.value}_{image_path.stem}",
            dataset=self.name,
            image_path=image_path,
            authenticity=Authenticity.NOT_AUTHENTIC,
            origin=Origin.AI,
            technique=Technique.AI_GENERATED,
            generator=generator,
            split=split,
            width=width,
            height=height,
            channels=channels,
        )

    def build(self) -> Iterator[ImageMetadata]:
        """
        Stream ImageMetadata objects.

        Validation is intentionally omitted during production
        manifest generation.
        """

        for image_path, generator, split in self.discover():

            yield self.map_sample(
                image_path=image_path,
                generator=generator,
                split=split,
            )