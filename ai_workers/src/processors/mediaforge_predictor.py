from pathlib import Path
import hashlib
import logging
import os
import time

# Avoid Hugging Face's Xet-backed download path on small containers unless a
# deployment explicitly opts back in.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import torch
import torchvision
import timm

from PIL import Image
from torchvision import transforms
from huggingface_hub import hf_hub_download

from src.processors.mediaforge_model import MediaForgeVision


logger = logging.getLogger(__name__)

logger.info(
    "Vision environment | torch=%s torchvision=%s timm=%s",
    torch.__version__,
    torchvision.__version__,
    timm.__version__,
)

CLASS_NAMES = {
    0: "authentic",
    1: "manipulated",
}

DEFAULT_REPO_ID = "rashmijha06/mediaforge_vision"
DEFAULT_FILENAME = "mediaforge_vision_v1.pth"
DEFAULT_WEIGHTS_PATH = (
    Path(__file__).resolve().parents[2] / "weights" / DEFAULT_FILENAME
)


class MediaForgeWeightsError(RuntimeError):
    """Raised when MediaForge Vision weights cannot be loaded."""


class MediaForgePredictor:

    _model = None

    _device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    _transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    def __init__(self):

        if MediaForgePredictor._model is None:
            self._load_model()

    def _load_model(self):

        model_path = resolve_weights_path()

        logger.info(
            "Loading MediaForge Vision weights | path=%s",
            model_path,
        )

        sha256_hash = hashlib.sha256()

        with open(model_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                sha256_hash.update(chunk)

        sha256 = sha256_hash.hexdigest()

        logger.info(
            "MediaForge Vision weights | sha256=%s",
            sha256,
        )

        weights = torch.load(
            model_path,
            map_location="cpu",
            weights_only=True,
            mmap=True,
        )

        with torch.device("meta"):
            model = MediaForgeVision()

        model.load_state_dict(
            weights,
            assign=True,
        )

        del weights

        if self._device.type != "cpu":
            model = model.to(self._device)

        model.to(self._device)

        model.eval()

        MediaForgePredictor._model = model

        logger.info(
            "Vision model | model=%s device=%s",
            self._model.__class__.__name__,
            self._device,
        )

        logger.info(
            "MediaForge Vision model loaded successfully | device=%s",
            self._device,
        )

    def predict(
        self,
        image_path: Path,
    ):  
        start = time.perf_counter()
        logger.info(
            "Vision input file | path=%s sha256=%s",
            image_path,
            hashlib.sha256(image_path.read_bytes()).hexdigest(),
        )

        image = (
            Image.open(image_path)
            .convert("RGB")
        )

        image = self._transform(image)

        logger.info(
            "Vision input | image=%s tensor_shape=%s dtype=%s "
            "min=%.5f max=%.5f mean=%.5f std=%.5f",
            image_path,
            tuple(image.shape),
            image.dtype,
            image.min().item(),
            image.max().item(),
            image.mean().item(),
            image.std().item()
        )

        image = (
            image
            .unsqueeze(0)
            .to(self._device)
        )


        inference_start = time.perf_counter()

        with torch.no_grad():

            logits = self._model(image)

            logger.info(
                "MediaForge Vision logits | values=%s",
                logits.squeeze().cpu().tolist(),
            )

            probs = torch.softmax(
                logits,
                dim=1,
            )

            confidence, prediction = (
                probs.max(dim=1)
            )
        inference_duration = (
            time.perf_counter() - inference_start
        )

        logger.info(
            "Vision inference completed | "
            "duration=%.3fs logits=%s",
            inference_duration,
            logits.detach().cpu().tolist(),
        )

        

        result = {
            "label": CLASS_NAMES[
                prediction.item()
            ],
            "confidence": float(
                confidence
            ),
            "probabilities": (
                probs
                .squeeze()
                .cpu()
                .tolist()
            ),
        }

        

        logger.info(
            "MediaForge Vision prediction | "
            "image=%s label=%s confidence=%.4f "
            "probabilities=%s duration=%.3fs",
            image_path,
            result["label"],
            result["confidence"],
            result["probabilities"],
            time.perf_counter() - start,
        )

        return result


def resolve_weights_path() -> Path:
    weights_path = Path(
        os.getenv(
            "MEDIAFORGE_VISION_WEIGHTS_PATH",
            str(DEFAULT_WEIGHTS_PATH),
        )
    )

    if weights_path.exists():
        logger.info(
            "MediaForge Vision weights found locally | path=%s",
            weights_path,
        )
        return weights_path

    return download_weights(weights_path)


def download_weights(weights_path: Path) -> Path:
    repo_id = os.getenv("MEDIAFORGE_VISION_REPO_ID", DEFAULT_REPO_ID)
    filename = os.getenv("MEDIAFORGE_VISION_FILENAME", DEFAULT_FILENAME)
    token = os.getenv("HF_TOKEN")

    if not token:
        raise MediaForgeWeightsError(
            "HF_TOKEN is required to download private MediaForge Vision "
            "weights from Hugging Face."
        )

    weights_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "MediaForge Vision weights not found locally | "
        "downloading from Hugging Face repo=%s filename=%s",
        repo_id,
        filename,
    )

    try:
        downloaded_path = Path(
            hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                token=token,
                local_dir=weights_path.parent,
            )
        )
    except Exception as exc:
        raise MediaForgeWeightsError(
            "Failed to download MediaForge Vision weights from Hugging Face."
        ) from exc

    if downloaded_path != weights_path and not weights_path.exists():
        downloaded_path.replace(weights_path)

    return weights_path
