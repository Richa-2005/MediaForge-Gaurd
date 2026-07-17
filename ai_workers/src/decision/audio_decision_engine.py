from src.schemas.analysis_result import AnalysisResult
from src.schemas.evidence import Evidence


class AudioDecisionEngine:
    """
    Aggregates audio forensic evidence into a final result.
    """

    def evaluate(
        self,
        evidence: list[Evidence],
    ) -> AnalysisResult:

        if not evidence:
            return AnalysisResult(
                label="unknown",
                risk_score=0.0,
                confidence=0.0,
                explanation="No audio evidence available.",
                evidence=[],
            )

        risk_score = sum(
            item.score
            for item in evidence
        ) / len(evidence)

        confidence = sum(
            item.confidence
            for item in evidence
        ) / len(evidence)

        label = "fake" if risk_score >= 0.5 else "real"

        return AnalysisResult(
            label=label,
            risk_score=round(risk_score, 4),
            confidence=round(confidence, 4),
            explanation="Audio forensic analysis completed.",
            evidence=evidence,
        )