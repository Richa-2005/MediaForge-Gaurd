
from dataclasses import dataclass, field
from typing import Any

from src.schemas.evidence import Evidence


@dataclass
class AgentResult:
    """
    Output returned by every AI agent.
    """

    upload_id: str

    agent: str

    label: str

    risk_score: float

    confidence: float

    explanation: str

    evidence: list[Evidence]

    details: dict[str, Any] = field(default_factory=dict)