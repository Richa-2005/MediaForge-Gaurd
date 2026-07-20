import re


def normalize_claim(text: str) -> str:
    """
    Normalize text for consistent fact retrieval.

    Performs:
    - lowercase conversion
    - punctuation removal
    - whitespace normalization
    """

    text = text.lower().strip()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Normalize whitespace
    text = " ".join(text.split())

    return text