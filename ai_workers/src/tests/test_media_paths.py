from pathlib import Path

import pytest

from src.config import DATA_DIR
from src.pipelines.audio_pipeline import AudioPipeline
from src.processors.audio_processor import extract_audio
from src.processors.video_processor import (
    extract_frames,
    frame_sample_interval,
    get_video_metadata,
)


DEMO_VIDEO = DATA_DIR / "sample_videos" / "demo_video.mp4"


def test_retained_demo_video_is_readable():
    metadata = get_video_metadata(DEMO_VIDEO)

    assert metadata["frame_count"] > 0
    assert metadata["duration"] > 0


def test_video_processor_rejects_missing_input(tmp_path):
    missing = tmp_path / "missing.mp4"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        get_video_metadata(missing)

    with pytest.raises(FileNotFoundError, match="does not exist"):
        extract_frames(missing, tmp_path / "frames")


def test_video_frame_sample_interval_uses_target_fps():
    assert frame_sample_interval(30, 1) == 30
    assert frame_sample_interval(24, 2) == 12
    assert frame_sample_interval(0, 1) > 0


def test_audio_processor_rejects_missing_video(tmp_path):
    with pytest.raises(FileNotFoundError, match="does not exist"):
        extract_audio(
            tmp_path / "missing.mp4",
            tmp_path / "audio",
        )


def test_audio_pipeline_rejects_missing_media(tmp_path):
    pipeline = AudioPipeline.__new__(AudioPipeline)

    with pytest.raises(FileNotFoundError, match="input file not found"):
        pipeline.run(
            Path(tmp_path / "missing.wav"),
            tmp_path / "audio",
        )
