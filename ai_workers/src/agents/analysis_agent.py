from pathlib import Path

from src.agents.audio_agent import AudioAgent
from src.agents.vision_agent import VisionAgent


class AnalysisAgent:
    """
    Master orchestrator for all AI workers.

    Routes uploaded media to the appropriate AI agents and
    aggregates their results.
    """

    def __init__(self) -> None:
        self.vision_agent = VisionAgent()
        self.audio_agent = AudioAgent()

    def analyze(
        self,
        upload_id: int,
        media_path: Path,
        media_type: str,
    ) -> dict:
        """
        Analyze uploaded media.

        Supported media types:
        - image
        - video
        - audio
        """

        results = {
            "upload_id": upload_id,
            "vision": None,
            "audio": None,
        }

        normalized_media_type = media_type.lower()

        if normalized_media_type == "image":
            results["vision"] = self.vision_agent.analyze(
                media_path,
                upload_id=upload_id,
            )

        elif normalized_media_type == "video":
            raise NotImplementedError(
                "Video analysis is not ready yet. "
                "The vision pipeline requires extracted image frames, "
                "not the raw video file."
            )

        elif normalized_media_type == "audio":
            results["audio"] = self.audio_agent.analyze(
                media_path,
                upload_id=upload_id,
            )

        else:
            raise ValueError(
                f"Unsupported media type: {normalized_media_type}"
            )

        return results