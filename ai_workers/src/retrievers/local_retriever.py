from src.retrievers.base_retriever import BaseRetriever
from src.schemas.retrieved_document import RetrievedDocument
from src.utils.text_normalizer import normalize_claim

class LocalRetriever(BaseRetriever):
    """
    Offline retriever used during development.

    Returns RetrievedDocument objects instead of making
    any authenticity decision.

    This simulates a local trusted knowledge base.
    """

    KNOWLEDGE_BASE = {

        "india has 28 states": {

            "title": "States and Union Territories of India",

            "content": (
                "India currently has 28 states "
                "and 8 union territories."
            ),

            "source": "Government of India",

            "url": None,

            "confidence": 0.99,

        },

        "earth is flat": {

            "title": "Shape of the Earth",

            "content": (
                "Scientific evidence shows that "
                "the Earth is an oblate spheroid."
            ),

            "source": "Scientific Consensus",

            "url": None,

            "confidence": 0.99,

        },

        "water boils at 100 degrees celsius": {

            "title": "Boiling Point of Water",

            "content": (
                "Pure water boils at approximately "
                "100°C at standard atmospheric pressure."
            ),

            "source": "Physics",

            "url": None,

            "confidence": 0.98,

        },

    }

    def retrieve(
        self,
        claim: str,
    ) -> list[RetrievedDocument]:

        key = normalize_claim(claim)

        fact = self.KNOWLEDGE_BASE.get(key)

        if fact is None:
            return []

        return [

            RetrievedDocument(

                source=fact["source"],

                title=fact["title"],

                content=fact["content"],

                url=fact["url"],

                confidence=fact["confidence"],

            )

        ]