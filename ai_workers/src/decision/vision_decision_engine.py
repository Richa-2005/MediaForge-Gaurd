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
        evidence: list[Evidence],
    ) -> AnalysisResult:

        if not evidence:
            return AnalysisResult(
                label="unknown",
                risk_score=0.0,
                confidence=0.0,
                explanation="No visual evidence available.",
                evidence=[],
            )

        weighted_score = 0.0
        total_weight = 0.0

        for item in evidence:

            weight = self.WEIGHTS.get(
                item.method,
                0.0,
            )

            weighted_score += item.score * weight
            total_weight += weight

        risk_score = (
            weighted_score / total_weight
            if total_weight > 0
            else 0.0
        )

        confidence = sum(
            item.confidence
            for item in evidence
        ) / len(evidence)

        # ---------- Standardized labels ----------

        if risk_score >= 0.50:
            label = "fake"
        else:
            label = "real"

        strongest = max(
            evidence,
            key=lambda item: item.score,
        )

        explanation = (
            f"{strongest.method} detected the strongest "
            f"forensic signal "
            f"(score={strongest.score:.2f})."
        )

        return AnalysisResult(
            label=label,
            risk_score=round(risk_score, 4),
            confidence=round(confidence, 4),
            explanation=explanation,
            evidence=evidence,
        )