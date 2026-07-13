import sys
from pathlib import Path

from app.core.config import settings

AI_WORKERS_DIR = Path(__file__).resolve().parents[3] / "ai_workers"
if str(AI_WORKERS_DIR) not in sys.path:
    sys.path.insert(0, str(AI_WORKERS_DIR))

from src.processors.video_processor import (
    get_video_metadata, 
    extract_frames
)
from src.processors.image_processor import (
    process_image
)

from src.processors.audio_processor import (
    extract_audio
)

def get_output_dir(upload, artifact_folder):
    return (
        settings.PROCESSING_DIR
        / artifact_folder
        / upload.sha256_hash
    )

def process_video_adapter(upload):
    video_path = Path(upload.file_path)

    output_dir = get_output_dir(upload,"frames")

    metadata = get_video_metadata(video_path)
    frame_paths = extract_frames(video_path, output_dir)

    artifacts = []

    artifacts.append(
        {
            "upload_id": upload.id,
            "artifact_type": "video_metadata",
            "file_path": None,
            "details": metadata,
        }
    )
    
    for frame in frame_paths:
        artifacts.append(
            {
                "upload_id": upload.id,
                "artifact_type": "frame",
                "file_path": str(frame),
                "details": {}
            }
        )
    return artifacts

def process_image_adapter(upload):

    output_dir = get_output_dir(upload, "image")
    image_path = Path(upload.file_path)
    result = process_image(image_path, output_dir)
    metadata = result["metadata"]

    artifacts = {
        "upload_id": upload.id,
        "artifact_type": "processed_image",
        "file_path": str(result["output_path"]),
        "details": {
            "width": metadata["width"],
            "height": metadata["height"],
            "channels": metadata["channels"],
            "dtype": metadata["dtype"]
        },
    }

    return [artifacts]

def process_audio_adapter(upload):
    output_dir = get_output_dir(upload,"audio")
    
    audio_path = Path(upload.file_path)

    final_path = extract_audio(audio_path,output_dir)

    return [
        {
            "upload_id": upload.id,
            "artifact_type": "processed_audio",
            "file_path": str(final_path),
            "details": {}
        }
    ]



