from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from src.schemas.evidence import Evidence
from src.schemas.retrieved_document import RetrievedDocument


class ClaimVerificationEngine:
    """
    Verifies factual claims using semantic similarity.

    Retrieval and verification are intentionally separated.
    """

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def verify(
        self,
        claim: str,
        documents: list[RetrievedDocument],
    ) -> Evidence:

        if not documents:

            return Evidence(

                method="Fact Verification",

                score=0.5,

                confidence=0.0,

                summary="No supporting documents found.",

                artifact_path=None,

                metadata={

                    "claim": claim,

                    "verdict": "unknown",

                    "sources": [],

                },

            )

        claim_embedding = self.model.encode(
            claim,
            convert_to_tensor=True,
        )

        best_document = None

        best_similarity = -1.0

        for document in documents:

            document_embedding = self.model.encode(

                document.content,

                convert_to_tensor=True,

            )

            similarity = float(

                cos_sim(
                    claim_embedding,
                    document_embedding,
                )

            )

            if similarity > best_similarity:

                best_similarity = similarity

                best_document = document

        if best_similarity >= 0.80:

            verdict = "supported"

            score = 0.0

        elif best_similarity >= 0.60:

            verdict = "unknown"

            score = 0.5

        else:

            verdict = "contradicted"

            score = 1.0

        return Evidence(

            method="Fact Verification",

            score=score,

            confidence=round(best_similarity, 4),

            summary=f"Claim is {verdict}.",

            artifact_path=None,

            metadata={

                "claim": claim,

                "verdict": verdict,

                "similarity": round(
                    best_similarity,
                    4,
                ),

                "sources": [

                    {

                        "title": best_document.title,

                        "source": best_document.source,

                        "url": best_document.url,

                    }

                ],

            },

        )