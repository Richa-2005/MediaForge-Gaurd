from pathlib import Path

from src.audio_forensics.spectral import SpectralAnalyzer
from src.audio_forensics.metadata import MetadataAnalyzer
from src.processors.audio_processor import extract_audio
from src.schemas.evidence import Evidence
from src.audio_forensics.silence import SilenceAnalyzer
from src.audio_forensics.mfcc import MFCCAnalyzer
from src.audio_forensics.transcription import TranscriptionAnalyzer
from src.audio_forensics.quality import QualityAnalyzer

import logging

logger = logging.getLogger(__name__)

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
}


class AudioPipeline:
    """
    Executes the complete audio analysis pipeline.
    """

    def __init__(self):
        self.analyzers = [
            MetadataAnalyzer(),
            SilenceAnalyzer(),
            SpectralAnalyzer(),
            MFCCAnalyzer(),
            QualityAnalyzer(),
            TranscriptionAnalyzer(),
        ]

    def run(
        self,
        media_path: Path,
        output_dir: Path,
    ) -> list[Evidence]:
        """
        Runs all available audio analyzers.

        Accepts either:
        - a direct audio file
        - a video file containing an audio track
        """

        media_path = Path(media_path)

        if not media_path.exists():
            raise FileNotFoundError(
                f"Audio pipeline input file not found: {media_path}"
            )

        if media_path.suffix.lower() in AUDIO_EXTENSIONS:
            audio_path = media_path
        else:
            processed = extract_audio(media_path, output_dir)
            audio_path = Path(processed)

        evidence: list[Evidence] = []

        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(audio_path)

                if result is not None:
                    evidence.append(result)

            except Exception as e:
                logger.exception(
                    "%s failed",
                    analyzer.__class__.__name__,
                )

        return evidence
