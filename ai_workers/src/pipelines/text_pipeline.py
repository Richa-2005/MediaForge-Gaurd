from src.forensics.text.statistics import TextStatisticsAnalyzer
from src.forensics.text.language import LanguageAnalyzer
from src.forensics.text.readability import ReadabilityAnalyzer
from src.forensics.text.sentiment import SentimentAnalyzer
from src.forensics.text.entities import EntityAnalyzer
from src.forensics.text.claim_extractor import ClaimExtractor


class TextPipeline:
    """
    Runs all text forensic analyzers and collects Evidence.
    """

    def __init__(self):

        self.analyzers = [

            TextStatisticsAnalyzer(),

            LanguageAnalyzer(),

            ReadabilityAnalyzer(),

            SentimentAnalyzer(),

            EntityAnalyzer(),

            ClaimExtractor(),

        ]

    def run(
        self,
        text: str,
    ):

        evidence = []

        for analyzer in self.analyzers:

            try:

                result = analyzer.analyze(text)

                if result:

                    evidence.append(result)

            except Exception as e:

                print(
                    f"{analyzer.__class__.__name__} failed: {e}"
                )

        return evidence