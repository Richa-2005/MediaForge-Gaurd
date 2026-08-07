from pathlib import Path
import logging
import os

import torch
from huggingface_hub import hf_hub_download
from PIL import Image
from torchvision import transforms

from src.processors.mediaforge_model import MediaForgeVision


logger = logging.getLogger(__name__)

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
            "Loading MediaForge Vision weights | path=%s device=%s",
            model_path,
            self._device,
        )

        model = MediaForgeVision()

        weights = torch.load(
            model_path,
            map_location=self._device,
        )

        model.load_state_dict(weights)

        model.to(self._device)

        model.eval()

        MediaForgePredictor._model = model
        logger.info("MediaForge Vision model loaded successfully")

    def predict(
        self,
        image_path: Path,
    ):

        image = Image.open(image_path).convert("RGB")

        image = self._transform(image)

        image = image.unsqueeze(0).to(self._device)

        with torch.no_grad():

            logits = self._model(image)

            probs = torch.softmax(logits, dim=1)

            confidence, prediction = probs.max(dim=1)

        return {

            "label": CLASS_NAMES[prediction.item()],

            "confidence": float(confidence),

            "probabilities": probs.squeeze().cpu().tolist(),

        }


def resolve_weights_path() -> Path:
    weights_path = Path(
        os.getenv(
            "MEDIAFORGE_VISION_WEIGHTS_PATH",
            str(DEFAULT_WEIGHTS_PATH),
        )
    )

    if weights_path.exists():
        logger.info(
            "Using cached MediaForge Vision weights | path=%s",
            weights_path,
        )
        return weights_path

    return download_weights(weights_path)


def download_weights(weights_path: Path) -> Path:
    repo_id = os.getenv(
        "MEDIAFORGE_VISION_REPO_ID",
        DEFAULT_REPO_ID,
    )
    filename = os.getenv(
        "MEDIAFORGE_VISION_FILENAME",
        DEFAULT_FILENAME,
    )
    token = os.getenv("HF_TOKEN")

    if not token:
        raise MediaForgeWeightsError(
            "MediaForge Vision weights were not found locally and HF_TOKEN "
            "is not configured. Set HF_TOKEN for the private Hugging Face "
            f"repo {repo_id}, or mount the weights at {weights_path}."
        )

    weights_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        logger.info(
            "Downloading MediaForge Vision weights from Hugging Face | "
            "repo_id=%s filename=%s destination=%s",
            repo_id,
            filename,
            weights_path,
        )
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            token=token,
            local_dir=str(weights_path.parent),
        )
    except Exception as exc:
        raise MediaForgeWeightsError(
            "Failed to download MediaForge Vision weights from Hugging Face "
            f"repo {repo_id}. Check HF_TOKEN, repo access, and filename "
            f"{filename}."
        ) from exc

    downloaded_path = Path(downloaded_path)
    if not downloaded_path.exists():
        raise MediaForgeWeightsError(
            "Hugging Face download completed but the weights file was not "
            f"found at {downloaded_path}."
        )

    if downloaded_path != weights_path and not weights_path.exists():
        downloaded_path.replace(weights_path)

    logger.info(
        "MediaForge Vision weights ready | path=%s size_bytes=%s",
        weights_path,
        weights_path.stat().st_size,
    )

    return weights_path
