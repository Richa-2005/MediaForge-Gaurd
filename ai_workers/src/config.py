from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR = BASE_DIR / "outputs"

FRAME_OUTPUT_DIR = OUTPUT_DIR / "frames"

AUDIO_OUTPUT_DIR = OUTPUT_DIR / "audio"

TEMP_DIR = BASE_DIR / "temp"

PROCESSED_IMAGE_DIR = OUTPUT_DIR / "processed_images"