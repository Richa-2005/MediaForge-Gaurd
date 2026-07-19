from app.services.llm.nodes.format_markdown import format_markdown
from app.services.llm.schemas import (
    ExplanationReport,
    Verdict,
    AnalysisSection,
)

state = {
    "report": ExplanationReport(
        title="Media Authenticity Report",
        summary="Likely authentic.",
        verdict=Verdict(
            label="Authentic",
            confidence="High",
        ),
        executive_summary="No manipulation indicators were detected.",
        analysis=AnalysisSection(
            visual_analysis="No anomalies.",
            audio_analysis="Not applicable.",
            metadata_analysis="Metadata consistent.",
        ),
        key_findings=[
            "Metadata is intact.",
            "No visual inconsistencies.",
            "High confidence prediction.",
        ],
        limitations="Automated analysis has limitations.",
        recommendation="Verify with the original source.",
        technical_notes="Confidence reflects model certainty.",
    )
}

print("=" * 60)
print("Testing Markdown Formatter")
print("=" * 60)

state = format_markdown(state)

print(state["report_markdown"])