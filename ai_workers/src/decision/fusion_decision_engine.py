from src.schemas.agent_result import AgentResult
from src.schemas.analysis_result import AnalysisResult


class FusionDecisionEngine:
    """
    Combines results from multiple AI agents into a single decision.
    """

    def evaluate(
        self,
        results: list[AgentResult],
    ) -> AnalysisResult:

        available = [
            result.analysis
            for result in results
            if result is not None
        ]

        if not available:
            return AnalysisResult(
                label="uncertain",
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

        # Low-confidence or borderline evidence is inconclusive rather
        # than evidence of authenticity.
        if confidence < 0.5 or 0.4 < risk_score < 0.6:
            label = "uncertain"
        elif risk_score >= 0.6:
            label = "manipulated"
        else:
            label = "authentic"

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
