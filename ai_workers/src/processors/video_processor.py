import cv2
import shutil
from pathlib import Path

from src.config import FRAME_OUTPUT_DIR, DATA_DIR
from src.constants import FRAME_SKIP, FRAME_PREFIX, FRAME_EXTENSION


def get_video_metadata(video_path: Path) -> dict:
    """
    Reads a video file and returns its metadata.

    Args:
        video_path (Path): Path to the video.

    Returns:
        dict: Video metadata.
    """

    if not video_path.exists():
        raise FileNotFoundError(f"{video_path} does not exist.")

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = frame_count / fps if fps else 0

    cap.release()

    return {
        "width": width,
        "height": height,
        "fps": fps,
        "frame_count": frame_count,
        "duration": round(duration, 2)
    }



def extract_frames(video_path: Path) -> list[Path]:
    """
    Extracts every FRAME_SKIP-th frame.

    Args:
        video_path (Path): Path to video.

    Returns:
        int: Number of frames saved.
    """

    if not video_path.exists():
        raise FileNotFoundError(f"{video_path} does not exist.")

    FRAME_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    frame_number = 0
    saved_frames = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_number % FRAME_SKIP == 0:

            frame_path = (
                FRAME_OUTPUT_DIR
                / f"{FRAME_PREFIX}{len(saved_frames):04d}{FRAME_EXTENSION}"
            )

            cv2.imwrite(str(frame_path), frame)

            saved_frames.append(frame_path)

        frame_number += 1

    cap.release()

    return saved_frames


def count_saved_frames() -> int:
    """
    Counts the number of extracted frames.
    """

    if not FRAME_OUTPUT_DIR.exists():
        return 0

    return len(list(FRAME_OUTPUT_DIR.glob(f"*{FRAME_EXTENSION}")))



def clear_frame_directory() -> None:
    """
    Removes all previously extracted frames.
    """

    if FRAME_OUTPUT_DIR.exists():
        shutil.rmtree(FRAME_OUTPUT_DIR)

    FRAME_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":

    sample_video = DATA_DIR / "sample_videos" / "sample.mp4"

    metadata = get_video_metadata(sample_video)

    print("Video Metadata")
    print(metadata)

    clear_frame_directory()

    frames = extract_frames(sample_video)

print(f"Extracted {len(frames)} frames")

for frame in frames[:5]:
    print(frame)

print(f"Frames Present: {count_saved_frames()}")