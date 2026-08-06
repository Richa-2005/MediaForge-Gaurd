"""
Dataset Manifest Builder.

Builds a single canonical manifest from one or more dataset adapters.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd

from .base import DatasetAdapter


class ManifestBuilder:
    """
    Builds a unified manifest from dataset adapters.
    """

    def __init__(self) -> None:
        self.adapters: list[DatasetAdapter] = []

    def add_adapter(self, adapter: DatasetAdapter) -> None:
        """
        Register a dataset adapter.
        """
        self.adapters.append(adapter)

    def build(self) -> pd.DataFrame:
        """
        Build a dataframe from every registered adapter.
        """

        rows = []

        for adapter in self.adapters:

            print(f"Loading {adapter.name}...")

            for sample in adapter.build():

                row = asdict(sample)

                # Convert Paths → strings
                row["image_path"] = str(row["image_path"])

                if row["mask_path"] is not None:
                    row["mask_path"] = str(row["mask_path"])

                # Convert Enums → values
                row["authenticity"] = row["authenticity"].value
                row["origin"] = row["origin"].value
                row["technique"] = row["technique"].value
                row["generator"] = row["generator"].value
                row["split"] = row["split"].value

                rows.append(row)

        df = pd.DataFrame(rows)

        return df

    def save(
        self,
        output: Path,
    ) -> None:
        """
        Build and save the manifest.
        """

        df = self.build()

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            output,
            index=False,
        )

        print(
            f"\nSaved {len(df):,} samples"
        )

        print(output)