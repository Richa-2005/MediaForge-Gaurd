from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    """
    Base class for all evidence retrievers.
    """

    @abstractmethod
    def retrieve(
        self,
        claim: str,
    ) -> dict:
        """
        Retrieve evidence for a claim.

        Returns a dictionary containing retrieved evidence.
        """
        pass
    