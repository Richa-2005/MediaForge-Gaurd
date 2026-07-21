from src.decision.factcheck_decision_engine import (
    FactCheckDecisionEngine,
)
from src.pipelines.factcheck_pipeline import (
    FactCheckPipeline,
)
from src.schemas.agent_result import AgentResult


class FactCheckAgent:
    """
    High-level entry point for fact-check analysis.

    Coordinates:
        - FactCheckPipeline
        - FactCheckDecisionEngine

    Returns:
        AgentResult
    """

    def __init__(self):

        self.pipeline = FactCheckPipeline()

        self.decision_engine = (
            FactCheckDecisionEngine()
        )

    def analyze(
        self,
        text: str,
        upload_id: int,
    ) -> AgentResult:

        evidence = self.pipeline.run(
            text
        )

        analysis = (
            self.decision_engine.evaluate(
                evidence
            )
        )

        return AgentResult(

            upload_id=upload_id,

            agent="factcheck",

            analysis=analysis,

            details={},

        )


if __name__ == "__main__":

    agent = FactCheckAgent()

    sample = """
    India has 28 states.

    Earth is flat.

    Water boils at
    100 degrees Celsius.
    """

    result = agent.analyze(
        sample,
        upload_id=1,
    )

    print(result)