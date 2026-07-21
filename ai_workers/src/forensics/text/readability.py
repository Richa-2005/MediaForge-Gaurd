from pathlib import Path
import re

from src.schemas.evidence import Evidence


class ReadabilityAnalyzer:
    """
    Computes readability metrics for the input text.
    """

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        if not text.strip():

            return Evidence(
                method="Readability Analysis",
                score=0.0,
                confidence=0.0,
                summary="No readable text provided.",
                artifact_path=None,
                metadata={},
            )

        words = re.findall(r"[A-Za-z]+", text)
        sentence_count = max(1, len(re.findall(r"[.!?]+", text)))
        word_count = max(1, len(words))
        syllable_counts = [count_syllables(word) for word in words]
        syllable_count = max(1, sum(syllable_counts))
        complex_words = sum(count >= 3 for count in syllable_counts)

        words_per_sentence = word_count / sentence_count
        syllables_per_word = syllable_count / word_count
        flesch_score = round(
            206.835
            - 1.015 * words_per_sentence
            - 84.6 * syllables_per_word,
            2,
        )
        grade_level = round(
            0.39 * words_per_sentence
            + 11.8 * syllables_per_word
            - 15.59,
            2,
        )
        gunning_fog = round(
            0.4
            * (
                words_per_sentence
                + 100 * complex_words / word_count
            ),
            2,
        )

        confidence = 1.0

        return Evidence(
            method="Readability Analysis",
            score=0.0,
            confidence=confidence,
            summary="Computed readability metrics.",
            artifact_path=None,
            metadata={
                "flesch_reading_ease": flesch_score,
                "flesch_kincaid_grade": grade_level,
                "gunning_fog_index": gunning_fog,
            },
        )


def count_syllables(word: str) -> int:
    """Estimate English syllables without external data downloads."""
    normalized = word.lower()
    groups = len(re.findall(r"[aeiouy]+", normalized))
    if normalized.endswith("e") and groups > 1:
        groups -= 1
    return max(1, groups)
