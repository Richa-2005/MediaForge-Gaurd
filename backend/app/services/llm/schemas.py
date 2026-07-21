from pydantic import BaseModel, Field


class Verdict(BaseModel):
    label: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class AgentAnalysisSection(BaseModel):
    agent: str
    title: str
    analysis: str
    key_observations: list[str]


class ExplanationReport(BaseModel):
    title: str
    verdict: Verdict
    summary: str
    executive_summary: str
    agent_analyses: list[AgentAnalysisSection]
    key_findings: list[str]
    limitations: str
    recommendation: str
    technical_notes: str