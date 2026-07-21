from src.forensics.text.statistics import TextStatisticsAnalyzer
from src.forensics.text.language import LanguageAnalyzer
from src.forensics.text.readability import ReadabilityAnalyzer
from src.forensics.text.sentiment import SentimentAnalyzer
from src.forensics.text.entities import EntityAnalyzer
from src.forensics.text.claim_extractor import ClaimExtractor
from src.forensics.text.sensational import SensationalLanguageAnalyzer
from src.forensics.text.clickbait import ClickbaitAnalyzer
from src.forensics.text.repetition import RepetitionAnalyzer
from src.schemas.evidence import Evidence
import logging


logger = logging.getLogger(__name__)

class TextPipeline:
    """
    Runs all text forensic analyzers and collects Evidence.
    """

    def __init__(self):

        analyzer_types = [
            TextStatisticsAnalyzer,
            LanguageAnalyzer,
            ReadabilityAnalyzer,
            EntityAnalyzer,
            ClaimExtractor,
            SentimentAnalyzer,
            SensationalLanguageAnalyzer,
            ClickbaitAnalyzer,
            RepetitionAnalyzer,
        ]
        self.analyzers = []
        for analyzer_type in analyzer_types:
            try:
                self.analyzers.append(analyzer_type())
            except Exception as exc:
                logger.warning(
                    "%s is unavailable: %s",
                    analyzer_type.__name__,
                    exc,
                )

    def run(
        self,
        text: str,
    )-> list[Evidence]:

        evidence = []

        for analyzer in self.analyzers:

            try:

                result = analyzer.analyze(text)

                if result:

                    evidence.append(result)

            except Exception as exc:
                logger.warning(
                    "%s failed: %s",
                    analyzer.__class__.__name__,
                    exc,
                )

        return evidence
