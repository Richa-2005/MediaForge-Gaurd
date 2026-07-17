from pathlib import Path

from src.agents.audio_agent import AudioAgent
from src.agents.vision_agent import VisionAgent


class AnalysisAgent:
    """
    Master orchestrator for all AI workers.

    Routes uploaded media to the appropriate AI agents and
    aggregates their results.
    """

    def __init__(self):

        self.vision_agent = VisionAgent()

        self.audio_agent = AudioAgent()

    def analyze(
        self,
        upload_id: str,
        media_path: Path,
        media_type: str,
    ) -> dict:
        """
        Analyze uploaded media.

        Supported media types:
        - image
        - video
        - audio

        Returns
        -------
        dict
        """

        results = {
            "upload_id": upload_id,
            "vision": None,
            "audio": None,
        }

        media_type = media_type.lower()

        if media_type == "image":

            results["vision"] = self.vision_agent.analyze(
                media_path
            )

        elif media_type == "video":

            results["vision"] = self.vision_agent.analyze(
                media_path
            )

            results["audio"] = self.audio_agent.analyze(
                media_path
            )

        elif media_type == "audio":

            results["audio"] = self.audio_agent.analyze(
                media_path
            )

        else:

            raise ValueError(
                f"Unsupported media type: {media_type}"
            )

        return results