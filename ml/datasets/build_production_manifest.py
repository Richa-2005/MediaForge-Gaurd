"""
Build production manifests for MediaForge Vision.

Usage
-----
python -m ml.datasets.build_production_manifest
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml
import argparse

# Import adapters so they register themselves
from .adapters import casia  # noqa: F401
from .adapters import coco      # noqa: F401
from .adapters import genimage  # noqa: F401

from .build_manifest import ManifestBuilder
from .environment import Environment
from .registry import create
from .statistics import DatasetStatistics



CONFIG_PATH = Path("ml/configs/datasets.yaml")


def load_config() -> dict:
    """
    Load datasets.yaml.
    """

    with CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(file)


def build_manifest(dataset: str | None = None) -> pd.DataFrame:
    """
    Build the unified dataset manifest.
    """

    config = load_config()

    builder = ManifestBuilder()

    datasets = config["datasets"]

    print("\nBuilding production manifest...\n")

    for dataset_name, dataset_cfg in datasets.items():

        if not dataset_cfg.get(
            "enabled",
            False,
        ):
            continue
        if dataset is not None and dataset_name != dataset:
            continue

        root = Environment.dataset_root(
            dataset_cfg
        )

        print(
            f"{dataset_name:<15} -> {root}"
        )

        adapter = create(
            dataset_cfg["adapter"],
            root,
        )

        builder.add_adapter(
            adapter
        )

    dataframe = builder.build()

    return dataframe


def split_manifest(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split the manifest into train/validation/test.

    If the adapters already populated the split column,
    simply filter by it.
    """

    if "split" not in dataframe.columns:

        raise ValueError(
            "Manifest has no 'split' column."
        )

    train = dataframe[
        dataframe["split"] == "train"
    ]

    validation = dataframe[
        dataframe["split"] == "validation"
    ]

    test = dataframe[
        dataframe["split"] == "test"
    ]

    return (
        train,
        validation,
        test,
    )


def save_manifests(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
) -> None:
    """
    Save parquet manifests.
    """

    output = Environment.manifest_directory()

    train.to_parquet(
        output / "train.parquet",
        index=False,
    )

    validation.to_parquet(
        output / "val.parquet",
        index=False,
    )

    test.to_parquet(
        output / "test.parquet",
        index=False,
    )


def save_statistics(
    dataframe: pd.DataFrame,
) -> None:
    """
    Save and print dataset statistics.
    """

    output = (
        Environment.manifest_directory()
        / "stats.json"
    )

    stats = DatasetStatistics(
        dataframe
    )

    stats.save(output)

    stats.print()


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Dataset to build (coco, casia, genimage).",
    )

    args = parser.parse_args()

    dataframe = build_manifest(
        dataset=args.dataset
    )

    if args.dataset is None:

        train, validation, test = split_manifest(
            dataframe
        )

        save_manifests(
            train,
            validation,
            test,
        )

        save_statistics(
            dataframe
        )

    else:

        output = (
            Environment.manifest_directory()
            / f"{args.dataset}.parquet"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_parquet(
            output,
            index=False,
        )

        print(
            f"\nSaved {output}"
        )


if __name__ == "__main__":

    main()