from pathlib import Path

from moviepy import AudioFileClip

from src.audio_forensics.base import BaseAudioAnalyzer
from src.schemas.evidence import Evidence


class MetadataAnalyzer(BaseAudioAnalyzer):
    """
    Extracts basic metadata from an audio file.
    """

    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        with AudioFileClip(str(audio_path)) as clip:

            duration = round(float(clip.duration), 2)

            fps = clip.fps

            channels = getattr(
                clip,
                "nchannels",
                None,
            )

        return Evidence(
            method="Audio Metadata",
            score=1.0,
            confidence=1.0,
            summary="Successfully extracted audio metadata.",
            artifact_path=None,
            metadata={
                "duration_seconds": duration,
                "sample_rate": fps,
                "channels": channels,
                "format": audio_path.suffix.lower(),
                "filename": audio_path.name,
            },
        )


if __name__ == "__main__":

    analyzer = MetadataAnalyzer()

    evidence = analyzer.analyze(
        Path("outputs/audio/demo_video.wav")
    )

    print(evidence)