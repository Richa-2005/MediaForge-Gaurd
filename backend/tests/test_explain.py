from types import SimpleNamespace
from unittest.mock import Mock

from app.services.llm.nodes import explain as explain_node
from app.services.llm.schemas import (
    AgentAnalysisSection,
    ExplanationReport,
    Verdict,
)


def test_explain_preserves_primary_verdict(monkeypatch):
    generated = ExplanationReport(
        title="MediaForge Guard Authenticity Report",
        verdict=Verdict(label="wrong", confidence=0.1),
        summary="A cautious summary.",
        executive_summary="A cautious explanation.",
        agent_analyses=[
            AgentAnalysisSection(
                agent="text",
                title="Text",
                analysis="Supplied analysis.",
                key_observations=[],
            )
        ],
        key_findings=["A supplied finding."],
        limitations="Automated result.",
        recommendation="Verify independently.",
        technical_notes="Supervisor is primary.",
    )
    structured = Mock()
    structured.invoke.return_value = generated
    model = Mock()
    model.with_structured_output.return_value = structured
    monkeypatch.setattr(explain_node, "get_chat_model", lambda: model)

    state = {
        "formatted_context": "Agent: text",
        "primary_analysis": SimpleNamespace(
            label=SimpleNamespace(value="uncertain"),
            confidence=0.42,
        ),
    }

    result = explain_node.explain(state)

    assert result["report"].verdict.label == "uncertain"
    assert result["report"].verdict.confidence == 0.42
