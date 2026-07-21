from app.services.llm.nodes.format_markdown import format_markdown
from app.services.llm.schemas import (
    AgentAnalysisSection,
    ExplanationReport,
    Verdict,
)


def test_format_markdown_supports_agent_independent_report():
    state = {
        "report": ExplanationReport(
            title="MediaForge Guard Authenticity Report",
            summary="The upload is likely authentic.",
            verdict=Verdict(label="authentic", confidence=0.9),
            executive_summary="No supplied result identified manipulation.",
            agent_analyses=[
                AgentAnalysisSection(
                    agent="text",
                    title="Text Analysis",
                    analysis="No strong manipulation signal was found.",
                    key_observations=["Language indicators were low risk."],
                )
            ],
            key_findings=["The text result was low risk."],
            limitations="Automated analysis may be wrong.",
            recommendation="Verify the original source.",
            technical_notes="The supervisor result is primary.",
        )
    }

    result = format_markdown(state)

    assert "## Agent Analysis" in result["report_markdown"]
    assert "### Text Analysis" in result["report_markdown"]
    assert "90.00% (High)" in result["report_markdown"]
