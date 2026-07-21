from pathlib import Path

from moviepy import VideoFileClip

import numpy as np


def extract_audio(video_path: Path, output_dir: Path) -> Path:
    if not video_path.exists():
        raise FileNotFoundError(f"{video_path} does not exist.")

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{video_path.stem}.wav"

    with VideoFileClip(str(video_path)) as clip:
        if clip.audio is None:
            raise ValueError("Video has no audio track.")

        clip.audio.write_audiofile(str(output_path))

    return output_path


def extract_mfcc(audio_path: Path) -> np.ndarray:
    # Implement later
    raise NotImplementedError


def transcribe_audio(audio_path: Path) -> str | None:
    # Enable Whisper later when FFmpeg is available
    return None
