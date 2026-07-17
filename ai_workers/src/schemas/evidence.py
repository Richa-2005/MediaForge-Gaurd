from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """
    Represents the output of a single forensic analyzer.
    """

    method: str = Field(
        ...,
        description="Name of the forensic analysis method.",
    )

    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalized forensic score.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in this evidence.",
    )

    summary: str = Field(
        ...,
        description="Human-readable explanation of the analysis.",
    )

    artifact_path: str | None = Field(
        default=None,
        description="Path to any generated visualization artifact.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Analyzer-specific metadata.",
    )