from pathlib import Path

import librosa
import numpy as np

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class QualityAnalyzer(BaseAudioAnalyzer):
    """
    Evaluates the overall quality of an extracted audio signal.

    Metrics:
    - RMS Energy
    - Peak Amplitude
    - Dynamic Range
    - Clipping Ratio
    """

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:

        signal, sample_rate = librosa.load(
            audio_path,
            sr=None,
            mono=True,
        )

        # Root Mean Square Energy
        rms = librosa.feature.rms(y=signal)[0]

        rms_energy = float(np.mean(rms))

        # Peak Amplitude
        peak_amplitude = float(np.max(np.abs(signal)))

        # Dynamic Range
        dynamic_range = float(np.max(signal) - np.min(signal))

        # Percentage of clipped samples
        clipping_ratio = float(
            np.mean(np.abs(signal) >= 0.99)
        )

        # Simple heuristic score
        score = clipping_ratio

        confidence = min(
            1.0,
            dynamic_range,
        )

        return Evidence(
            method="Audio Quality",
            score=round(score, 4),
            confidence=round(confidence, 4),
            summary="Measured audio quality indicators.",
            artifact_path=None,
            metadata={
                "sample_rate": sample_rate,
                "rms_energy": round(rms_energy, 4),
                "peak_amplitude": round(
                    peak_amplitude,
                    4,
                ),
                "dynamic_range": round(
                    dynamic_range,
                    4,
                ),
                "clipping_ratio": round(
                    clipping_ratio,
                    6,
                ),
                "analysis_method": "RMS + Peak + Dynamic Range",
            },
        )