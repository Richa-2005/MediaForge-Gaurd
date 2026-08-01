"""
Build train and validation manifests for MediaForge Vision.

Pipeline

datasets.yaml
        ↓
Enabled adapters
        ↓
Canonical manifest
        ↓
Validation split
        ↓
artifacts/manifests/
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

# Import adapters so they register themselves
from ml.datasets.adapters.casia import CASIAAdapter
from ml.datasets.adapters.coco import COCOAdapter
from ml.datasets.adapters.genimage import GenImageAdapter

from ml.datasets.build_manifest import ManifestBuilder
from ml.datasets.registry import create


CONFIG_PATH = Path("ml/configs/datasets.yaml")


def load_config() -> dict:

    with CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(file)


def main() -> None:

    config = load_config()

    runtime = config["runtime"]["environment"]

    builder = ManifestBuilder()

    # --------------------------------------------------------
    # Build enabled adapters
    # --------------------------------------------------------

    for name, dataset in config["datasets"].items():

        if not dataset["enabled"]:
            continue

        root = Path(

            dataset["kaggle_root"]

            if runtime == "kaggle"

            else dataset["fixture_root"]

        )

        builder.add_adapter(

            create(
                dataset["adapter"],
                root,
            )

        )

    dataframe = builder.build()

    print()

    print(
        f"Loaded {len(dataframe):,} samples."
    )

    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    split_cfg = config["split"]

    train_df, val_df = train_test_split(

        dataframe,

        train_size=split_cfg["train"],

        random_state=split_cfg["random_seed"],

        shuffle=True,

        stratify=(
            dataframe["authenticity"]
            if split_cfg["stratify"]
            else None
        ),

    )

    train_df = train_df.copy()

    val_df = val_df.copy()

    train_df["split"] = "train"

    val_df["split"] = "validation"

    merged = pd.concat(

        [
            train_df,
            val_df,
        ],

        ignore_index=True,

    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    manifest_cfg = config["manifest"]

    output_dir = Path(
        manifest_cfg["output_dir"]
    )

    output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

    train_path = output_dir / manifest_cfg["train_file"]

    val_path = output_dir / manifest_cfg["validation_file"]

    merged_path = output_dir / manifest_cfg["merged_file"]

    train_df.to_parquet(

        train_path,

        index=False,

    )

    val_df.to_parquet(

        val_path,

        index=False,

    )

    merged.to_parquet(

        merged_path,

        index=False,

    )

    statistics = {

        "total": len(merged),

        "train": len(train_df),

        "validation": len(val_df),

        "datasets": merged["dataset"].value_counts().to_dict(),

        "authenticity": merged["authenticity"].value_counts().to_dict(),

    }

    with (
        output_dir
        / manifest_cfg["statistics"]
    ).open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(

            statistics,

            file,

            indent=4,

        )

    print("\n" + "=" * 70)

    print("MediaForge Vision Manifest")

    print("=" * 70)

    print(f"Total      : {len(merged):,}")

    print(f"Train      : {len(train_df):,}")

    print(f"Validation : {len(val_df):,}")

    print()

    print(train_path)

    print(val_path)

    print(merged_path)

    print("=" * 70)


if __name__ == "__main__":

    main()