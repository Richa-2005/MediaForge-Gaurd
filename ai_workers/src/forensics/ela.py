from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops

from src.forensics.base import BaseForensicAnalyzer
from src.schemas.evidence import Evidence


class ELAAnalyzer(BaseForensicAnalyzer):
    """
    Performs Error Level Analysis (ELA) on JPEG images.

    ELA highlights regions with inconsistent JPEG compression,
    which may indicate image manipulation.
    """

    def __init__(
        self,
        jpeg_quality: int = 90,
        scale: float = 15.0,
    ):
        self.jpeg_quality = jpeg_quality
        self.scale = scale

    def generate_ela(
        self,
        image_path: Path,
    ) -> np.ndarray:
        """
        Generates an ELA visualization as a NumPy array.
        """

        image = self.load_image(image_path)

        original = Image.fromarray(
            cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB,
            )
        )

        temp_file = image_path.with_suffix(".ela_temp.jpg")

        original.save(
            temp_file,
            "JPEG",
            quality=self.jpeg_quality,
        )

        recompressed = Image.open(temp_file)

        diff = ImageChops.difference(
            original,
            recompressed,
        )

        diff_array = np.array(diff).astype(np.float32)

        diff_array *= self.scale

        diff_array = np.clip(
            diff_array,
            0,
            255,
        ).astype(np.uint8)

        temp_file.unlink(missing_ok=True)

        return diff_array

    def compute_score(
        self,
        ela_image: np.ndarray,
    ) -> float:
        """
        Computes a normalized ELA score.
        """

        score = float(
            ela_image.mean() / 255.0
        )

        return round(score, 4)

    def analyze(
        self,
        image_path: Path,
        artifact_path: Path | None = None,
    ) -> Evidence:
        """
        Runs Error Level Analysis and returns Evidence.
        """

        ela_image = self.generate_ela(
            image_path
        )

        score = self.compute_score(
            ela_image
        )

        if artifact_path is not None:

            ela_bgr = cv2.cvtColor(
                ela_image,
                cv2.COLOR_RGB2BGR,
            )

            self.save_artifact(
                ela_bgr,
                artifact_path,
            )

        confidence = min(
            score * 1.5,
            1.0,
        )

        return Evidence(
            method="ELA",
            score=score,
            confidence=round(
                confidence,
                4,
            ),
            summary="JPEG compression inconsistencies analyzed using Error Level Analysis.",
            artifact_path=str(artifact_path)
            if artifact_path
            else None,
            metadata={
                "jpeg_quality": self.jpeg_quality,
                "scale": self.scale,
                "algorithm": "Error Level Analysis",
            },
        )


if __name__ == "__main__":

    analyzer = ELAAnalyzer()

    evidence = analyzer.analyze(
        image_path=Path(
            "data/sample_images/sample_img.jpg"
        ),
        artifact_path=Path(
            "outputs/forensics/ela.png"
        ),
    )

    print(evidence)