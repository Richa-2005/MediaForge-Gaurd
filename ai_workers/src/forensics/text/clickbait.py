import re
from pathlib import Path

from src.schemas.evidence import Evidence


class ClickbaitAnalyzer:
    """
    Detects common clickbait headline patterns.
    """

    PATTERNS = [

        r"you won't believe",

        r"what happened next",

        r"this will shock you",

        r"number\s+\d+",

        r"top\s+\d+",

        r"one simple trick",

        r"doctors hate",

        r"the truth about",

        r"they don't want you to know",

        r"find out why",

        r"before it's too late",

        r"gone wrong",

        r"this changes everything",

        r"must watch",

        r"must read",

        r"can you guess",

        r"everyone is talking about",

        r"what happens if",

        r"you need to know",

        r"revealed",

    ]

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        lower = text.lower()

        matches = []

        for pattern in self.PATTERNS:

            if re.search(pattern, lower):

                matches.append(pattern)

        score = min(

            len(matches) * 0.30,

            1.0,

        )

        confidence = min(

            0.70 + score * 0.30,

            1.0,

        )

        return Evidence(

            method="Clickbait Detection",

            score=round(score, 4),

            confidence=round(confidence, 4),

            summary="Detected clickbait headline patterns.",

            artifact_path=None,

            metadata={

                "matched_patterns": matches,

                "pattern_count": len(matches),

            },

        )
    