from pathlib import Path

import whisper

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class TranscriptionAnalyzer(BaseAudioAnalyzer):

    def __init__(self):
        self.model = whisper.load_model("base")

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:

        result = self.model.transcribe(str(audio_path), fp16=False)

        transcript = result["text"].strip()

        language = result.get("language", "unknown")

        confidence = 1.0 if transcript else 0.0

        return Evidence(
            method="Whisper Transcription",
            score=0.0,
            confidence=confidence,
            summary="Speech transcribed using Whisper.",
            artifact_path=None,
            metadata={
                "language": language,
                "transcript": transcript,
                "word_count": len(transcript.split()),
                "character_count": len(transcript)
            },
        )