from pathlib import Path

import cv2
import numpy as np

from src.forensics.base import BaseForensicAnalyzer
from src.schemas.evidence import Evidence


class NoiseAnalyzer(BaseForensicAnalyzer):
    """
    Performs image noise analysis using high-pass residuals.

    The goal is to highlight regions whose sensor noise pattern
    differs from the surrounding image.
    """

    def __init__(self, blur_kernel: int = 5):
        self.blur_kernel = blur_kernel

    def generate_residual(self, image: np.ndarray) -> np.ndarray:
        """
        Generate high-frequency residual by subtracting
        a Gaussian blurred image.
        """

        blurred = cv2.GaussianBlur(
            image,
            (self.blur_kernel, self.blur_kernel),
            0,
        )

        residual = cv2.absdiff(image, blurred)

        return residual

    def compute_score(self, residual: np.ndarray) -> float:
        """
        Compute normalized noise score.
        """

        gray = cv2.cvtColor(residual, cv2.COLOR_BGR2GRAY)

        score = float(gray.mean() / 255.0)

        return round(score, 4)

    def analyze(
        self,
        image_path: Path,
        artifact_path: Path | None = None,
    ) -> Evidence:
        """
        Run noise analysis and return an Evidence object.
        """

        image = self.load_image(image_path)

        residual = self.generate_residual(image)

        score = self.compute_score(residual)

        if artifact_path is not None:
            self.save_artifact(
                residual,
                artifact_path,
            )

        confidence = min(1.0, score * 1.5)

        return Evidence(
            method="Noise Analysis",
            score=score,
            confidence=round(confidence, 4),
            summary="Analyzed high-frequency residual noise patterns.",
            artifact_path=str(artifact_path) if artifact_path else None,
            metadata={
                "kernel_size": self.blur_kernel,
                "algorithm": "Gaussian High-Pass Residual",
            },
        )


if __name__ == "__main__":

    analyzer = NoiseAnalyzer()

    evidence = analyzer.analyze(
        image_path=Path("data/sample_images/sample_img.jpg"),
        artifact_path=Path("outputs/forensics/noise_residual.png"),
    )

    print(evidence)