import traceback

from src.agents.factcheck_agent import FactCheckAgent


def main():

    print("=" * 60)
    print("Running FactCheck Integration Test")
    print("=" * 60)

    sample = """
    India has 28 states.

    Earth is flat.

    Water boils at 100 degrees Celsius.
    """

    agent = FactCheckAgent()

    try:

        result = agent.analyze(
            sample,
            upload_id="demo_text",
        )

        print("\n✓ FactCheck pipeline completed successfully!\n")

        print(f"Upload ID   : {result.upload_id}")
        print(f"Agent       : {result.agent}")

        print("\nAnalysis")
        print("-" * 40)

        print(f"Label       : {result.analysis.label}")

        print(
            f"Risk Score  : "
            f"{result.analysis.risk_score:.4f}"
        )

        print(
            f"Confidence  : "
            f"{result.analysis.confidence:.4f}"
        )

        print(
            f"Explanation : "
            f"{result.analysis.explanation}"
        )

        print("\nEvidence")
        print("-" * 40)

        for i, item in enumerate(
            result.analysis.evidence,
            start=1,
        ):

            print(f"\n[{i}]")

            print(
                f"Method      : {item.method}"
            )

            print(
                f"Score       : {item.score:.4f}"
            )

            print(
                f"Confidence  : "
                f"{item.confidence:.4f}"
            )

            print(
                f"Summary     : {item.summary}"
            )

            print("\nMetadata")

            for key, value in item.metadata.items():

                print(f"{key}: {value}")

        print("\n" + "=" * 60)

        print("✓ FactCheck Integration PASSED")

        print("=" * 60)

    except Exception as e:

        print("\n✗ FactCheck Integration FAILED\n")

        print(e)

        traceback.print_exc()

        raise


if __name__ == "__main__":

    main()