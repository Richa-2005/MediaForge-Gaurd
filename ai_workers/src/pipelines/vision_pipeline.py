from pathlib import Path

from src.forensics.blur import BlurAnalyzer
from src.forensics.ela import ELAAnalyzer
from src.forensics.fft import FFTAnalyzer
from src.forensics.noise import NoiseAnalyzer
from src.processors.face_processor import process_faces
from src.schemas.evidence import Evidence


class VisionPipeline:
    """
    Executes the complete vision analysis pipeline.
    """

    def __init__(self):

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

        face_results = process_faces(
            image_path=image_path,
            output_dir=output_dir / "faces",
        )

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

            evidence.append(
                analyzer.analyze(
                    image_path=image_path,
                    artifact_path=artifact_path,
                )
            )

        return evidence, face_results


if __name__ == "__main__":

    pipeline = VisionPipeline()

    evidence, faces = pipeline.run(
        image_path=Path("data/sample_images/sample_img.jpg"),
        output_dir=Path("outputs/pipeline"),
    )

    print(faces)

    for item in evidence:
        print(item)