from src.schemas.agent_result import AgentResult
from src.schemas.analysis_result import AnalysisResult


class FusionDecisionEngine:
    """
    Combines results from multiple AI agents into a single decision.
    """

    def evaluate(
        self,
        vision: AgentResult | None,
        audio: AgentResult | None,
    ) -> AnalysisResult:

        available = [
            result.analysis
            for result in [vision, audio]
            if result is not None
        ]

        if not available:
            return AnalysisResult(
                label="unknown",
                risk_score=0.0,
                confidence=0.0,
                explanation="No analysis available.",
                evidence=[],
            )

        risk_score = sum(
            item.risk_score
            for item in available
        ) / len(available)

        confidence = sum(
            item.confidence
            for item in available
        ) / len(available)

        label = (
            "fake"
            if risk_score >= 0.5
            else "real"
        )

        explanation = (
            f"Combined analysis from {len(available)} AI workers."
        )

        evidence = []

        for item in available:
            evidence.extend(item.evidence)

        return AnalysisResult(
            label=label,
            risk_score=round(risk_score, 4),
            confidence=round(confidence, 4),
            explanation=explanation,
            evidence=evidence,
        )