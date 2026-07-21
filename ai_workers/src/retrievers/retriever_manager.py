from src.retrievers.local_retriever import LocalRetriever
from src.schemas.retrieved_document import RetrievedDocument


class RetrieverManager:
    """
    Coordinates multiple knowledge retrievers.

    Every retriever returns a list of RetrievedDocument objects.

    The manager aggregates all retrieved evidence into one list
    without making any verification decision.
    """

    def __init__(self):

        self.retrievers = [

            LocalRetriever(),

            # WikipediaRetriever(),
            # GoogleFactCheckRetriever(),
            # GovernmentRetriever(),
            # NewsRetriever(),

        ]

    def retrieve(
        self,
        claim: str,
    ) -> list[RetrievedDocument]:

        documents: list[RetrievedDocument] = []

        for retriever in self.retrievers:

            try:

                results = retriever.retrieve(claim)

                if results:

                    documents.extend(results)

            except Exception as e:

                print(
                    f"[RetrieverManager] "
                    f"{retriever.__class__.__name__} failed: {e}"
                )

        return documents