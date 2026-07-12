from pathlib import Path
from pydantic import BaseModel


class VideoMetadata(BaseModel):
    width: int
    height: int
    fps: float
    frame_count: int
    duration: float


class FrameExtractionResult(BaseModel):
    total_frames: int
    extracted_frames: int
    frame_paths: list[Path]

class ImageMetadata(BaseModel):
    width: int
    height: int
    channels: int
    format: str