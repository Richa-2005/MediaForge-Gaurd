from src.claim_extraction.claim_extractor import ClaimExtractor
from src.retrievers.retriever_manager import RetrieverManager
from src.verification.claim_verifier import ClaimVerifier
from src.schemas.evidence import Evidence


class FactCheckPipeline:
    """
    Executes the complete fact-check pipeline.

    Text
        ↓
    Claim Extraction
        ↓
    Retrieval
        ↓
    Claim Verification
        ↓
    Evidence[]
    """

    def __init__(self):

        self.extractor = ClaimExtractor()

        self.retriever = RetrieverManager()

        self.verifier = ClaimVerifier()

    def run(
        self,
        text: str,
    ) -> list[Evidence]:
        """
        Execute the complete fact-check workflow.
        """

        claims = self.extractor.extract(text)

        evidence = []

        for claim in claims:

            documents = self.retriever.retrieve(
                claim
            )

            result = self.verifier.verify(
                claim,
                documents,
            )

            evidence.append(result)

        return evidence


if __name__ == "__main__":

    pipeline = FactCheckPipeline()

    sample = """
    India has 28 states.
    Earth is flat.
    Water boils at 100 degrees Celsius.
    """

    evidence = pipeline.run(sample)

    for item in evidence:

        print(item)