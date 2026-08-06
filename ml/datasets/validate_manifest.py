"""
Validate MediaForge Vision manifests.

Checks:

    • Required columns
    • Missing images
    • Duplicate image IDs
    • Corrupted images
    • Dataset statistics
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image

from ml.utils.config import load_config


REQUIRED_COLUMNS = [

    "image_id",

    "dataset",

    "image_path",

    "authenticity",

    "origin",

    "generator",

    "technique",

    "split",

]


class ManifestValidator:

    def __init__(

        self,

        manifest: Path,

        verify_images: bool = True,

    ) -> None:

        self.manifest = Path(manifest)

        self.verify_images = verify_images

        self.dataframe: pd.DataFrame | None = None

    # ==========================================================
    # Load
    # ==========================================================

    def load(self) -> None:

        if not self.manifest.exists():

            raise FileNotFoundError(

                f"Manifest not found: {self.manifest}"

            )

        self.dataframe = pd.read_parquet(

            self.manifest

        )

    # ==========================================================
    # Schema
    # ==========================================================

    def validate_schema(self) -> None:

        assert self.dataframe is not None

        missing = [

            column

            for column in REQUIRED_COLUMNS

            if column not in self.dataframe.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

    # ==========================================================
    # Duplicate IDs
    # ==========================================================

    def validate_duplicates(self) -> None:

        assert self.dataframe is not None

        duplicates = self.dataframe.duplicated(

            subset="image_id"

        )

        if duplicates.any():

            raise ValueError(

                f"{duplicates.sum()} duplicate image IDs found."

            )

    # ==========================================================
    # Missing Images
    # ==========================================================

    def validate_paths(self) -> None:

        assert self.dataframe is not None

        missing = []

        for path in self.dataframe["image_path"]:

            if not Path(path).exists():

                missing.append(path)

        if missing:

            raise FileNotFoundError(

                f"{len(missing)} missing images."

            )

    # ==========================================================
    # Verify Images
    # ==========================================================

    def validate_images(self) -> None:

        if not self.verify_images:

            return

        assert self.dataframe is not None

        corrupt = []

        for path in self.dataframe["image_path"]:

            try:

                with Image.open(path) as image:

                    image.verify()

            except Exception:

                corrupt.append(path)

        if corrupt:

            raise ValueError(

                f"{len(corrupt)} corrupted images detected."

            )

    # ==========================================================
    # Statistics
    # ==========================================================

    def print_summary(self) -> None:

        assert self.dataframe is not None

        print()

        print("=" * 70)

        print("MediaForge Vision Manifest Summary")

        print("=" * 70)

        print(f"Samples : {len(self.dataframe):,}")

        print()

        print("Datasets")

        print(

            self.dataframe["dataset"]

            .value_counts()

            .to_string()

        )

        print()

        print("Authenticity")

        print(

            self.dataframe["authenticity"]

            .value_counts()

            .to_string()

        )

        print()

        print("Split")

        print(

            self.dataframe["split"]

            .value_counts()

            .to_string()

        )

        print("=" * 70)

    # ==========================================================
    # Run
    # ==========================================================

    def validate(self) -> None:

        self.load()

        self.validate_schema()

        self.validate_duplicates()

        self.validate_paths()

        self.validate_images()

        self.print_summary()


def main() -> None:

    dataset_config = load_config(

        "ml/configs/datasets.yaml"

    )

    manifest_cfg = dataset_config["manifest"]

    manifest_path = (

        Path(manifest_cfg["output_dir"])

        / manifest_cfg["merged_file"]

    )

    validator = ManifestValidator(

        manifest=manifest_path,

        verify_images=dataset_config["validation"][
            "verify_images"
        ],

    )

    validator.validate()

    print()

    print("✓ Manifest validation passed.")


if __name__ == "__main__":

    main()