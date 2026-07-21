from pathlib import Path

import logging

logger = logging.getLogger(__name__)

class AnalysisAgent:
    """
    Master orchestrator for all AI workers.

    Routes uploaded media to the appropriate AI agents and
    aggregates their results.
    """

    def __init__(self) -> None:
        # Agent construction can load large media/NLP dependencies. Keep
        # it route-specific so, for example, image analysis never tries
        # to initialize the fact-check model.
        self.vision_agent = None
        self.audio_agent = None
        self.text_agent = None
        self.factcheck_agent = None
        self.fusion_agent = None

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
        - text
        """

        results = {
            "upload_id": upload_id,
            "vision": None,
            "audio": None,
            "text": None,
            "factcheck": None,
            "fusion": None,
        }

        normalized_media_type = media_type.strip().lower()

        if normalized_media_type == "image":
            from src.agents.vision_agent import VisionAgent

            self.vision_agent = self.vision_agent or VisionAgent()
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
            from src.agents.audio_agent import AudioAgent

            self.audio_agent = self.audio_agent or AudioAgent()
            results["audio"] = self.audio_agent.analyze(
                media_path,
                upload_id=upload_id,
            )

        elif normalized_media_type == "text":
            from src.agents.factcheck_agent import FactCheckAgent
            from src.agents.fusion_agent import FusionAgent
            from src.agents.text_agent import TextAgent

            try:
                text_content = media_path.read_text(
                    encoding="utf-8"
                )
            except UnicodeDecodeError as exc:
                raise ValueError(
                    f"Text file is not valid UTF-8: {media_path}"
                ) from exc

            text_content = text_content.strip()

            if not text_content:
                raise ValueError(
                    f"Text file is empty: {media_path}"
                )

            self.text_agent = self.text_agent or TextAgent()
            self.factcheck_agent = (
                self.factcheck_agent or FactCheckAgent()
            )
            self.fusion_agent = self.fusion_agent or FusionAgent()

            text_result = self.text_agent.analyze(
                text_content,
                upload_id=upload_id,
            )

            factcheck_result = (
                self.factcheck_agent.analyze(
                    text_content,
                    upload_id=upload_id,
                )
            )

            results["text"] = text_result
            results["factcheck"] = factcheck_result

            try:
                results["fusion"] = self.fusion_agent.analyze(
                    results=[
                        text_result,
                        factcheck_result,
                    ],
                    upload_id=upload_id,
                )
            except Exception:
                # Specialist results remain useful if fusion fails.
                logger.exception(
                    "Fusion failed | upload_id=%s",
                    upload_id,
                )

        else:
            raise ValueError(
                f"Unsupported media type: {normalized_media_type}"
            )

        return results
