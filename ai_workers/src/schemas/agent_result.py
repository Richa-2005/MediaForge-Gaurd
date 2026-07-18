from dataclasses import dataclass
from typing import Any

from src.schemas.analysis_result import AnalysisResult


@dataclass
class AgentResult:
    """
    Final response returned by every AI agent.
    """

    upload_id: int
    agent: str
    analysis: AnalysisResult
    details: dict[str, Any] | None = None