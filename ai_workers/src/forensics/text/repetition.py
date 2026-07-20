import re
from collections import Counter
from pathlib import Path

from src.schemas.evidence import Evidence


class RepetitionAnalyzer:
    """
    Detects repeated words and repeated sentences.
    """

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        # ---------- Words ----------

        words = re.findall(
            r"\b\w+\b",
            text.lower(),
        )

        word_counter = Counter(words)

        repeated_words = {

            word: count

            for word, count in word_counter.items()

            if count >= 3

        }

        # ---------- Sentences ----------

        sentences = [

            sentence.strip()

            for sentence in re.split(
                r"[.!?]",
                text
            )

            if sentence.strip()

        ]

        sentence_counter = Counter(sentences)

        repeated_sentences = {

            sentence: count

            for sentence, count in sentence_counter.items()

            if count >= 2

        }

        # ---------- Score ----------

        word_score = min(

            len(repeated_words) * 0.10,

            0.50,

        )

        sentence_score = min(

            len(repeated_sentences) * 0.50,

            0.50,

        )

        score = min(

            word_score + sentence_score,

            1.0,

        )

        confidence = min(

            0.70 + score * 0.30,

            1.0,

        )

        return Evidence(

            method="Repetition Analysis",

            score=round(score, 4),

            confidence=round(confidence, 4),

            summary="Detected repeated words and repeated sentences.",

            artifact_path=None,

            metadata={

                "repeated_words": repeated_words,

                "repeated_sentences": repeated_sentences,

                "word_repetition_count": len(repeated_words),

                "sentence_repetition_count": len(repeated_sentences),

            },

        )