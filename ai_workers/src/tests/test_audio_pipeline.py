from pathlib import Path
import traceback

from src.agents.audio_agent import AudioAgent
from src.config import DATA_DIR


def main():
    print("=" * 60)
    print("Running Audio Pipeline Integration Test")
    print("=" * 60)

    sample_video = (
        DATA_DIR
        / "sample_videos"
        / "demo_video.mp4"
    )

    if not sample_video.exists():
        raise FileNotFoundError(
            f"Sample video not found: {sample_video}"
        )

    agent = AudioAgent()

    try:
        result = agent.analyze(sample_video , upload_id=1)

        print("\n✓ Audio pipeline completed successfully!\n")

        print(f"Upload ID   : {result.upload_id}")
        print(f"Agent       : {result.agent}")

        print("\nAnalysis")
        print("-" * 40)
        print(f"Label       : {result.analysis.label}")
        print(f"Risk Score  : {result.analysis.risk_score:.4f}")
        print(f"Confidence  : {result.analysis.confidence:.4f}")
        print(f"Explanation : {result.analysis.explanation}")

        print("\nEvidence")
        print("-" * 40)

        for idx, item in enumerate(result.analysis.evidence, start=1):
            print(f"\n[{idx}] {item.method}")
            print(f"Score      : {item.score:.4f}")
            print(f"Confidence : {item.confidence:.4f}")
            print(f"Summary    : {item.summary}")

            if item.metadata:
                print("Metadata:")
                for key, value in item.metadata.items():
                    print(f"  {key}: {value}")

        print("\n" + "=" * 60)
        print("✓ Integration test PASSED")
        print("=" * 60)

    except Exception as e:
        print("\n✗ Integration test FAILED\n")
        print(e)
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()