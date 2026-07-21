from dataclasses import dataclass

from src.schemas.evidence import Evidence


from typing import Literal

Label = Literal[
    "authentic",
    "manipulated",
    "uncertain",
]

@dataclass
class AnalysisResult:
    label: Label
    risk_score: float
    confidence: float
    explanation: str
    evidence: list[Evidence]