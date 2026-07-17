from pathlib import Path

from src.pipelines.vision_pipeline import VisionPipeline
from src.schemas.agent_result import AgentResult


class VisionAgent:
    """
    Performs explainable vision analysis using the VisionPipeline.
    """

    WEIGHTS = {
        "ELA": 0.35,
        "Noise Analysis": 0.20,
        "FFT Analysis": 0.25,
        "Blur Analysis": 0.20,
    }

    def __init__(self):
        self.pipeline = VisionPipeline()

    def analyze(
        self,
        upload_id: str,
        image_path: Path,
        output_dir: Path,
    ) -> AgentResult:

        pipeline_result = self.pipeline.run(
            image_path=image_path,
            output_dir=output_dir,
        )

        evidence = pipeline_result["forensics"]

        faces = pipeline_result["faces"]

        risk_score = 0.0

        for item in evidence:
            weight = self.WEIGHTS.get(
                item.method,
                0.0,
            )

            risk_score += item.score * weight

        risk_score = round(
            min(risk_score, 1.0),
            4,
        )

        confidence = round(
            sum(item.confidence for item in evidence)
            / len(evidence),
            4,
        )

        if risk_score >= 0.70:
            label = "manipulated"
        elif risk_score >= 0.45:
            label = "uncertain"
        else:
            label = "authentic"

        strongest = max(
            evidence,
            key=lambda e: e.score,
        )

        explanation = (
            f"{strongest.method} produced the strongest forensic signal "
            f"(score={strongest.score:.2f})."
        )

        return AgentResult(
            upload_id=upload_id,
            agent="vision",
            label=label,
            risk_score=risk_score,
            confidence=confidence,
            explanation=explanation,
            evidence=evidence,
            details={
                "face_count": faces["face_count"],
                "bounding_boxes": faces["bounding_boxes"],
                "saved_faces": faces["saved_faces"],
            },
        )


if __name__ == "__main__":

    agent = VisionAgent()

    result = agent.analyze(
        upload_id="demo_upload",
        image_path=Path("data/sample_images/sample_img.jpg"),
        output_dir=Path("outputs/vision_agent"),
    )

    print(result.model_dump_json(indent=2))