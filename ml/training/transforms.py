"""
Image transformation pipelines for MediaForge Vision.

Separate pipelines are provided for:

- Training
- Validation
- Inference
"""

from __future__ import annotations

import albumentations as A
from albumentations.pytorch import ToTensorV2


# ============================================================
# Constants
# ============================================================

IMAGE_SIZE = 224

IMAGENET_MEAN = (
    0.485,
    0.456,
    0.406,
)

IMAGENET_STD = (
    0.229,
    0.224,
    0.225,
)


# ============================================================
# Training
# ============================================================

def get_train_transforms() -> A.Compose:
    """
    Training augmentations.

    Designed for image forensic detection while preserving
    manipulation artifacts.
    """

    return A.Compose(

        [

            # ---------- Resize ----------
            A.LongestMaxSize(
                max_size=256,
            ),

            A.PadIfNeeded(
                min_height=256,
                min_width=256,
                border_mode=0,
            ),

            A.RandomCrop(
                IMAGE_SIZE,
                IMAGE_SIZE,
            ),

            # ---------- Geometry ----------
            A.HorizontalFlip(
                p=0.5,
            ),

            A.Rotate(
                limit=5,
                border_mode=0,
                p=0.3,
            ),

            # ---------- Color ----------
            A.ColorJitter(
                brightness=0.10,
                contrast=0.10,
                saturation=0.05,
                hue=0.02,
                p=0.30,
            ),

            # ---------- Compression ----------
            A.ImageCompression(
                quality_range=(70, 100),
                p=0.40,
            ),

            # ---------- Noise ----------
            A.GaussNoise(
                std_range=(0.01, 0.04),
                p=0.15,
            ),

            # ---------- Blur ----------
            A.GaussianBlur(
                blur_limit=(3, 3),
                p=0.08,
            ),

            # ---------- Normalize ----------
            A.Normalize(
                mean=IMAGENET_MEAN,
                std=IMAGENET_STD,
            ),

            ToTensorV2(),

        ]
    )


# ============================================================
# Validation
# ============================================================

def get_val_transforms() -> A.Compose:
    """
    Validation transforms.
    """

    return A.Compose(

        [

            A.LongestMaxSize(
                max_size=IMAGE_SIZE,
            ),

            A.PadIfNeeded(
                IMAGE_SIZE,
                IMAGE_SIZE,
                border_mode=0,
            ),

            A.CenterCrop(
                IMAGE_SIZE,
                IMAGE_SIZE,
            ),

            A.Normalize(
                mean=IMAGENET_MEAN,
                std=IMAGENET_STD,
            ),

            ToTensorV2(),

        ]
    )


# ============================================================
# Inference
# ============================================================

def get_inference_transforms() -> A.Compose:
    """
    Inference transforms.
    """

    return get_val_transforms()