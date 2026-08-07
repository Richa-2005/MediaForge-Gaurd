"""
Dataset statistics for MediaForge Vision.

Computes summary statistics from the canonical manifest.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class DatasetStatistics:
    """
    Computes dataset statistics from a manifest dataframe.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        self.dataframe = dataframe

    # ==========================================================
    # Dataset Counts
    # ==========================================================

    def dataset_counts(self) -> dict[str, int]:
        """
        Count samples per dataset.
        """

        return (
            self.dataframe["dataset"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

    # ==========================================================
    # Authenticity Counts
    # ==========================================================

    def authenticity_counts(self) -> dict[str, int]:
        """
        Count samples per authenticity class.
        """

        return (
            self.dataframe["authenticity"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

    # ==========================================================
    # Split Counts
    # ==========================================================

    def split_counts(self) -> dict[str, int]:
        """
        Count train / validation / test samples.
        """

        return (
            self.dataframe["split"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

    # ==========================================================
    # Generator Counts
    # ==========================================================

    def generator_counts(self) -> dict[str, int]:
        """
        Count AI generators.
        """

        return (
            self.dataframe["generator"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self) -> dict:
        """
        Return the complete statistics dictionary.
        """

        return {

            "total_images": len(
                self.dataframe
            ),

            "datasets": self.dataset_counts(),

            "authenticity": self.authenticity_counts(),

            "splits": self.split_counts(),

            "generators": self.generator_counts(),
        }

    # ==========================================================
    # Save
    # ==========================================================

    def save(
        self,
        output: str | Path,
    ) -> Path:
        """
        Save statistics as JSON.
        """

        output = Path(output)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(

                self.summary(),

                file,

                indent=4,

            )

        return output

    # ==========================================================
    # Print
    # ==========================================================

    def print(self) -> None:
        """
        Pretty-print dataset statistics.
        """

        stats = self.summary()

        print("\n" + "=" * 70)
        print("MediaForge Vision Dataset Statistics")
        print("=" * 70)

        print(
            f"\nTotal Images : {stats['total_images']:,}"
        )

        print("\nDatasets")

        for name, count in stats["datasets"].items():

            print(
                f"  {name:<20} {count:,}"
            )

        print("\nAuthenticity")

        for name, count in stats["authenticity"].items():

            print(
                f"  {name:<20} {count:,}"
            )

        print("\nSplits")

        for name, count in stats["splits"].items():

            print(
                f"  {name:<20} {count:,}"
            )

        print("\nGenerators")

        for name, count in stats["generators"].items():

            print(
                f"  {name:<20} {count:,}"
            )

        print("\n" + "=" * 70)