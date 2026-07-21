from src.decision.fusion_decision_engine import (
    FusionDecisionEngine,
)
from src.schemas.agent_result import AgentResult


class FusionAgent:
    """
    Combines results produced by multiple specialist agents.
    """

    def __init__(self) -> None:
        self.decision_engine = FusionDecisionEngine()

    def analyze(
        self,
        results: list[AgentResult],
        upload_id: int,
    ) -> AgentResult:
        if not results:
            raise ValueError(
                "Fusion requires at least one agent result."
            )

        analysis = self.decision_engine.evaluate(results)

        return AgentResult(
            upload_id=upload_id,
            agent="supervisor",
            analysis=analysis,
            details={
                "source_agents": [
                    result.agent
                    for result in results
                ],
                "source_result_count": len(results),
            },
        )