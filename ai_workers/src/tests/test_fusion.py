from pathlib import Path

import pytest

from src.agents.analysis_agent import AnalysisAgent
from src.agents.fusion_agent import FusionAgent
from src.decision.fusion_decision_engine import FusionDecisionEngine
from src.schemas.agent_result import AgentResult
from src.schemas.analysis_result import AnalysisResult


def agent_result(agent: str, risk: float, confidence: float) -> AgentResult:
    return AgentResult(
        upload_id=1,
        agent=agent,
        analysis=AnalysisResult(
            label="uncertain",
            risk_score=risk,
            confidence=confidence,
            explanation=f"{agent} result",
            evidence=[],
        ),
    )


def test_fusion_combines_two_results():
    result = FusionAgent().analyze(
        [agent_result("text", 0.8, 0.9), agent_result("factcheck", 0.6, 0.7)],
        upload_id=1,
    )

    assert result.agent == "supervisor"
    assert result.analysis.label == "manipulated"
    assert result.analysis.risk_score == 0.7
    assert result.analysis.confidence == 0.8


def test_fusion_accepts_one_result():
    result = FusionAgent().analyze(
        [agent_result("text", 0.2, 0.8)],
        upload_id=1,
    )

    assert result.analysis.label == "authentic"


def test_fusion_agent_rejects_empty_result_list():
    with pytest.raises(ValueError, match="at least one"):
        FusionAgent().analyze([], upload_id=1)


@pytest.mark.parametrize(
    ("risk", "confidence", "expected"),
    [
        (0.6, 0.8, "manipulated"),
        (0.49, 0.2, "uncertain"),
        (0.5, 0.9, "uncertain"),
        (0.2, 0.8, "authentic"),
    ],
)
def test_fusion_thresholds(risk, confidence, expected):
    analysis = FusionDecisionEngine().evaluate(
        [agent_result("text", risk, confidence)]
    )

    assert analysis.label == expected


def test_fusion_failure_does_not_discard_specialist_results(tmp_path: Path):
    text_result = agent_result("text", 0.2, 0.8)
    factcheck_result = agent_result("factcheck", 0.3, 0.7)

    agent = AnalysisAgent.__new__(AnalysisAgent)
    agent.vision_agent = None
    agent.audio_agent = None
    agent.text_agent = MockAgent(text_result)
    agent.factcheck_agent = MockAgent(factcheck_result)
    agent.fusion_agent = FailingFusionAgent()

    text_path = tmp_path / "sample.txt"
    text_path.write_text("A meaningful claim.", encoding="utf-8")

    result = agent.analyze(1, text_path, "text")

    assert result["text"] is text_result
    assert result["factcheck"] is factcheck_result
    assert result["fusion"] is None


class MockAgent:
    def __init__(self, result):
        self.result = result

    def analyze(self, *_args, **_kwargs):
        return self.result


class FailingFusionAgent:
    def analyze(self, *_args, **_kwargs):
        raise RuntimeError("fusion unavailable")
