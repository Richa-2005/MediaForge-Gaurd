"""
Image utilities.
"""

from pathlib import Path
from PIL import Image


def verify_image(path: Path) -> bool:
    """
    Checks whether an image can be opened.
    """

    try:
        with Image.open(path) as img:
            img.verify()
        return True

    except Exception:
        return False


def get_image_size(path: Path):
    """
    Returns (width, height).
    """

    with Image.open(path) as img:
        return img.size


def get_num_channels(path: Path):
    """
    Returns number of channels.
    """

    with Image.open(path) as img:
        return len(img.getbands())