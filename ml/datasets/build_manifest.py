"""
Dataset Manifest Builder.

Builds a canonical manifest from one or more dataset adapters.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
import pandas as pd

from .base import DatasetAdapter


class ManifestBuilder:
    """
    Builds a unified manifest from registered dataset adapters.
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
        Build a canonical dataframe from every adapter.
        """
        rows: list[dict] = []

        for adapter in self.adapters:
            print(f"Loading {adapter.name}...")
            for sample in adapter.build():
                # Extract dictionary from dataclass or fallback to custom object/dict
                if hasattr(sample, "to_dict"):
                    row = sample.to_dict()
                elif is_dataclass(sample):
                    row = asdict(sample)
                elif isinstance(sample, dict):
                    row = sample.copy()
                else:
                    row = vars(sample).copy()

                # Convert Paths and Enums to serializable values for Pandas/Parquet
                for key, value in row.items():
                    if isinstance(value, Path):
                        row[key] = str(value)
                    elif hasattr(value, "value"):  # Handles Enum objects
                        row[key] = value.value

                rows.append(row)

        return pd.DataFrame(rows)

    def save(self, output: str | Path) -> Path:
        """
        Build and save the manifest.
        """
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)

        dataframe = self.build()
        dataframe.to_parquet(output, index=False)

        print(f"\nSaved {len(dataframe):,} samples")
        print(output)
        return output