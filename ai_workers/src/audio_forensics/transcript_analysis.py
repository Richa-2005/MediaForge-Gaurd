from pathlib import Path

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class TranscriptAnalyzer(BaseAudioAnalyzer):
    """
    Performs lightweight analysis of the transcript.
    """

    def analyze(
        self,
        transcript: str,
        language: str,
    ) -> Evidence:

        words = transcript.split()

        word_count = len(words)

        char_count = len(transcript)

        is_empty = word_count == 0

        return Evidence(
            method="Transcript Analysis",
            score=0.0,
            confidence=1.0,
            summary="Transcript statistics extracted.",
            artifact_path=None,
            metadata={
                "language": language,
                "word_count": word_count,
                "character_count": char_count,
                "is_empty": is_empty,
            },
        )