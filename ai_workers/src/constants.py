from pathlib import Path


IMAGE_SIZE = (224, 224)

FRAME_INTERVAL = 30

SUPPORTED_IMAGES = [
    ".jpg",
    ".jpeg",
    ".png"
]

SUPPORTED_VIDEOS = [
    ".mp4",
    ".avi",
    ".mov"
]

SUPPORTED_AUDIO = [
    ".wav",
    ".mp3"
]

IMAGE_SIZE = (224,224)

FRAME_SKIP=30
VIDEO_SAMPLE_FPS = 1
MAX_VIDEO_ANALYSIS_FRAMES = 20

MAX_IMAGE_SIZE_MB = 10

MAX_VIDEO_SIZE_MB = 100

MAX_AUDIO_SIZE_MB = 50

FRAME_PREFIX = "frame_"

FRAME_EXTENSION = ".jpg"

PROCESSED_IMAGE_PREFIX = "processed_"

PROCESSED_IMAGE_EXTENSION = ".jpg"
