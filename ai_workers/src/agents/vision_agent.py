from pathlib import Path

from src.config import PROCESSED_IMAGE_DIR
from src.decision.vision_decision_engine import VisionDecisionEngine
from src.pipelines.vision_pipeline import VisionPipeline
from src.schemas.agent_result import AgentResult


class VisionAgent:
    """
    High-level entry point for vision analysis.
    """

    def __init__(self):

        self.pipeline = VisionPipeline()

        self.decision_engine = VisionDecisionEngine()

    def analyze(
        self,
        image_path: Path,
        upload_id: int,
) -> AgentResult:

        evidence, face_data = self.pipeline.run(
            image_path,
            PROCESSED_IMAGE_DIR,
        )

        analysis = self.decision_engine.evaluate(
            evidence
        )

        return AgentResult(
            upload_id=upload_id,
            agent="vision",
            analysis=analysis,
            details={
                "faces": face_data,
            },
        )


if __name__ == "__main__":

    from src.config import DATA_DIR

    agent = VisionAgent()

    result = agent.analyze(
        DATA_DIR
        / "sample_images"
        / "sample_img.jpg",
        upload_id=1,
    )

    print(result)