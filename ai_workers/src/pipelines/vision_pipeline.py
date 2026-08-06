from pathlib import Path

from src.forensics.blur import BlurAnalyzer
from src.forensics.ela import ELAAnalyzer
from src.forensics.fft import FFTAnalyzer
from src.forensics.noise import NoiseAnalyzer
from src.processors.face_processor import process_faces
from src.schemas.evidence import Evidence
from src.processors.mediaforge_predictor import MediaForgePredictor

import logging

logger = logging.getLogger(__name__)

class VisionPipeline:
    """
    Executes the complete vision analysis pipeline.
    """

    def __init__(self):
        self.predictor = MediaForgePredictor()
         
        self.analyzers = [
            ELAAnalyzer(),
            NoiseAnalyzer(),
            FFTAnalyzer(),
            BlurAnalyzer(),
        ]

    def run(
        self,
        image_path: Path,
        output_dir: Path,
    ) -> tuple[list[Evidence], dict]:
        """
        Runs all available vision analyzers.

        Returns
        -------
        tuple[list[Evidence], dict]
            (
                forensic evidence,
                face metadata,
            )
        """

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            face_results = process_faces(
                image_path=image_path,
                output_dir=output_dir / "faces",
            )

        except Exception:
            logger.exception("Face processing failed")
            face_results = {}

        prediction = self.predictor.predict(image_path)

        evidence: list[Evidence] = []

        for analyzer in self.analyzers:

            artifact_name = (
                analyzer.__class__.__name__
                .replace("Analyzer", "")
                .lower()
            )

            artifact_path = (
                output_dir /
                f"{artifact_name}.png"
            )

            try:
                result = analyzer.analyze(
                    image_path=image_path,
                    artifact_path=artifact_path,
                )

                if result is not None:
                    evidence.append(result)

            except Exception:
                    logger.exception(
                        "%s failed",
                        analyzer.__class__.__name__,
                    )

        return (prediction, evidence, face_results)


if __name__ == "__main__":

    pipeline = VisionPipeline()

    prediction, evidence, faces = pipeline.run(
        image_path=Path("data/sample_images/sample_img.jpg"),
        output_dir=Path("outputs/pipeline"),
    )

    print(faces)

    for item in evidence:
        print(item)