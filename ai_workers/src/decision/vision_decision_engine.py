from src.schemas.agent_result import AgentResult
from src.schemas.evidence import Evidence


class VisionDecisionEngine:
    """
    Combines forensic evidence into one final decision.
    """

    WEIGHTS = {
        "ELA": 0.35,
        "Noise Analysis": 0.20,
        "FFT Analysis": 0.25,
        "Blur Analysis": 0.20,
    }

    def evaluate(
        self,
        upload_id: str,
        evidence: list[Evidence],
        face_data: dict,
    ) -> AgentResult:

        weighted_score = 0.0

        for item in evidence:
            weighted_score += (
                item.score *
                self.WEIGHTS.get(item.method, 0.0)
            )

        risk_score = round(
            min(weighted_score, 1.0),
            4,
        )

        confidence = round(
            sum(e.confidence for e in evidence) /
            len(evidence),
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
            f"{strongest.method} produced the strongest forensic "
            f"signal (score={strongest.score:.2f})."
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
                "face_count": face_data["face_count"],
                "bounding_boxes": face_data["bounding_boxes"],
                "saved_faces": face_data["saved_faces"],
            },
        )