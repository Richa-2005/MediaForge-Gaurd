from src.schemas.analysis_result import AnalysisResult
from src.schemas.evidence import Evidence


class FactCheckDecisionEngine:
    """
    Aggregates multiple claim verification results
    into a single AnalysisResult.

    Unlike ClaimVerifier, this engine does NOT inspect
    claims directly. It only evaluates the Evidence
    objects returned by the verifier.
    """

    def evaluate(
        self,
        evidence: list[Evidence],
    ) -> AnalysisResult:

        if not evidence:

            return AnalysisResult(

                label = "uncertain",

                risk_score=0.5,

                confidence=0.0,

                explanation="No factual claims were detected.",

                evidence=[],

            )

        risk_score = (

            sum(
                item.score
                for item in evidence
            )

            / len(evidence)

        )

        confidence = (

            sum(
                item.confidence
                for item in evidence
            )

            / len(evidence)

        )

        supported = sum(

            item.metadata.get("verdict") == "supported"

            for item in evidence

        )

        contradicted = sum(

            item.metadata.get("verdict") == "contradicted"

            for item in evidence

        )

        unknown = sum(

            item.metadata.get("verdict") == "unknown"

            for item in evidence

        )

        if contradicted > supported:

            label = "manipulated"

        elif supported > contradicted:

            label = "authentic"

        else:

            label = "uncertain"

        explanation = (

            f"{supported} supported, "

            f"{contradicted} contradicted, "

            f"{unknown} unknown claim(s)."

        )

        return AnalysisResult(

            label=label,

            risk_score=round(
                risk_score,
                4,
            ),

            confidence=round(
                confidence,
                4,
            ),

            explanation=explanation,

            evidence=evidence,

        )