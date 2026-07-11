from pathlib import Path
from moviepy import VideoFileClip
from pathlib import Path

from src.config import AUDIO_OUTPUT_DIR, DATA_DIR
sample_video = DATA_DIR / "sample_videos" / "demo_video.mp4"
import whisper
import numpy as np

def extract_audio(video_path: Path) -> Path:
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = AUDIO_OUTPUT_DIR / f"{video_path.stem}.wav"

    with VideoFileClip(str(video_path)) as clip:
        if clip.audio is None:
            raise ValueError("Video has no audio track.")
        clip.audio.write_audiofile(str(output_path))

    return output_path

def extract_mfcc(audio_path: Path) -> np.ndarray:
    pass

_model = whisper.load_model("base")

def transcribe_audio(audio_path: Path) -> str:
    result = _model.transcribe(str(audio_path))
    return None


if __name__ == "__main__":
    sample_video = DATA_DIR / "sample_videos" / "demo_video.mp4"
    audio_path = extract_audio(sample_video)
    print(f"Extracted audio saved to: {audio_path}")
    print(sample_video.resolve())
    print(sample_video.exists())