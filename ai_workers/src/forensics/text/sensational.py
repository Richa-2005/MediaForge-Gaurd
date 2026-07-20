import re
from pathlib import Path

from src.schemas.evidence import Evidence


class SensationalLanguageAnalyzer:
    """
    Detects sensational and emotionally manipulative language.
    """

    KEYWORDS = {

        "breaking",

        "shocking",

        "urgent",

        "exclusive",

        "viral",

        "must read",

        "secret",

        "don't miss",

        "wake up",

        "before it's deleted",

        "they don't want you to know",

        "unbelievable",

        "warning",

        "alert",

        "exposed",

        "truth revealed",
    }

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        lower = text.lower()

        matches = []

        for keyword in self.KEYWORDS:

            if keyword in lower:

                matches.append(keyword)

        exclamation_count = text.count("!")

        uppercase_words = len(

            re.findall(
                r"\b[A-Z]{3,}\b",
                text,
            )

        )

        raw_score = (

            len(matches) * 0.45

            + exclamation_count * 0.05

            + uppercase_words * 0.08

        )

        score = min(raw_score, 1.0)

        confidence = min(

            0.6 + score * 0.4,

            1.0,

        )

        return Evidence(

            method="Sensational Language",

            score=round(score, 4),

            confidence=round(confidence, 4),

            summary="Detected emotionally manipulative language.",

            artifact_path=None,

            metadata={

                "matched_keywords": matches,

                "keyword_count": len(matches),

                "exclamation_marks": exclamation_count,

                "uppercase_words": uppercase_words,

            },

        )