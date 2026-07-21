from pathlib import Path

import librosa
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

        # Whisper shells out to a system `ffmpeg` executable when given
        # a path. Librosa already supports the application's audio
        # formats, so pass decoded 16 kHz samples directly instead.
        audio, _ = librosa.load(
            audio_path,
            sr=whisper.audio.SAMPLE_RATE,
            mono=True,
        )
        result = self.model.transcribe(audio, fp16=False)

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
