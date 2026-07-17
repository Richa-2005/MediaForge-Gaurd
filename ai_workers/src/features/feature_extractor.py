from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models

from src.preprocessing.face_preprocessor import preprocess_face


class FeatureExtractor:
    """
    Extracts CNN embeddings from a face image.
    """

    def __init__(self):

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        weights = models.ResNet18_Weights.DEFAULT

        model = models.resnet18(weights=weights)

        # Remove classification layer
        self.model = nn.Sequential(
            *list(model.children())[:-1]
        )

        self.model.eval()
        self.model.to(self.device)

    @torch.no_grad()
    def extract(self, face_path: Path) -> torch.Tensor:

        tensor = preprocess_face(face_path)

        tensor = tensor.to(self.device)

        embedding = self.model(tensor)

        embedding = embedding.flatten()

        return embedding.cpu()


if __name__ == "__main__":

    sample_face = Path(
        "outputs/demo_faces/face_0000.jpg"
    )

    extractor = FeatureExtractor()

    embedding = extractor.extract(sample_face)

    print("Embedding Shape :", embedding.shape)