from pathlib import Path

from src.schemas.evidence import Evidence
from src.utils.spacy_model import load_english_pipeline


class ClaimExtractor:
    """
    Extracts factual-looking claims from text.
    """

    def __init__(self):

        self.nlp = load_english_pipeline()

    def is_claim(self, sentence):

        has_subject = False

        has_verb = False

        for token in sentence:

            if token.dep_ in (
                "nsubj",
                "nsubjpass",
            ):
                has_subject = True

            if token.pos_ == "VERB":
                has_verb = True

        return (
            has_subject
            and has_verb
        )

    def analyze(
        self,
        text: str,
        artifact_path=None,
    ) -> Evidence:

        doc = self.nlp(text)

        claims = []

        for sentence in doc.sents:

            sentence = sentence.as_doc()

            if self.is_claim(sentence):

                claims.append(
                    sentence.text.strip()
                )

        return Evidence(
            method="Claim Extraction",
            score=0.0,
            confidence=1.0,
            summary="Extracted factual claims from text.",
            artifact_path=None,
            metadata={
                "claim_count": len(claims),
                "claims": claims,
            },
        )
