from pathlib import Path

import librosa
import numpy as np

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class MFCCAnalyzer(BaseAudioAnalyzer):
    """
    Extracts MFCC features from an audio signal.
    """

    def __init__(
        self,
        n_mfcc: int = 13,
    ):
        self.n_mfcc = n_mfcc

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:

        signal, sample_rate = librosa.load(
            audio_path,
            sr=None,
        )

        mfcc = librosa.feature.mfcc(
            y=signal,
            sr=sample_rate,
            n_mfcc=self.n_mfcc,
        )

        mean = np.mean(mfcc)

        std = np.std(mfcc)

        score = min(
            1.0,
            abs(mean) / 100,
        )

        return Evidence(
            method="MFCC Analysis",
            score=round(score, 4),
            confidence=round(score, 4),
            summary="Extracted Mel-Frequency Cepstral Coefficients.",
            artifact_path=None,
            metadata={
                "mfcc_mean": round(float(mean), 4),
                "mfcc_std": round(float(std), 4),
                "coefficients": self.n_mfcc,
            },
        )