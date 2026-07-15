from abc import ABC, abstractmethod
from pathlib import Path

from src.schemas.evidence import Evidence


class BaseAudioAnalyzer(ABC):
    """
    Base class for all audio forensic analyzers.

    Every analyzer receives an audio file and returns
    one standardized Evidence object.
    """

    @abstractmethod
    def analyze(
        self,
        audio_path: Path,
        artifact_path: Path | None = None,
    ) -> Evidence:
        """
        Analyze an audio file and return forensic evidence.
        """
        raise NotImplementedError