from pathlib import Path

import cv2
import numpy as np
import torch


# Standard ImageNet normalization
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Default model input size
MODEL_INPUT_SIZE = (224, 224)


def load_face(face_path: Path) -> np.ndarray:
    """
    Loads a cropped face image from disk.

    Args:
        face_path: Path to cropped face.

    Returns:
        BGR image as numpy array.
    """

    if not face_path.exists():
        raise FileNotFoundError(f"{face_path} does not exist.")

    image = cv2.imread(str(face_path))

    if image is None:
        raise ValueError(f"Unable to read image: {face_path}")

    return image


def resize_face(
    image: np.ndarray,
    size: tuple[int, int] = MODEL_INPUT_SIZE,
) -> np.ndarray:
    """
    Resize image to CNN input size.
    """

    return cv2.resize(image, size)


def bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Convert OpenCV BGR to RGB.
    """

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def normalize_face(image: np.ndarray) -> np.ndarray:
    """
    Normalize image using ImageNet statistics.
    """

    image = image.astype(np.float32) / 255.0

    image = (image - IMAGENET_MEAN) / IMAGENET_STD

    return image


def to_tensor(image: np.ndarray) -> torch.Tensor:
    """
    Convert HWC numpy array to CHW torch tensor.
    """

    tensor = torch.from_numpy(image)

    tensor = tensor.permute(2, 0, 1)

    return tensor.float()


def add_batch_dimension(tensor: torch.Tensor) -> torch.Tensor:
    """
    Convert (C,H,W) -> (1,C,H,W)
    """

    return tensor.unsqueeze(0)


def preprocess_face(face_path: Path) -> torch.Tensor:
    """
    Complete preprocessing pipeline.

    Face
      ↓
    Resize
      ↓
    RGB
      ↓
    Normalize
      ↓
    Tensor
      ↓
    Batch
    """

    image = load_face(face_path)

    image = resize_face(image)

    image = bgr_to_rgb(image)

    image = normalize_face(image)

    tensor = to_tensor(image)

    tensor = add_batch_dimension(tensor)

    return tensor


if __name__ == "__main__":

    sample_face = Path("outputs/demo_faces/face_0000.jpg")

    tensor = preprocess_face(sample_face)

    print("Tensor Shape :", tensor.shape)
    print("Tensor Type  :", tensor.dtype)