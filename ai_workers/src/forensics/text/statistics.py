from pathlib import Path
import re

from src.schemas.evidence import Evidence


class TextStatisticsAnalyzer:
    """
    Computes basic statistics about a text document.
    """

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        text = text.strip()

        words = re.findall(r"\b\w+\b", text)
        sentences = re.split(r"[.!?]+", text)

        sentence_lengths = [
            len(re.findall(r"\b\w+\b", s))
            for s in sentences
            if s.strip()
        ]

        word_count = len(words)

        sentence_count = max(
            len(sentence_lengths),
            1,
        )

        avg_sentence_length = round(
            word_count / sentence_count,
            2,
        )

        uppercase_ratio = (
            sum(c.isupper() for c in text)
            / max(len(text), 1)
        )

        punctuation_ratio = (
            len(re.findall(r"[.,!?;:]", text))
            / max(len(text), 1)
        )

        confidence = 1.0

        return Evidence(
            method="Text Statistics",
            score=0.0,
            confidence=confidence,
            summary="Computed structural statistics for the text.",
            artifact_path=None,
            metadata={
                "word_count": word_count,
                "sentence_count": sentence_count,
                "average_sentence_length": avg_sentence_length,
                "uppercase_ratio": round(uppercase_ratio, 4),
                "punctuation_ratio": round(punctuation_ratio, 4),
            },
        )