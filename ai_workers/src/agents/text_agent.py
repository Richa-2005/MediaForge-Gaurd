from src.decision.text_decision_engine import TextDecisionEngine
from src.pipelines.text_pipeline import TextPipeline
from src.schemas.agent_result import AgentResult


class TextAgent:
    """
    High-level entry point for text analysis.
    """

    def __init__(self):

        self.pipeline = TextPipeline()

        self.decision_engine = TextDecisionEngine()

    def analyze(
        self,
        text: str,
        upload_id: str = "text",
    ) -> AgentResult:

        evidence = self.pipeline.run(text)

        analysis = self.decision_engine.evaluate(
            evidence
        )

        return AgentResult(

            upload_id=upload_id,

            agent="text",

            analysis=analysis,

            details={

                "character_count": len(text),

                "word_count": len(text.split()),

            },

        )


if __name__ == "__main__":

    sample = """
    BREAKING!!

    Doctors don't want you to know this.

    WHO approved a new vaccine.

    Read before it's deleted.

    """

    agent = TextAgent()

    result = agent.analyze(sample)

    print(result)