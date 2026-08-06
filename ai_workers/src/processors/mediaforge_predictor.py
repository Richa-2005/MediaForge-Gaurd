from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

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

        model_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "weights"
            / "mediaforge_vision_v1.pth"
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