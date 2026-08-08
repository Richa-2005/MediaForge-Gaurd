from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms
from huggingface_hub import hf_hub_download
from src.processors.mediaforge_model import MediaForgeVision


CLASS_NAMES = {
    0: "authentic",
    1: "manipulated",
}


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

        weights_dir = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "weights"
        )

        weights_dir.mkdir(parents=True, exist_ok=True)

        model_path = weights_dir / "mediaforge_vision_v1.pth"

        if not model_path.exists():

            

            model_path = Path(
                hf_hub_download(
                    repo_id="rashmijha06/mediaforge_vision",
                    filename="mediaforge_vision_v1.pth",
                    local_dir=weights_dir,
                )
            )

        weights = torch.load(
            model_path,
            map_location="cpu",
            weights_only=True,
            mmap=True,
        )

        model = MediaForgeVision()

        model.load_state_dict(
            weights,
            assign=True,
        )

        del weights

        model.to(self._device)

        model.eval()

        MediaForgePredictor._model = model

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