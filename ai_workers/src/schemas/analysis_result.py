from dataclasses import dataclass

from src.schemas.evidence import Evidence


@dataclass
class AnalysisResult:
    """
    Final decision produced by an AI decision engine.
    """

    label: str

    risk_score: float

    confidence: float

    explanation: str

    evidence: list[Evidence]