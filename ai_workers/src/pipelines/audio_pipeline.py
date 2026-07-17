from pathlib import Path

from src.audio_forensics.spectral import SpectralAnalyzer
from src.schemas import evidence
from src.audio_forensics.metadata import MetadataAnalyzer
from src.processors.audio_processor import extract_audio
from src.schemas.evidence import Evidence
from src.audio_forensics.silence import SilenceAnalyzer
from src.audio_forensics.mfcc import MFCCAnalyzer
from src.schemas.analysis_result import AnalysisResult
from src.audio_forensics.transcription import TranscriptionAnalyzer
from src.audio_forensics.quality import QualityAnalyzer

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
        TranscriptionAnalyzer()
    ]

    def run(
        self,
        video_path: Path,
        output_dir: Path,
    ) -> list[Evidence]:
        """
        Runs all available audio analyzers.

        Returns
        -------
        list[Evidence]
        """

        processed = extract_audio(video_path, output_dir)

        audio_path = Path(processed)

        evidence: list[Evidence] = []

        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(audio_path)

                if result is not None:
                    evidence.append(result)

            except Exception as e:
                print(
                    f"{analyzer.__class__.__name__} failed: {e}"
                )

        return evidence


if __name__ == "__main__":

    from src.config import (
        DATA_DIR,
        AUDIO_OUTPUT_DIR,
    )

    pipeline = AudioPipeline()

    result = pipeline.run(
        DATA_DIR / "sample_videos" / "demo_video.mp4",
        AUDIO_OUTPUT_DIR,
    )

    for item in result:
        print(item)