from pathlib import Path

from src.config import AUDIO_OUTPUT_DIR
from src.decision.audio_decision_engine import AudioDecisionEngine
from src.pipelines.audio_pipeline import AudioPipeline
from src.schemas.agent_result import AgentResult


class AudioAgent:
    """
    High-level entry point for audio analysis.
    """

    def __init__(self):
        self.pipeline = AudioPipeline()
        self.decision_engine = AudioDecisionEngine()

    def analyze(
        self,
        media_path: Path,
        upload_id: int,
    ) -> AgentResult:

        evidence = self.pipeline.run(
            media_path,
            AUDIO_OUTPUT_DIR,
        )

        analysis = self.decision_engine.evaluate(
            evidence
        )

        return AgentResult(
            upload_id=upload_id,
            agent="audio",
            analysis=analysis,
            details={},
        )
