from pathlib import Path

import textstat

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

        flesch_score = round(
            textstat.flesch_reading_ease(text),
            2,
        )

        grade_level = round(
            textstat.flesch_kincaid_grade(text),
            2,
        )

        gunning_fog = round(
            textstat.gunning_fog(text),
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