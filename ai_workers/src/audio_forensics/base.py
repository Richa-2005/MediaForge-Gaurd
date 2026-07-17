from abc import ABC, abstractmethod
from pathlib import Path

from src.schemas.evidence import Evidence


class BaseAudioAnalyzer(ABC):
    """
    Abstract base class for all audio forensic analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        audio_path: Path,
    ) -> Evidence:
        """
        Analyze an audio file and return forensic evidence.
        """
        raise NotImplementedError