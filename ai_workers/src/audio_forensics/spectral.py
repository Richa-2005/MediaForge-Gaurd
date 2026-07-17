from pathlib import Path

import librosa
import numpy as np

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class SpectralAnalyzer(BaseAudioAnalyzer):
    """
    Performs simple spectral analysis of an audio signal.
    """

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:

        signal, sample_rate = librosa.load(
            audio_path,
            sr=None,
        )

        spectral_centroid = librosa.feature.spectral_centroid(
            y=signal,
            sr=sample_rate,
        )

        centroid = float(
            np.mean(spectral_centroid)
        )

        score = min(
            1.0,
            centroid / 8000,
        )

        return Evidence(
            method="Spectral Analysis",
            score=round(score, 4),
            confidence=round(score, 4),
            summary="Computed spectral centroid of the audio.",
            artifact_path=None,
            metadata={
                "spectral_centroid": round(
                    centroid,
                    2,
                ),
                "sample_rate": sample_rate,
            },
        )