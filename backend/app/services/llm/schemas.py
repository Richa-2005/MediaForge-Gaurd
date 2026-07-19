from pydantic import BaseModel, Field


class Verdict(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)


class AnalysisSection(BaseModel):
    visual_analysis: str
    audio_analysis: str
    metadata_analysis: str


class ExplanationReport(BaseModel):
    title: str
    verdict: Verdict
    summary: str
    executive_summary: str
    analysis: AnalysisSection
    key_findings: list[str]
    limitations: str
    recommendation: str
    technical_notes: str