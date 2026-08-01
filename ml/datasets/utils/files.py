"""
Filesystem utilities for MediaForge Vision.

These helpers are dataset-agnostic and shared by all adapters.
"""

from pathlib import Path
from typing import Iterator

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
}


def is_image_file(path: Path) -> bool:
    """
    Returns True if the path looks like a supported image.
    """

    return (
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def iter_images(root: Path) -> Iterator[Path]:
    """
    Recursively yields image files in deterministic order.
    """

    if not root.exists():
        raise FileNotFoundError(root)

    for path in sorted(root.rglob("*")):
        if is_image_file(path):
            yield path


def safe_relative(path: Path, root: Path) -> Path:
    """
    Returns a relative path if possible.
    """

    try:
        return path.relative_to(root)
    except ValueError:
        return path