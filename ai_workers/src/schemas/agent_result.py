from typing import Any

from pydantic import BaseModel, Field

from src.schemas.evidence import Evidence


class AgentResult(BaseModel):
    """
    Standard output returned by every AI agent.
    """

    upload_id: str = Field(
        ...,
        description="Upload identifier supplied by the backend.",
    )

    agent: str = Field(
        ...,
        description="Agent name (vision, audio, text, video).",
    )

    label: str = Field(
        ...,
        description="Predicted label.",
    )

    risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability that the content is manipulated or misleading.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the predicted label.",
    )

    explanation: str = Field(
        ...,
        description="Human-readable explanation of the decision.",
    )

    evidence: list[Evidence] = Field(
        default_factory=list,
        description="Evidence collected during analysis.",
    )

    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional agent-specific information.",
    )