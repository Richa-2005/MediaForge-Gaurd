from pathlib import Path

from src.forensics.blur import BlurAnalyzer
from src.forensics.ela import ELAAnalyzer
from src.forensics.fft import FFTAnalyzer
from src.forensics.noise import NoiseAnalyzer
from src.processors.face_processor import process_faces


class VisionPipeline:
    """
    Orchestrates all vision preprocessing and forensic analyzers.
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
    ) -> dict:
        """
        Runs the complete vision pipeline.

        Returns:
            dict containing face analysis and forensic evidence.
        """

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------- Face Detection ----------

        face_results = process_faces(
            image_path=image_path,
            output_dir=output_dir / "faces",
        )

        # ---------- Forensic Analysis ----------

        forensic_results = []

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

            evidence = analyzer.analyze(
                image_path=image_path,
                artifact_path=artifact_path,
            )

            forensic_results.append(evidence)

        return {
            "faces": face_results,
            "forensics": forensic_results,
        }


if __name__ == "__main__":

    pipeline = VisionPipeline()

    result = pipeline.run(
        image_path=Path("data/sample_images/sample_img.jpg"),
        output_dir=Path("outputs/pipeline"),
    )

    print(result)