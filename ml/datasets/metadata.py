"""
Canonical metadata object used throughout MediaForge Vision.

Every dataset adapter converts its native format into ImageMetadata.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .taxonomy import (
    Authenticity,
    Origin,
    Technique,
    Generator,
    Split,
)


@dataclass(slots=True)
class ImageMetadata:
    """
    Standard representation of a single image sample.
    """

    # ---------- Identity ----------
    image_id: str
    dataset: str

    # ---------- Files ----------
    image_path: Path
    mask_path: Optional[Path] = None

    # ---------- Labels ----------
    authenticity: Authenticity = Authenticity.INCONCLUSIVE
    origin: Origin = Origin.UNKNOWN
    technique: Technique = Technique.UNKNOWN
    generator: Generator = Generator.UNKNOWN

    # ---------- Dataset ----------
    split: Split = Split.TRAIN

    # ---------- Image Info ----------
    width: Optional[int] = None
    height: Optional[int] = None
    channels: Optional[int] = None

    # ---------- Optional ----------
    metadata: Optional[dict] = None