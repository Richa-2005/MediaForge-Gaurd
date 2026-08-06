from src.schemas import evidence
from src.schemas.analysis_result import AnalysisResult
from src.schemas.evidence import Evidence


class VisionDecisionEngine:
    """
    Aggregates vision forensic evidence into a final result.
    """

    WEIGHTS = {
        "ELA": 0.35,
        "Noise Analysis": 0.20,
        "FFT Analysis": 0.25,
        "Blur Analysis": 0.20,
    }

    def evaluate(
       self,
        prediction: dict,
        evidence: list[Evidence],
    ) -> AnalysisResult:

        label = prediction["label"]

        confidence = prediction["confidence"]

        risk_score = (
            confidence
            if label == "manipulated"
            else 1.0 - confidence
        )

        explanation = (
            f"MediaForge Vision classified this image as "
            f"{label} "
            f"with {confidence:.2%} confidence."
        )

        return AnalysisResult(

            label=label,

            risk_score=round(risk_score, 4),

            confidence=round(confidence, 4),

            explanation=explanation,

            evidence=evidence,
        )