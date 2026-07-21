import logging
from functools import lru_cache

import spacy


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def load_english_pipeline():
    """Load the optional English model with a runnable fallback."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        logger.warning(
            "spaCy model en_core_web_sm is unavailable; "
            "using the basic English tokenizer."
        )
        pipeline = spacy.blank("en")
        pipeline.add_pipe("sentencizer")
        return pipeline
