# vision.py
from pathlib import Path

from src.agents.vision_agent import VisionAgent
from src.schemas.agent_result import AgentResult


def analyze_image(
    image_path: str | Path,
) -> AgentResult:
    """
    Public helper for vision analysis.

    This function delegates image analysis to the VisionAgent.
    """

    agent = VisionAgent()

    return agent.analyze(
        Path(image_path)
    )