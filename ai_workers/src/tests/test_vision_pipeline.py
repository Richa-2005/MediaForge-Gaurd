from pathlib import Path
import traceback

from src.agents.vision_agent import VisionAgent
from src.config import DATA_DIR


def main():

    print("=" * 60)
    print("Running Vision Pipeline Integration Test")
    print("=" * 60)

    sample_image = (
        DATA_DIR
        / "sample_images"
        / "sample_img.jpg"
    )

    if not sample_image.exists():
        raise FileNotFoundError(
            f"Sample image not found: {sample_image}"
        )

    agent = VisionAgent()

    try:

        result = agent.analyze(sample_image , upload_id=1)

        print("\n✓ Vision pipeline completed successfully!\n")

        print(f"Upload ID   : {result.upload_id}")
        print(f"Agent       : {result.agent}")

        print("\nAnalysis")
        print("-" * 40)
        print(f"Label       : {result.analysis.label}")
        print(f"Risk Score  : {result.analysis.risk_score:.4f}")
        print(f"Confidence  : {result.analysis.confidence:.4f}")
        print(f"Explanation : {result.analysis.explanation}")

        # ---------- Face Metadata ----------

        if result.details and "faces" in result.details:

            faces = result.details["faces"]

            print("\nDetected Faces")
            print("-" * 40)
            print(f"Face Count : {faces['face_count']}")

            if faces["bounding_boxes"]:
                print("Bounding Boxes:")

                for box in faces["bounding_boxes"]:
                    print(f"  {box}")

            if faces["saved_faces"]:
                print("Saved Face Crops:")

                for path in faces["saved_faces"]:
                    print(f"  {path}")

        # ---------- Evidence ----------

        print("\nEvidence")
        print("-" * 40)

        for idx, item in enumerate(
            result.analysis.evidence,
            start=1,
        ):

            print(f"\n[{idx}] {item.method}")
            print(f"Score      : {item.score:.4f}")
            print(f"Confidence : {item.confidence:.4f}")
            print(f"Summary    : {item.summary}")

            if item.metadata:

                print("Metadata:")

                for key, value in item.metadata.items():
                    print(f"  {key}: {value}")

        print("\n" + "=" * 60)
        print("✓ Vision Integration Test PASSED")
        print("=" * 60)

    except Exception as e:

        print("\n✗ Vision Integration Test FAILED\n")
        print(e)
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()