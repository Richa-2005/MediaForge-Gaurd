from pathlib import Path

from src.schemas.evidence import Evidence
from src.utils.spacy_model import load_english_pipeline


class EntityAnalyzer:
    """
    Extracts named entities from text using spaCy.
    """

    def __init__(self):

        self.nlp = load_english_pipeline()

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        doc = self.nlp(text)

        entities = []

        entity_counts = {}

        for ent in doc.ents:

            entities.append(
                {
                    "text": ent.text,
                    "label": ent.label_,
                }
            )

            entity_counts[ent.label_] = (
                entity_counts.get(
                    ent.label_,
                    0,
                )
                + 1
            )

        return Evidence(
            method="Named Entity Recognition",
            score=0.0,
            confidence=1.0,
            summary="Extracted named entities from text.",
            artifact_path=None,
            metadata={
                "entity_count": len(entities),
                "entities": entities,
                "entity_types": entity_counts,
            },
        )
