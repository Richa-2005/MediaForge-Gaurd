from pathlib import Path

import cv2
import numpy as np

from src.forensics.base import BaseForensicAnalyzer
from src.schemas.evidence import Evidence


class BlurAnalyzer(BaseForensicAnalyzer):
    """
    Performs blur analysis using the Variance of the Laplacian.

    Lower variance generally indicates a blurrier image.
    """

    def generate_laplacian(self, image: np.ndarray) -> np.ndarray:
        """
        Compute the Laplacian image.
        """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        laplacian = cv2.Laplacian(
            gray,
            cv2.CV_64F,
        )

        return laplacian

    def create_visualization(
        self,
        laplacian: np.ndarray,
    ) -> np.ndarray:
        """
        Convert Laplacian to an 8-bit visualization.
        """

        visualization = cv2.convertScaleAbs(laplacian)

        return visualization

    def compute_score(
        self,
        laplacian: np.ndarray,
    ) -> float:
        """
        Compute normalized blur score.

        Higher score = sharper image.
        """

        variance = laplacian.var()

        score = min(
            variance / 1000.0,
            1.0,
        )

        return round(float(score), 4)

    def analyze(
        self,
        image_path: Path,
        artifact_path: Path | None = None,
    ) -> Evidence:

        image = self.load_image(image_path)

        laplacian = self.generate_laplacian(image)

        visualization = self.create_visualization(
            laplacian
        )

        score = self.compute_score(
            laplacian
        )

        if artifact_path is not None:
            self.save_artifact(
                visualization,
                artifact_path,
            )

        confidence = min(
            score * 1.4,
            1.0,
        )

        return Evidence(
            method="Blur Analysis",
            score=score,
            confidence=round(confidence, 4),
            summary="Estimated image sharpness using the Variance of the Laplacian.",
            artifact_path=str(artifact_path)
            if artifact_path
            else None,
            metadata={
                "algorithm": "Variance of Laplacian",
            },
        )


if __name__ == "__main__":

    analyzer = BlurAnalyzer()

    evidence = analyzer.analyze(
        image_path=Path(
            "data/sample_images/sample_img.jpg"
        ),
        artifact_path=Path(
            "outputs/forensics/blur_map.png"
        ),
    )

    print(evidence)