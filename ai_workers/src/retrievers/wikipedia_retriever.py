import wikipedia
from wikipedia.exceptions import (
    DisambiguationError,
    PageError,
)


class WikipediaRetriever:
    """
    Retrieves supporting information from Wikipedia.

    This retriever does not make the final authenticity
    decision. It only returns retrieved evidence.
    """

    def retrieve(
        self,
        claim: str,
    ) -> dict:

        try:

            summary = wikipedia.summary(
                claim,
                sentences=2,
                auto_suggest=True,
            )

            page = wikipedia.page(
                claim,
                auto_suggest=True,
            )

            return {

                "claim": claim,

                "verdict": "supported",

                "matched_text": summary,

                "source": "Wikipedia",

                "url": page.url,

            }

        except DisambiguationError as e:

            return {

                "claim": claim,

                "verdict": "unknown",

                "matched_text": str(e),

                "source": "Wikipedia",

                "url": None,

            }

        except PageError:

            return {

                "claim": claim,

                "verdict": "unknown",

                "matched_text": None,

                "source": "Wikipedia",

                "url": None,

            }

        except Exception as e:

            return {

                "claim": claim,

                "verdict": "unknown",

                "matched_text": str(e),

                "source": "Wikipedia",

                "url": None,

            }