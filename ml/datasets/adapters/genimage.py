"""
Tiny GenImage Dataset Adapter.

Converts the Tiny GenImage dataset into the canonical ImageMetadata
representation used throughout MediaForge Vision.
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


@register("genimage")
class GenImageAdapter(DatasetAdapter):
    """
    Adapter for Tiny GenImage.

    Expected structure:

    root/
        imagenet_ai_0419_biggan/
            train/
                ai/
                nature/
            val/
                ai/
                nature/

        imagenet_ai_0419_vqdm/
        imagenet_ai_0424_sdv5/
        imagenet_ai_0424_wukong/
        imagenet_ai_0508_adm/
        imagenet_glide/
        imagenet_midjourney/
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
        Validate dataset structure.
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

                images = list(iter_images(split_dir))

                if not images:
                    raise ValueError(
                        f"No images found inside {split_dir}"
                    )

                corrupt = [
                    img
                    for img in images
                    if not verify_image(img)
                ]

                if corrupt:
                    raise ValueError(
                        f"{len(corrupt)} corrupt images found in {split_dir}"
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

            for split_name, split in self.SPLITS.items():

                split_dir = dataset_dir / split_name

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
        """

        width, height = get_image_size(image_path)

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
            channels=get_num_channels(image_path),
        )

    def build(self) -> Iterator[ImageMetadata]:
        """
        Stream ImageMetadata objects.
        """

        self.validate()

        for image_path, generator, split in self.discover():

            yield self.map_sample(
                image_path=image_path,
                generator=generator,
                split=split,
            )