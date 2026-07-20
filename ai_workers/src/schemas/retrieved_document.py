from dataclasses import dataclass


@dataclass
class RetrievedDocument:
    """
    A document returned by a retriever.

    This schema is intentionally generic so that
    Wikipedia, Google Fact Check, government APIs,
    or vector databases can all return the same type.
    """

    source: str

    title: str

    content: str

    url: str | None = None

    confidence: float = 1.0