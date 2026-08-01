"""
Hashing utilities for MediaForge Vision.

Used for:
- Duplicate detection
- Dataset validation
- Manifest integrity
- Experiment reproducibility
"""

from __future__ import annotations

import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024  # 1 MB


def _hash_file(path: Path, algorithm: str) -> str:
    """
    Compute a hash for a file using the specified algorithm.

    Parameters
    ----------
    path : Path
        Path to the file.

    algorithm : str
        hashlib algorithm name.

    Returns
    -------
    str
        Hex digest.
    """

    hasher = hashlib.new(algorithm)

    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)

    return hasher.hexdigest()


def sha256(path: Path) -> str:
    """Return SHA256 hash of a file."""
    return _hash_file(path, "sha256")


def md5(path: Path) -> str:
    """Return MD5 hash of a file."""
    return _hash_file(path, "md5")