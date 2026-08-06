"""
PyTorch Dataset for MediaForge Vision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset


class VisionDataset(Dataset):
    """
    Loads images using the canonical manifest.

    Parameters
    ----------
    manifest
        Path to the canonical manifest parquet file.

    transform
        Optional torchvision transform.

    return_metadata
        If True, returns (image, label, metadata).
        Otherwise returns (image, label).
    """

    def __init__(
        self,
        manifest: str | Path,
        transform: Callable | None = None,
        return_metadata: bool = False,
    ) -> None:

        self.manifest = pd.read_parquet(manifest)

        self.transform = transform

        self.return_metadata = return_metadata

    def __len__(self) -> int:
        return len(self.manifest)

    def __getitem__(self, index: int):

        row = self.manifest.iloc[index]

        image = Image.open(
            row.image_path
        ).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        label = (
            0
            if row.authenticity == "authentic"
            else 1
        )

        if not self.return_metadata:
            return image, label

        metadata = {
            "image_id": row.image_id,
            "dataset": row.dataset,
            "origin": row.origin,
            "generator": row.generator,
            "technique": row.technique,
            "split": row.split,
        }

        return image, label, metadata