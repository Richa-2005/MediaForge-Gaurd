

import cv2
from pathlib import Path
import numpy as np
from src.constants import IMAGE_SIZE
from src.config import DATA_DIR , PROCESSED_IMAGE_DIR

def load_image(image_path: Path) -> np.ndarray:
    """
    Loads an image using OpenCV.
    """

    if not image_path.exists():
        raise FileNotFoundError(f"{image_path} does not exist.")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    return image



def get_image_metadata(image: np.ndarray) -> dict:
    """
    Returns metadata for an image.
    """

    height, width, channels = image.shape

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "dtype": str(image.dtype)
    }



def resize_image(image: np.ndarray) -> np.ndarray:
    """
    Resizes image to model input size.
    """

    return cv2.resize(image, IMAGE_SIZE)


def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Converts OpenCV BGR image to RGB.
    """

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_processed_image(
    image: np.ndarray,
    filename: str
) -> Path:
    """
    Saves processed image.
    """

    PROCESSED_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_IMAGE_DIR / filename

    cv2.imwrite(str(output_path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    return output_path


def process_image(image_path: Path):

    image = load_image(image_path)

    metadata = get_image_metadata(image)

    image = resize_image(image)

    image = convert_bgr_to_rgb(image)

    output = save_processed_image(image, image_path.name)

    return {
        "metadata": metadata,
        "output_path": output
    }




if __name__ == "__main__":

    sample_image = DATA_DIR / "sample_images" / "sample.jpg"

    result = process_image(sample_image)

    print(result["metadata"])

    print(result["output_path"])