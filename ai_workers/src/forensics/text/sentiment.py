from pathlib import Path

from nltk.sentiment import SentimentIntensityAnalyzer

from src.schemas.evidence import Evidence


class SentimentAnalyzer:
    """
    Computes sentiment polarity using VADER.
    """

    def __init__(self):

        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        scores = self.analyzer.polarity_scores(text)

        compound = scores["compound"]

        if compound >= 0.05:
            label = "positive"

        elif compound <= -0.05:
            label = "negative"

        else:
            label = "neutral"

        # Higher emotional intensity = higher heuristic score
        risk_score = abs(compound)

        return Evidence(
            method="Sentiment Analysis",
            score=round(risk_score, 4),
            confidence=1.0,
            summary="Analyzed emotional tone using VADER.",
            artifact_path=None,
            metadata={
                "label": label,
                "compound": round(compound, 4),
                "positive": scores["pos"],
                "neutral": scores["neu"],
                "negative": scores["neg"],
            },
        )