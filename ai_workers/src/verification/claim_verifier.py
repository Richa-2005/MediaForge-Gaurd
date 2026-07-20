from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

import torch

from src.schemas.evidence import Evidence
from src.schemas.retrieved_document import RetrievedDocument


class ClaimVerifier:
    """
    Verifies claims using Natural Language Inference.

    Premise:
        Retrieved document

    Hypothesis:
        User claim
    """

    MODEL_NAME = (
        "MoritzLaurer/"
        "DeBERTa-v3-base-mnli-fever-anli"
    )

    def __init__(self):

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                self.MODEL_NAME
            )
        )

        self.id2label = self.model.config.id2label

    def predict(
        self,
        premise: str,
        hypothesis: str,
    ):

        inputs = self.tokenizer(

            premise,

            hypothesis,

            return_tensors="pt",

            truncation=True,

        )

        with torch.no_grad():

            outputs = self.model(**inputs)

        probabilities = torch.softmax(

            outputs.logits,

            dim=1,

        )[0]

        prediction = torch.argmax(

            probabilities

        ).item()

        label = self.id2label[prediction]

        confidence = float(

            probabilities[prediction]

        )

        return label.lower(), confidence

    def verify(
        self,
        claim: str,
        documents: list[RetrievedDocument],
    ) -> Evidence:

        if not documents:

            return Evidence(

                method="Fact Verification",

                score=0.5,

                confidence=0.0,

                summary="No evidence found.",

                artifact_path=None,

                metadata={

                    "claim": claim,

                    "verdict": "unknown",

                    "matched_document": None,

                },

            )

        best_document = None

        best_label = "neutral"

        best_confidence = 0.0

        for document in documents:

            label, confidence = self.predict(

                premise=document.content,

                hypothesis=claim,

            )

            if confidence > best_confidence:

                best_label = label

                best_confidence = confidence

                best_document = document

        if "entail" in best_label:

            verdict = "supported"

            score = 0.0

            summary = (
                "Claim supported by retrieved evidence."
            )

        elif "contrad" in best_label:

            verdict = "contradicted"

            score = 1.0

            summary = (
                "Claim contradicted by retrieved evidence."
            )

        else:

            verdict = "unknown"

            score = 0.5

            summary = (
                "Retrieved evidence is inconclusive."
            )

        return Evidence(

            method="Fact Verification",

            score=score,

            confidence=round(
                best_confidence,
                4,
            ),

            summary=summary,

            artifact_path=None,

            metadata={

                "claim": claim,

                "verdict": verdict,

                "nli_label": best_label,

                "matched_document": {

                    "title": best_document.title,

                    "source": best_document.source,

                    "url": best_document.url,

                    "content": best_document.content,

                }

                if best_document

                else None,

            },

        )