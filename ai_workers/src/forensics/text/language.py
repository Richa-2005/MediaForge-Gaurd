from pathlib import Path

from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException

from src.schemas.evidence import Evidence


class LanguageAnalyzer:
    """
    Detects the primary language of a text.
    """

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        try:

            language = detect(text)

            probabilities = detect_langs(text)

            confidence = round(
                probabilities[0].prob,
                4,
            )

        except LangDetectException:

            language = "unknown"

            confidence = 0.0

        return Evidence(
            method="Language Detection",
            score=0.0,
            confidence=confidence,
            summary="Detected the primary language of the text.",
            artifact_path=None,
            metadata={
                "language": language,
                "confidence": confidence,
            },
        )