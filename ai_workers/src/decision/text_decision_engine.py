from src.schemas.analysis_result import AnalysisResult
from src.schemas.evidence import Evidence


class TextDecisionEngine:
    """
    Aggregates text forensic evidence into one AnalysisResult.
    """

    WEIGHTS = {

        "Sentiment": 0.15,

        "Sensational Language": 0.30,

        "Clickbait Detection": 0.30,

        "Repetition Analysis": 0.25,

    }

    def evaluate(
        self,
        evidence: list[Evidence],
    ) -> AnalysisResult:

        # ----------------------------
        # Empty pipeline
        # ----------------------------

        if not evidence:

            return AnalysisResult(

                label="unknown",

                risk_score=0.0,

                confidence=0.0,

                explanation="No text evidence available.",

                evidence=[],

            )

        # ----------------------------
        # Weighted aggregation
        # ----------------------------

        weighted_score = 0.0

        total_weight = 0.0

        confidences = []

        for item in evidence:

            confidences.append(item.confidence)

            weight = self.WEIGHTS.get(

                item.method,

                0.0,

            )

            weighted_score += (

                item.score * weight

            )

            total_weight += weight

        risk_score = (

            weighted_score / total_weight

            if total_weight > 0

            else 0.0

        )

        confidence = (

            sum(confidences)

            / len(confidences)

        )

        # ----------------------------
        # Label
        # ----------------------------

        if risk_score >= 0.65:

            label = "fake"

        elif risk_score >= 0.35:

            label = "unknown"

        else:

            label = "real"

        # ----------------------------
        # Strongest signal
        # ----------------------------

        scored = [

            e

            for e in evidence

            if e.method in self.WEIGHTS

        ]

        if scored:

            strongest = max(

                scored,

                key=lambda e: e.score,

            )

            explanation = (

                f"{strongest.method} "

                "contributed the strongest "

                "misinformation signal."

            )

        else:

            explanation = (

                "No heuristic risk signals detected."

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