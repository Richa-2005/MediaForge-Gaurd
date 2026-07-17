from abc import ABC, abstractmethod
from pathlib import Path

import cv2
import numpy as np

from src.schemas.evidence import Evidence


class BaseForensicAnalyzer(ABC):
    """
    Base class for all forensic analyzers.

    Every analyzer should return an Evidence object.
    """

    def load_image(self, image_path: Path) -> np.ndarray:
        """
        Loads an image from disk.
        """

        if not image_path.exists():
            raise FileNotFoundError(image_path)

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(f"Unable to load image: {image_path}")

        return image

    def save_artifact(
        self,
        artifact: np.ndarray,
        output_path: Path,
    ) -> None:
        """
        Saves an artifact image.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(str(output_path), artifact)

    @abstractmethod
    def analyze(
        self,
        image_path: Path,
        artifact_path: Path | None = None,
    ) -> Evidence:
        """
        Runs forensic analysis and returns Evidence.
        """

        pass