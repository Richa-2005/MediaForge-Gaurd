from pathlib import Path

import cv2
import numpy as np

from src.forensics.base import BaseForensicAnalyzer
from src.schemas.evidence import Evidence


class FFTAnalyzer(BaseForensicAnalyzer):
    """
    Performs frequency-domain analysis using the
    Fast Fourier Transform (FFT).
    """

    def generate_spectrum(self, image: np.ndarray) -> np.ndarray:
        """
        Generate a log-scaled FFT magnitude spectrum.
        """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        fft = np.fft.fft2(gray)

        fft_shift = np.fft.fftshift(fft)

        magnitude = np.abs(fft_shift)

        spectrum = np.log1p(magnitude)

        spectrum = cv2.normalize(
            spectrum,
            None,
            0,
            255,
            cv2.NORM_MINMAX,
        )

        return spectrum.astype(np.uint8)

    def compute_score(self, spectrum: np.ndarray) -> float:
        """
        Compute a normalized frequency-domain score.
        """

        score = float(spectrum.mean() / 255.0)

        return round(score, 4)

    def analyze(
        self,
        image_path: Path,
        artifact_path: Path | None = None,
    ) -> Evidence:
        """
        Run FFT analysis and return an Evidence object.
        """

        image = self.load_image(image_path)

        spectrum = self.generate_spectrum(image)

        score = self.compute_score(spectrum)

        if artifact_path is not None:
            self.save_artifact(
                spectrum,
                artifact_path,
            )

        confidence = min(1.0, score * 1.4)

        return Evidence(
            method="FFT Analysis",
            score=score,
            confidence=round(confidence, 4),
            summary="Frequency-domain characteristics analyzed.",
            artifact_path=str(artifact_path) if artifact_path else None,
            metadata={
                "algorithm": "2D FFT",
            },
        )


if __name__ == "__main__":

    analyzer = FFTAnalyzer()

    evidence = analyzer.analyze(
        image_path=Path("data/sample_images/sample_img.jpg"),
        artifact_path=Path("outputs/forensics/fft_spectrum.png"),
    )

    print(evidence)