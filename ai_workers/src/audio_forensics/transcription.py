from pathlib import Path
import os

import librosa
import whisper

from src.audio_forensics.base import BaseAudioAnalyzer
from src.clients.audio_inference_client import RemoteAudioInferenceClient
from src.schemas.evidence import Evidence


class TranscriptionAnalyzer(BaseAudioAnalyzer):

    def __init__(self):
        self.provider = os.getenv("AUDIO_INFERENCE_PROVIDER", "local").strip().lower()
        self.remote_client = None
        self.model = None

        if self.provider == "modal":
            self.remote_client = RemoteAudioInferenceClient()
        elif self.provider == "local":
            self.model = whisper.load_model("base")
        else:
            raise ValueError(
                "Unsupported AUDIO_INFERENCE_PROVIDER: "
                f"{self.provider}. Expected 'local' or 'modal'."
            )

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:
        if self.provider == "modal":
            result = self.remote_client.transcribe(audio_path)
        else:
            result = self._transcribe_locally(audio_path)

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

    def _transcribe_locally(
        self,
        audio_path: Path,
    ) -> dict:
        # Whisper shells out to a system `ffmpeg` executable when given
        # a path. Librosa already supports the application's audio
        # formats, so pass decoded 16 kHz samples directly instead.
        audio, _ = librosa.load(
            audio_path,
            sr=whisper.audio.SAMPLE_RATE,
            mono=True,
        )
        return self.model.transcribe(audio, fp16=False)
