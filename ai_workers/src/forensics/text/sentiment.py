from pathlib import Path

from nltk.sentiment import SentimentIntensityAnalyzer

from src.schemas.evidence import Evidence


class SentimentAnalyzer:
    """
    Computes sentiment polarity using VADER.
    """

    def __init__(self):
        try:
            self.analyzer = SentimentIntensityAnalyzer()
        except LookupError:
            self.analyzer = None

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        if self.analyzer is not None:
            scores = self.analyzer.polarity_scores(text)
            confidence = 1.0
        else:
            scores = fallback_sentiment_scores(text)
            confidence = 0.5

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
            confidence=confidence,
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


def fallback_sentiment_scores(text: str) -> dict[str, float]:
    positive_words = {
        "accurate", "authentic", "excellent", "good", "safe", "true"
    }
    negative_words = {
        "bad", "danger", "fake", "fraud", "harmful", "lie", "scam"
    }
    words = [word.strip(".,!?;:").lower() for word in text.split()]
    positive = sum(word in positive_words for word in words)
    negative = sum(word in negative_words for word in words)
    total = max(1, len(words))
    compound = (positive - negative) / max(1, positive + negative)
    return {
        "neg": negative / total,
        "neu": max(0.0, 1.0 - (positive + negative) / total),
        "pos": positive / total,
        "compound": compound,
    }
