from pathlib import Path

import librosa
import numpy as np

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class SilenceAnalyzer(BaseAudioAnalyzer):
    """
    Detects unusually large silent regions in audio.
    """

    def __init__(
        self,
        threshold_db: float = 25,
    ):
        self.threshold_db = threshold_db

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:

        signal, sample_rate = librosa.load(
            audio_path,
            sr=None,
        )

        intervals = librosa.effects.split(
            signal,
            top_db=self.threshold_db,
        )

        duration = len(signal) / sample_rate

        speech_duration = sum(
            (end - start)
            for start, end in intervals
        ) / sample_rate

        silence_duration = max(
            0.0,
            duration - speech_duration,
        )

        silence_ratio = silence_duration / duration

        return Evidence(
            method="Silence Analysis",
            score=round(silence_ratio, 4),
            confidence=round(
                min(
                    1.0,
                    silence_ratio * 2,
                ),
                4,
            ),
            summary="Detected silent regions in the audio.",
            artifact_path=None,
            metadata={
                "duration_seconds": round(float(duration), 2),
                "speech_seconds": round(float(speech_duration), 2),
                "silence_seconds": round(float(silence_duration), 2),
                "silence_ratio": round(float(silence_ratio), 4),
                "speech_ratio": round(float(1 - silence_ratio), 4),
                "analysis_method": "librosa_rms_energy",
                "silence_threshold_db": self.threshold_db,
            }
            
        )
    